import sys
import json
import re
from lark import Lark, Transformer

SENSES_GRAMMAR = """
start: sense_line

sense_line: (sense [";"])*

sense: /[A-Za-z0-9,\/()\[\]~=>.:\-\+'"!_\? ]+/

%import common.WS -> WS
%ignore WS
"""


class SenseTransformer(Transformer):
    def extract_parentheses_text(self, text):
        text = text.replace("[", "(").replace("]", ")")
        extracted = " ".join(
            re.findall(r"\((.*?)\)", text, re.DOTALL)
        )  # Extract text inside parentheses, including newlines
        cleaned_text = re.sub(
            r"\s*\(.*?\)\s*", " ", text, flags=re.DOTALL
        ).strip()  # Remove parentheses and enclosed text
        return (cleaned_text, extracted.strip())

        return cleaned_text, extracted

    def sense(self, tokens):
        words = []
        for token in tokens:
            (word_part, notes_part) = self.extract_parentheses_text(f"{token}".strip())
            word = dict(sense=word_part, note=notes_part)
            words.append(word)
        return words

    def sense_line(self, tree):
        senses = []
        notes = []
        for node in tree:
            for sense in node:
                # print(sense)
                (s, n) = (sense["sense"], sense["note"])
                if s:
                    senses.append(s)
                if n:
                    notes.append(n)
        return dict(senses=senses, notes=notes)


if __name__ == "__main__":
    input_data = sys.stdin.read().strip()

    if not input_data:
        print("⚠️ No input data received! Please check your input file.")
        sys.exit(1)

    parser = Lark(SENSES_GRAMMAR)
    xformer = SenseTransformer()
    for line in input_data.splitlines():
        # print("Looking at line:")
        # print(line)
        parsed = parser.parse(line)
        # from rich.pretty import pprint
        # print(parsed.pretty())
        result = xformer.transform(parsed)
        print(result.pretty())
