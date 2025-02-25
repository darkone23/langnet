from sh import Command
from pathlib import Path
import re

from rich.pretty import pprint

from .lineparsers import FactsReducer, SensesReducer, CodesReducer


class WhitakersWordsChunker:

    # https://sourceforge.net/p/wwwords/wiki/wordsdoc.htm/

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


def main():

    latin_words = [
        # Common Nouns (1st, 2nd, 3rd, 4th, 5th declension)
        "amor",
        "femina",
        "templum",
        "caesar",
        "maria",
        "bellum",
        "puella",
        "puer",
        "domus",
        "mensa",
        "liber",
        "aqua",
        "nox",
        "luna",
        "sol",
        "stella",
        "mare",
        "terra",
        "ventus",
        "ignis",
        "caput",
        "manus",
        "pes",
        "oculus",
        "auris",
        "cor",
        "mens",
        "vox",
        "flumen",
        "silva",
        "mons",
        "urbs",
        "via",
        "spes",
        "rex",
        "dux",
        "legio",
        "hostis",
        "amicus",
        "civis",
        "gladius",
        "arcus",
        "sagitta",
        "equus",
        "carmen",
        "verbum",
        "ars",
        "virtus",
        "lux",
        "veritas",
        "pax",
        "flos",
        "hortus",
        "agricola",
        "magister",
        "senex",
        "avis",
        "leo",
        "candidatus",
        "spectaculum",
        "fabula",
        "navis",
        "proelium",
        "oratio",
        "tempestas",
        "turris",
        "scutum",
        "spatium",
        "sermo",
        "beneficium",
        "gloria",
        "imago",
        "modus",
        "exemplum",
        "fortuna",
        "caelum",
        "corpus",
        "culpa",
        "genus",
        "gens",
        "iter",
        "locus",
        "mors",
        "odium",
        "plebs",
        "praemium",
        "studium",
        "urbs",
        "virtus",
        "vulnus",
        "dolor",
        "imperium",
        "fides",
        "salus",
        "orbis",
        "vita",
        "fames",
        "victoria",
        "dona",
        "custos",
        "anima",
        "lux",
        "nubes",
        "pontifex",
        "tempus",
        # Adjectives (1st/2nd and 3rd declension)
        "altus",
        "magnus",
        "parvus",
        "bonus",
        "malus",
        "novus",
        "vetus",
        "pulcher",
        "fortis",
        "felix",
        "saevus",
        "gravis",
        "acer",
        "brevis",
        "longus",
        "mirus",
        "notus",
        "pauper",
        "praeclarus",
        "quietus",
        "rarus",
        "robustus",
        "sanctus",
        "subitus",
        "validus",
        "vanus",
        "vehemens",
        "verus",
        "vilis",
        "divinus",
        "dulcis",
        "ferox",
        "ignotus",
        "infelix",
        "laetus",
        "latus",
        "lenis",
        "miser",
        "multus",
        "nobilis",
        "omnis",
        "perpetuus",
        "pius",
        "prudentia",
        "rapidus",
        "rudis",
        "sacer",
        "sapiens",
        "sollicitus",
        "strenuus",
        "tardus",
        "timidus",
        "tristis",
        "validus",
        "vastus",
        "viridis",
        # Verbs (1st, 2nd, 3rd, 4th conjugation, irregular)
        "amo",
        "habeo",
        "dico",
        "facio",
        "fero",
        "capio",
        "venio",
        "audio",
        "curro",
        "sum",
        "possum",
        "volo",
        "nolo",
        "malo",
        "do",
        "sto",
        "lego",
        "scribo",
        "mitto",
        "peto",
        "pono",
        "teneo",
        "cognosco",
        "video",
        "tango",
        "traho",
        "iubeo",
        "vivo",
        "vinco",
        "pugno",
        "servio",
        "laudo",
        "narro",
        "clamo",
        "cado",
        "praebeo",
        "deleo",
        "luceo",
        "credo",
        "desidero",
        "gaudeo",
        "moneo",
        "opprimo",
        "orior",
        "pello",
        "puto",
        "quaero",
        "regno",
        "sedeo",
        "soleo",
        "sto",
        "taceo",
        "tempto",
        "terreo",
        "tollo",
        "utor",
        "veho",
        "verto",
        "voco",
        "vulnero",
        "servio",
        "scio",
        "sentio",
        "spero",
        "spondeo",
        "supero",
        "suus",
        "taceo",
        "torqueo",
        "trado",
        "traho",
        "turbo",
        "vacuo",
        "vado",
        "valeo",
        "vasto",
        "veho",
        "venor",
        "verto",
        "vexo",
        "video",
        "vinco",
        "vivo",
        "volo",
        "voveo",
        "vulnero",
        # Pronouns
        "ego",
        "tu",
        "ille",
        "illa",
        "illud",
        "ipse",
        "ipsa",
        "ipsum",
        "hic",
        "haec",
        "hoc",
        "iste",
        "ista",
        "id",
        "qui",
        "quae",
        "quod",
        "quicumque",
        "quidam",
        "quis",
        "quisque",
        "quilibet",
        "ullus",
        "aliquis",
        "nemo",
        "nihil",
        "sui",
        "se",
        "nos",
        "vos",
        "is",
        "ea",
        "id",
        "mei",
        "tui",
        "noster",
        "vester",
        "suus",
        # Conjunctions
        "et",
        "sed",
        "aut",
        "nec",
        "neque",
        "nam",
        "quamquam",
        "quia",
        "quod",
        "si",
        "ut",
        "nisi",
        "at",
        "itaque",
        "ergo",
        "dum",
        "donec",
        "vel",
        "quoque",
        "sed",
        "tamen",
        "quamvis",
        "etsi",
        "ideo",
        "quoniam",
        "enim",
        # Prepositions (with ablative and accusative)
        "in",
        "cum",
        "de",
        "pro",
        "sub",
        "a",
        "ab",
        "ex",
        "e",
        "sine",
        "prae",
        "ad",
        "ante",
        "circum",
        "contra",
        "inter",
        "ob",
        "per",
        "post",
        "propter",
        "supra",
        "trans",
        "ultra",
        "subter",
        "iuxta",
        "secundum",
        # Adverbs
        "bene",
        "male",
        "saepe",
        "numquam",
        "semper",
        "hic",
        "ibi",
        "inde",
        "mox",
        "nunc",
        "olim",
        "postea",
        "quoties",
        "sic",
        "tamen",
        "tarde",
        "ut",
        "ita",
        "longe",
        "paene",
        "prope",
        "statim",
        "satis",
        # Interjections
        "heu",
        "eheu",
        "vae",
        "papae",
        "io",
        "evax",
        "attat",
        "heus",
        "st",
        "horribile",
        "dictu",
        "ecce",
    ]

    print("calculating words...")
    words = WhitakersWords.words(latin_words)
    for word in words:
        pprint(word)


if __name__ == "__main__":
    main()
