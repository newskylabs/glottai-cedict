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

"""tests/glottai/cedict/trie/test_insert.py:

Test for utilities to insert entries into a trie.

pytest -q tests/glottai/cedict/trie/test_insert.py

"""

__author__ = "Dietrich Bollmann"
__email__ = "dietrich@newskylabs.net"
__copyright__ = "Copyright 2023 Dietrich Bollmann"
__license__ = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__ = "2023/06/17"


from glottai.cedict.trie.insert import trie_insert


def test_trie_insert_000():
    trie = {}
    trie_insert(trie, "word", "word-entry")
    print("trie:", trie)

    assert trie == {"w": {"o": {"r": {"d": {True: "word-entry"}}}}}


def test_trie_insert_010():
    trie = {}
    for word in ["a", "b", "aa", "ab", "ba", "bb"]:
        trie_insert(trie, word, word)
    print("trie:", trie)

    assert trie == {
        "a": {True: "a", "a": {True: "aa"}, "b": {True: "ab"}},
        "b": {True: "b", "a": {True: "ba"}, "b": {True: "bb"}},
    }


def test_trie_insert_020():
    trie = {}
    trie_insert(trie, "一个个", "一個個 一个个 [yī gè gè] /each and every one/")
    print("trie:", trie)

    assert trie == {
        "一": {"个": {"个": {True: "一個個 一个个 [yī gè gè] /each and every one/"}}}
    }

    trie_insert(trie, "一", "一 一 [yī] /one/")
    print("trie:", trie)

    assert trie == {
        "一": {
            True: "一 一 [yī] /one/",
            "个": {"个": {True: "一個個 一个个 [yī gè gè] /each and every one/"}},
        }
    }

    trie_insert(trie, "个", "個 个 [gè] /(classifier)")
    print("trie:", trie)

    assert trie == {
        "一": {
            True: "一 一 [yī] /one/",
            "个": {"个": {True: "一個個 一个个 [yī gè gè] /each and every one/"}},
        },
        "个": {True: "個 个 [gè] /(classifier)"},
    }

    trie_insert(trie, "不太好", "不太好 不太好 [bù tài hǎo] /not so good/not too well/")
    print("trie:", trie)

    assert trie == {
        "一": {
            True: "一 一 [yī] /one/",
            "个": {"个": {True: "一個個 一个个 [yī gè gè] /each and every one/"}},
        },
        "个": {True: "個 个 [gè] /(classifier)"},
        "不": {
            "太": {
                "好": {True: "不太好 不太好 [bù tài hǎo] /not so good/not too well/"}
            }
        },
    }

    trie_insert(trie, "看", "看 看 [kān] /to see/to look at/")
    print("trie:", trie)

    assert trie == {
        "一": {
            True: "一 一 [yī] /one/",
            "个": {"个": {True: "一個個 一个个 [yī gè gè] /each and every one/"}},
        },
        "个": {True: "個 个 [gè] /(classifier)"},
        "不": {
            "太": {
                "好": {True: "不太好 不太好 [bù tài hǎo] /not so good/not too well/"}
            }
        },
        "看": {True: "看 看 [kān] /to see/to look at/"},
    }

    trie_insert(trie, "的", "的 的 [de] /(attribution)/")
    print("trie:", trie)

    assert trie == {
        "一": {
            True: "一 一 [yī] /one/",
            "个": {"个": {True: "一個個 一个个 [yī gè gè] /each and every one/"}},
        },
        "个": {True: "個 个 [gè] /(classifier)"},
        "不": {
            "太": {
                "好": {True: "不太好 不太好 [bù tài hǎo] /not so good/not too well/"}
            }
        },
        "看": {True: "看 看 [kān] /to see/to look at/"},
        "的": {True: "的 的 [de] /(attribution)/"},
    }

    trie_insert(trie, "女孩", "女孩 女孩 [nǚ hái] /girl; lass/")
    print("trie:", trie)

    assert trie == {
        "一": {
            True: "一 一 [yī] /one/",
            "个": {"个": {True: "一個個 一个个 [yī gè gè] /each and every one/"}},
        },
        "个": {True: "個 个 [gè] /(classifier)"},
        "不": {
            "太": {
                "好": {True: "不太好 不太好 [bù tài hǎo] /not so good/not too well/"}
            }
        },
        "看": {True: "看 看 [kān] /to see/to look at/"},
        "的": {True: "的 的 [de] /(attribution)/"},
        "女": {"孩": {True: "女孩 女孩 [nǚ hái] /girl; lass/"}},
    }
