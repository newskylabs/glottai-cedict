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

"""src/glottai/cedict/lexer/lexer.py:

A simple lexer.

"""

__author__ = "Dietrich Bollmann"
__email__ = "dietrich@newskylabs.net"
__copyright__ = "Copyright 2023 Dietrich Bollmann"
__license__ = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__ = "2022/12/27"

from .token import Token, TType

from glottai.cedict.trie import trie_lookup


def is_newline(char):
    return char == "\n"


_punctuation_chars = "，。"


def is_punctuation(char):
    return char in _punctuation_chars


def lexer(trie, text, start):
    """Analyse TEXT into a list of tokens as found in TRIE
    starting at character START.

    Example:

    text = "她叫李叶，是一个不太好看的女孩。"
    start = 0
    trie = {
        "她": {True: "她 她 [tā] /she/"},
        "叫": {True: "叫 叫 [jiào] /to shout/to be called/"},
        "李": {True: "李 李 [Lǐ] /surname Li/\n李 李 [lǐ] /plum/"},
        "叶": {True: "葉 叶 [Yè] /surname Ye/\n葉 叶 [yè] /leaf/page/"},
        "是": {True: "是 是 [shì] /to be/"},
        "一": {True: "一 一 [yī] /one/"},
        "个": {True: "個 个 [gè] /individual/"},
        "不": {
            "太": {
                "好": {True: "不太好 不太好 [bù tài hǎo] /not so good/not too well/"}
            },
        },
        "看": {True: "看 看 [kàn] /to see/to look at/to watch/"},
        "的": {True: "的 的 [de] /of; ~'s (possessive particle)/"},
        "女": {"孩": {True: "女孩 女孩 [nǚ hái] /girl; lass/"}},
    }

    tokens = lexer(trie, text, start)

    Results in the following token list:

    tokens = [
        Token('她', ttype=TType.CEDICT, start=0, end=1),
        Token('叫', ttype=TType.CEDICT, start=1, end=2),
        Token('李', ttype=TType.CEDICT, start=2, end=3),
        Token('叶', ttype=TType.CEDICT, start=3, end=4),
        Token('，', ttype=TType.PUNCTUATION, start=4, end=5),
        Token('是', ttype=TType.CEDICT, start=5, end=6),
        Token('一', ttype=TType.CEDICT, start=6, end=7),
        Token('个', ttype=TType.CEDICT, start=7, end=8),
        Token('不太好', ttype=TType.CEDICT, start=8, end=11),
        Token('看', ttype=TType.CEDICT, start=11, end=12),
        Token('的', ttype=TType.CEDICT, start=12, end=13),
        Token('女孩', ttype=TType.CEDICT, start=13, end=15),
        Token('。', ttype=TType.PUNCTUATION, start=15, end=16)
    ]

    """

    text_length = len(text)
    start = 0
    tokens = []
    while True:
        # Done?
        # When the 'start' index is equal to 'text_length'
        # the whole text has been processed
        if start == text_length:
            # Done
            #
            # Return the list of found tokens
            return tokens

        # Try to find lonest prefix defined in EDICT
        word, entry, end = trie_lookup(trie, text, text_length, start)

        if word:
            # Found a longest prefix in EDICT
            token = Token(
                ttype=TType.CEDICT,
                word=word,
                entry=entry,
                start=start,
                end=end,
            )

            # Continue with the next prefix
            start = end

        else:
            # Nothing found in EDICT
            # Lets see what kind of character we have
            char = text[start]
            end = start + 1

            if is_newline(char):
                # Newline character
                token = Token(
                    ttype=TType.NEWLINE,
                    word=char,
                    entry=f"{char} {char} [{char}] /{char}/",
                    start=start,
                    end=end,
                )

            elif is_punctuation(char):
                # Punctuation character
                token = Token(
                    ttype=TType.PUNCTUATION,
                    word=char,
                    entry=f"{char} {char} [{char}] /{char}/",
                    start=start,
                    end=end,
                )

            else:
                # Unknown token
                token = Token(
                    ttype=TType.UNKNOWN,
                    word=char,
                    entry=f"{char} {char} [{char}] /{char}/",
                    start=start,
                    end=end,
                )

            # Continue with the next character in text
            start = end

        # Append the found token to the list of tokens
        tokens.append(token)


def print_tokens(tokens, indent=0, varname=None, end="\n", pretty_print=False):
    """Pretty print tokens returned by the lexer."""

    indent_str = "    " * indent
    indent_elem_str = indent_str + "    "
    print(indent_str, end="")

    if varname is not None:
        print(f"{varname} = ", end="")

    print("[")

    token_indent = indent + 1
    for i, token in enumerate(tokens):
        if i > 0:
            print(",")

        if pretty_print:
            token.pprint(indent=token_indent, end="")

        else:
            print(indent_elem_str, end="")
            print(token, end="")

    print("")
    print(indent_str, end="")
    print("]", end=end)
