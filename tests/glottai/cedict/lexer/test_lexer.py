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

"""tests/glottai/cedict/lexer/test_lexer.py:

Test for the lexer.

pytest -q tests/glottai/cedict/lexer/test_lexer.py

"""

__author__ = "Dietrich Bollmann"
__email__ = "dietrich@newskylabs.net"
__copyright__ = "Copyright 2023 Dietrich Bollmann"
__license__ = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__ = "2023/08/04"


from glottai.cedict.lexer.lexer import (
    is_newline,
    is_punctuation,
    lexer,
    print_tokens,
)

from glottai.cedict.lexer.token import (
    Token,
    TType,
)


def test_is_newline_000():
    assert is_newline("\n")
    assert not is_newline("x")


def test_is_punctuation_000():
    assert is_punctuation("，")
    assert is_punctuation("。")
    assert not is_punctuation("x")


# Uncomment to generate the test trie "_test_trie1"
# used in the unit test in the current file:
# | def test_generate_test_trie1():
# |     """Uncomment to generate the test tries
# |     used in the unit test in the current file.
# |
# |     """
# |
# |     # Generate and print a test trie
# |     # for the text: "她叫李叶，是一个不太好看的女孩。"
# |     text = "她叫李叶，是一个不太好看的女孩。"
# |     varname = "_test_trie1"
# |     print_test_trie(text, varname=varname)
# |
# |     # The test has to fail
# |     # in order to make pytest print the test trie:
# |     assert False

_test_trie1 = {
    "她": {True: "她 她 [tā] /she/"},
    "叫": {True: "叫 叫 [jiào] /to shout/to be called/"},
    "李": {True: "李 李 [Lǐ] /surname Li/\n李 李 [lǐ] /plum/"},
    "叶": {True: "葉 叶 [Yè] /surname Ye/\n葉 叶 [yè] /leaf/page/"},
    "是": {True: "是 是 [shì] /to be/"},
    "一": {True: "一 一 [yī] /one/"},
    "个": {True: "個 个 [gè] /individual/"},
    "不": {
        "太": {"好": {True: "不太好 不太好 [bù tài hǎo] /not so good/not too well/"}}
    },
    "看": {True: "看 看 [kàn] /to see/to look at/to watch/"},
    "的": {True: "的 的 [de] /of; ~'s (possessive particle)/"},
    "女": {"孩": {True: "女孩 女孩 [nǚ hái] /girl; lass/"}},
}


def test_lexer_000():
    text = "她叫李叶，是一个不太好看的女孩。"
    start = 0
    tokens = lexer(_test_trie1, text, start)

    # DEBUG
    print_tokens(tokens, varname="tokens")

    expected_tokens = [
        Token(
            ttype=TType.CEDICT,
            word="她",
            entry="她 她 [tā] /she/",
            start=0,
            end=1,
        ),
        Token(
            ttype=TType.CEDICT,
            word="叫",
            entry="叫 叫 [jiào] /to shout/to be called/",
            start=1,
            end=2,
        ),
        Token(
            ttype=TType.CEDICT,
            word="李",
            entry="李 李 [Lǐ] /surname Li/\n李 李 [lǐ] /plum/",
            start=2,
            end=3,
        ),
        Token(
            ttype=TType.CEDICT,
            word="叶",
            entry="葉 叶 [Yè] /surname Ye/\n葉 叶 [yè] /leaf/page/",
            start=3,
            end=4,
        ),
        Token(
            ttype=TType.PUNCTUATION,
            word="，",
            entry="， ， [，] /，/",
            start=4,
            end=5,
        ),
        Token(
            ttype=TType.CEDICT,
            word="是",
            entry="是 是 [shì] /to be/",
            start=5,
            end=6,
        ),
        Token(
            ttype=TType.CEDICT,
            word="一",
            entry="一 一 [yī] /one/",
            start=6,
            end=7,
        ),
        Token(
            ttype=TType.CEDICT,
            word="个",
            entry="個 个 [gè] /individual/",
            start=7,
            end=8,
        ),
        Token(
            ttype=TType.CEDICT,
            word="不太好",
            entry="不太好 不太好 [bù tài hǎo] /not so good/not too well/",
            start=8,
            end=11,
        ),
        Token(
            ttype=TType.CEDICT,
            word="看",
            entry="看 看 [kàn] /to see/to look at/to watch/",
            start=11,
            end=12,
        ),
        Token(
            ttype=TType.CEDICT,
            word="的",
            entry="的 的 [de] /of; ~'s (possessive particle)/",
            start=12,
            end=13,
        ),
        Token(
            ttype=TType.CEDICT,
            word="女孩",
            entry="女孩 女孩 [nǚ hái] /girl; lass/",
            start=13,
            end=15,
        ),
        Token(
            ttype=TType.PUNCTUATION,
            word="。",
            entry="。 。 [。] /。/",
            start=15,
            end=16,
        ),
    ]

    assert tokens == expected_tokens
