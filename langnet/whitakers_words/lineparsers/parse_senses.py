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

    def start(self, args):
        return args[0]

    def extract_parentheses_text(self, text):
        text = (
            text.replace("(", "{").replace(")", "}").replace("[", "(").replace("]", ")")
        )
        extracted = " ".join(
            re.findall(r"\((.*?)\)", text, re.DOTALL)
        )  # Extract text inside parentheses, including newlines
        cleaned_text = re.sub(
            r"\s*\(.*?\)\s*", " ", text, flags=re.DOTALL
        ).strip()  # Remove parentheses and enclosed text
        cleaned_text = cleaned_text.replace("{", "(").replace("}", ")")
        return (cleaned_text, extracted.strip())

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
        obj = dict(senses=senses, notes=notes)
        if len(notes) == 0:
            del obj["notes"]
        return obj


class SensesReducer:
    parser = Lark(SENSES_GRAMMAR)
    xformer = SenseTransformer()

    @staticmethod
    def reduce(line):
        tree = SensesReducer.parser.parse(line)
        result = SensesReducer.xformer.transform(tree)
        return result


if __name__ == "__main__":
    input_data = sys.stdin.read().strip()

    if not input_data:
        print("⚠️ No input data received! Please check your input file.")
        sys.exit(1)

    from rich.pretty import pprint

    for line in input_data.splitlines():
        # print("Looking at line:")
        print(line)
        result = SensesReducer.reduce(line)
        pprint(result)
        # print(result.pretty())
