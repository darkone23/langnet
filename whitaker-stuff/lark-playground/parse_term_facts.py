import sys
import json
from lark import Lark

TERM_FACTS_GRAMMAR = """
start: noun_line
	  | verb_line
	  | adverb_line
	  | pronoun_line
	  | adjective_line
	  | conjunction_line
	  | vpar_line
	  | prep_line
	  | tack_line
	  | interj_line
	  | num_line
	  | suffix_line
	  | supine_line

noun_line: term "N" declension whitaker_variant case number gender [notes]
pronoun_line: term "PRON" declension whitaker_variant case number gender [notes]
verb_line: term "V" declension whitaker_variant word word [word] num char [notes]
adverb_line: term "ADV" word [notes]
adjective_line: term "ADJ" declension whitaker_variant word char char word [notes]
conjunction_line: term "CONJ" [notes]
vpar_line: term "VPAR" declension whitaker_variant word char char [notes]
prep_line: term "PREP" [notes]
tack_line: term "TACKON" [notes]
interj_line: term "INTERJ" [notes]
num_line: term "NUM" declension whitaker_variant word char char word [notes]
suffix_line: term "SUFFIX" [notes]
supine_line: term "SUPINE" declension whitaker_variant word char char [notes]

gender: char
case: word
number: char
term: /[A-Za-z\.]+/
num: /[0-9]{1}/
word: /[A-Z]+/
char: /[A-Z]{1}/
declension: num
whitaker_variant: num
notes: /[A-Za-z0-9,\/()\[\]~=>.:\-\+'"!_\? ]+/

%import common.WS -> WS
%ignore WS
"""

# class WhitakerTransformer(Transformer):
#     def process_entry(self, items, entry_type):
#         items = [item for item in items if isinstance(item, Token)]
#         print(f"DEBUG ({entry_type}): {items}")

#         if len(items) == 0:
#             return

#         return {
#         }


if __name__ == "__main__":
    input_data = sys.stdin.read().strip()

    if not input_data:
        print("⚠️ No input data received! Please check your input file.")
        sys.exit(1)

    parser = Lark(TERM_FACTS_GRAMMAR)
    for line in input_data.splitlines():
        print("Looking at line:")
        print(line)
        parsed = parser.parse(line)
        # from rich.pretty import pprint
        print(parsed.pretty())
