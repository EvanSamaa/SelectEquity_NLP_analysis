from __future__ import print_function
from __future__ import unicode_literals

from builtins import str, bytes, dict, int

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from builtins import str, bytes, dict, int
from pattern.en import article, referenced
from pattern.en import pluralize, singularize
from pattern.en import comparative, superlative
from pattern.en import conjugate, lemma, lexeme, tenses
from pattern.en import NOUN, VERB, ADJECTIVE
from pattern.en import number, numerals, quantify, reflect
from pattern.en import parse, pprint, tag
from pattern.en import parse, Text
#'''
# The singularize() function returns the singular form of a plural noun (or adjective).
# It is slightly less robust than the pluralize() function.
for word in ["parts-of-speech", "children", "dogs'", "wolves", "bears", "kitchen knives",
             "octopodes", "matrices", "matrixes"]:
    print(singularize(word))
print(singularize("our", pos=ADJECTIVE))
print("")



print(number("I am two thousand five hundred and eight years old"))
print(number("two point eighty-five"))
print("")
#'''

