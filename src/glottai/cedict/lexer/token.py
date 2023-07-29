# ==========================================================
# Copyright 2023 Dietrich Bollmann
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------

"""src/glottai/cedict/lexer/token.py:

Token and token type TType
as well as Token related utilities.

"""

__author__ = "Dietrich Bollmann"
__email__ = "dietrich@newskylabs.net"
__copyright__ = "Copyright 2023 Dietrich Bollmann"
__license__ = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__ = "2022/12/27"


from enum import Enum


class TType(Enum):
    UNKNOWN = 0
    CEDICT = 1
    NEWLINE = 2
    PUNCTUATION = 3


class Token:
    """ """

    def __init__(self, ttype, word, entry, start, end):
        self.ttype = ttype
        self.word = word
        self.entry = entry
        self.start = start
        self.end = end

    def print(self, end="\n"):
        print(f"{self}: {self.entry}", end=end)

    def __str__(self):
        return (
            f"Token({repr(self.word)}, "
            f"ttype={self.ttype}, "
            f"start={self.start}, "
            f"end={self.end})"
        )

    def __repr__(self):
        return (
            f"Token(ttype={self.ttype}, "
            f"word={repr(self.word)}, "
            f"entry={repr(self.entry)}, "
            f"start={self.start}, "
            f"end={self.end})"
        )

    def __eq__(self, other):
        if not isinstance(other, Token):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return (
            self.ttype == other.ttype
            and self.word == other.word
            and self.entry == other.entry
            and self.start == other.start
            and self.end == other.end
        )

    def pprint(self, indent=0, end="\n"):
        i = "    " * indent
        print(
            f"{i}Token(\n"
            f"{i}    ttype = {self.ttype},\n"
            f"{i}    word  = {repr(self.word)},\n"
            f"{i}    entry = {repr(self.entry)},\n"
            f"{i}    start = {self.start},\n"
            f"{i}    end   = {self.end}\n"
            f"{i})",
            end=end,
        )


def pretty_print_token_list(token_list, varname=None, indent=0, end="\n"):
    """ """

    if varname is not None:
        print(f"{varname} = ", end="")

    print("[")

    i = 0
    for token in token_list:
        if i > 0:
            print(",")

        token.pprint(indent=indent + 1, end="")

        i += 1

    print("")

    i = "    " * indent
    print(f"{i}]", end=end)
