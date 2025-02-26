from sh import Command
from pathlib import Path
import re

from rich.pretty import pprint

from .lineparsers import FactsReducer, SensesReducer, CodesReducer


class WhitakersWordsChunker:

    # https://sourceforge.net/p/wwwords/wiki/wordsdoc.htm/

    # TODO: this is blowing up if not available
    # should be a litle nicer and just have some error state like 'dont use me'
    
    ww = Command(Path.home() / ".local/bin/whitakers-words")
    term_pattern = r"^[a-z.]+(?:\.[a-z]+)*\s+[A-Z]+"

    def __init__(self, input: list[str]):
        # we might be in a special input mode
        # need special output parsing for that case
        self.input = input
        self.result = self.ww(*input)

    def classify_line(self, line):
        line_type = None
        if ";" in line:
            line_type = "sense"
        elif "]" in line:
            line_type = "term-code"
        elif "RETURN/ENTER" in line or "exception in PAUSE" in line or "*" == line:
            line_type = "ui-control"
        elif line.startswith("Word mod") or "An internal 'b'" in line:
            line_type = "ui-control"
        elif line.strip() == "":
            line_type = "empty"
        elif re.match(self.term_pattern, line):
            line_type = "term-facts"
        else:
            line_type = "unknown"
        return dict(line_txt=line, line_type=line_type)

    def get_next_word(
        self, current: dict | None, last_line: dict | None, line_info: dict
    ):
        next_word = dict(lines=[line_info])
        start_new_word = False

        if not last_line:
            start_new_word = True
        else:
            this_line_type = line_info["line_type"]
            last_line_type = last_line["line_type"]
            if last_line_type == "term-code":
                start_new_word = this_line_type != "sense"
            elif last_line_type == "sense":
                if this_line_type == "unknown":
                    pass
                else:
                    start_new_word = this_line_type != "sense"
            elif last_line_type == "unknown":
                start_new_word = this_line_type.startswith("term-")

        if start_new_word:
            return next_word
        else:
            current["lines"].append(line_info)
            return current

    def analyze_chunk(self, entry: dict):
        entry["txts"] = txts = []
        entry["types"] = types = []
        for line in entry["lines"]:
            line_type = line["line_type"]
            line_txt = line["line_txt"]
            if line_type == "ui-control" or line_type == "empty":
                pass
            else:
                txts.append(line_txt)
                types.append(line_type)
        entry["size"] = len(txts)
        del entry["lines"]

    def get_word_chunks(self):
        word_chunks = []
        current_word = None
        last_line = None
        for line in self.result.splitlines():
            line_info = self.classify_line(line)
            next_word = self.get_next_word(current_word, last_line, line_info)
            last_line = line_info
            if next_word is not current_word:
                current_word = next_word
                word_chunks.append(current_word)
        for chunk in word_chunks:
            self.analyze_chunk(chunk)
        return word_chunks


class WhitakersWords:

    @staticmethod
    def words(search: list[str]):
        words_chunker = WhitakersWordsChunker(search)
        chunks = words_chunker.get_word_chunks()
        wordlist = []

        def smart_merge(src: dict, dest: dict):
            for k, v in src.items():
                if k in dest:
                    _v = dest[k]
                    if v == _v:
                        pass
                    else:
                        if type(v) == list and type(_v) == list:
                            dest[k] = v + _v
                        elif type(v) == list:
                            dest[k] = v + [f"{_v}".strip()]
                        elif type(_v) == list:
                            dest[k] = _v + [f"{v}".strip()]
                        else:
                            print("OH NO A COLLISION!", k, v, _v, v == _v)
                else:
                    dest[k] = v

        for word_chunk in chunks:
            unknown = []
            terms = []
            lines = []
            word = dict(terms=terms, raw_lines=lines, unknown=unknown)
            for i in range(word_chunk["size"]):
                (txt, line_type) = (word_chunk["txts"][i], word_chunk["types"][i])
                # print(line_type, txt)
                lines.append(txt)
                if line_type == "sense":
                    data = SensesReducer.reduce(txt)
                    smart_merge(data, word)
                elif line_type == "term-facts":
                    data = FactsReducer.reduce(txt)
                    terms.append(data)
                elif line_type == "term-code":
                    data = CodesReducer.reduce(txt)
                    smart_merge(dict(codeline=data), word)
                elif line_type == "unknown":
                    unknown.append(txt)
                else:
                    assert False, f"Unexpected line type! [{line_type}]"
            if len(unknown) == 0:
                del word["unknown"]
            if len(lines):
                wordlist.append(word)
        return wordlist
