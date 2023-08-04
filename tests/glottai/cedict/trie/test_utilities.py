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

"""tests/glottai/cedict/trie/test_utilities.py:

Test for the trie utilities.

pytest -q tests/glottai/cedict/trie/test_utilities.py

"""

__author__ = "Dietrich Bollmann"
__email__ = "dietrich@newskylabs.net"
__copyright__ = "Copyright 2023 Dietrich Bollmann"
__license__ = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__ = "2023/08/04"


import sys

from glottai.cedict.trie.utilities import (
    extract_test_trie,
    print_test_trie,
)


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


# Uncomment to generate the test trie "_test_trie2"
# used in the unit test in the current file:
# | def test_generate_test_trie2():
# |     """Uncomment to generate the test tries
# |     used in the unit test in the current file.
# |
# |     """
# |
# |     # Generate and print a test trie
# |     # for the text: "她叫李叶，是一个不太好看的女孩。"
# |     text = "她叫李叶。"
# |     varname = "_test_trie2"
# |     print_test_trie(text, trie=_test_trie1, varname=varname)
# |
# |     # The test has to fail
# |     # in order to make pytest print the test trie:
# |     assert False

_test_trie2 = {
    "她": {True: "她 她 [tā] /she/"},
    "叫": {True: "叫 叫 [jiào] /to shout/to be called/"},
    "李": {True: "李 李 [Lǐ] /surname Li/\n李 李 [lǐ] /plum/"},
    "叶": {True: "葉 叶 [Yè] /surname Ye/\n葉 叶 [yè] /leaf/page/"},
}


def test_extract_test_trie000():
    text = "她叫李叶，是一个不太好看的女孩。"
    test_trie = extract_test_trie(_test_trie1, text)
    assert test_trie == _test_trie1


def test_extract_test_trie010():
    text = "她叫李叶。"
    test_trie = extract_test_trie(_test_trie1, text)
    assert test_trie == _test_trie2


def test_capsys(capsys):
    """Access captured output in capsys

    See:

    Accessing captured output from a test function
    https://docs.pytest.org/en/7.1.x/how-to/capture-stdout-stderr.html
    """
    print("hello")
    sys.stderr.write("world\n")
    captured = capsys.readouterr()
    assert captured.out == "hello\n"
    assert captured.err == "world\n"
    print("next")
    captured = capsys.readouterr()
    assert captured.out == "next\n"


def test_print_test_trie000(capsys):  # Access captured output in capsys
    text = "她叫李叶，是一个不太好看的女孩。"
    varname = "trie"
    print_test_trie(text, trie=_test_trie1, varname=varname)

    captured = capsys.readouterr()

    expected_output = """trie = {
    '她': {
        True: '她 她 [tā] /she/'
    },
    '叫': {
        True: '叫 叫 [jiào] /to shout/to be called/'
    },
    '李': {
        True: '李 李 [Lǐ] /surname Li/\\n李 李 [lǐ] /plum/'
    },
    '叶': {
        True: '葉 叶 [Yè] /surname Ye/\\n葉 叶 [yè] /leaf/page/'
    },
    '是': {
        True: '是 是 [shì] /to be/'
    },
    '一': {
        True: '一 一 [yī] /one/'
    },
    '个': {
        True: '個 个 [gè] /individual/'
    },
    '不': {
        '太': {
            '好': {
                True: '不太好 不太好 [bù tài hǎo] /not so good/not too well/'
            }
        }
    },
    '看': {
        True: '看 看 [kàn] /to see/to look at/to watch/'
    },
    '的': {
        True: "的 的 [de] /of; ~'s (possessive particle)/"
    },
    '女': {
        '孩': {
            True: '女孩 女孩 [nǚ hái] /girl; lass/'
        }
    }
}"""

    assert captured.out == expected_output


def test_print_test_trie010(capsys):  # Access captured output in capsys
    text = "她叫李叶。"
    varname = "trie"
    print_test_trie(text, trie=_test_trie1, varname=varname)

    captured = capsys.readouterr()

    expected_output = """trie = {
    '她': {
        True: '她 她 [tā] /she/'
    },
    '叫': {
        True: '叫 叫 [jiào] /to shout/to be called/'
    },
    '李': {
        True: '李 李 [Lǐ] /surname Li/\\n李 李 [lǐ] /plum/'
    },
    '叶': {
        True: '葉 叶 [Yè] /surname Ye/\\n葉 叶 [yè] /leaf/page/'
    }
}"""

    assert captured.out == expected_output
