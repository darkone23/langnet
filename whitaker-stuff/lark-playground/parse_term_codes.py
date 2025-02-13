import sys
import json
from lark import Lark

TERM_CODES_GRAMMAR = """
start: simple_code_line | full_code_line | basic_code_line 

simple_code_line: term_info pos code_chunk [notes]
full_code_line: term_info pos [person] [pos_info] code_chunk [notes]
basic_code_line: code_chunk [notes]

pos_info: /[A-Z]{1,7}/
pos: /[A-Z]{1,7}/
term_txt: /[A-Za-z.]{1}[a-z., ()-\/]+/
term_info: proper_names | term_txt
proper_names: name ("," name)*
name: /[A-Z][a-z]+/
person: "(" /[0-9]{1}[sthnrd]{2}/ ")"

age: char
area: char
geo: char
freq: char
source: char
code: age area geo freq source
code_chunk: "[" code  "]"

term: /[A-Za-z\.]+/
num: /[0-9]{1}/
word: /[A-Z]+/
char: /[A-Z]{1}/
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

    parser = Lark(TERM_CODES_GRAMMAR)
    for line in input_data.splitlines():
        print("Looking at line:")
        print(line)
        parsed = parser.parse(line)
        # from rich.pretty import pprint
        print(parsed.pretty())
