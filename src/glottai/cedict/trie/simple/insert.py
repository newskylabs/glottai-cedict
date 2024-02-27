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

"""src/glottai/cedict/trie/insert.py:

Insert entries into a trie.

"""


def trie_insert(trie, key, value):
    """Inserts VALUE under KEY into the TRIE.

    Example:

    from glottai.cedict.trie import trie_insert

    trie = {}
    trie_insert(trie, 'word', 'word-entry')
    trie

    > {'w': {'o': {'r': {'d': {True: 'word-entry'}}}}}

    trie = {}
    for word in ['a', 'b', 'aa', 'ab', 'ba', 'bb']:
        trie_insert(trie, word, word)
    trie

    > {'a': {True: 'a',
    >        'a': {True: 'aa'},
    >        'b': {True: 'ab'}},
    >  'b': {True: 'b',
    >        'a': {True: 'ba'},
    >        'b': {True: 'bb'}}}

    """

    if key:
        # Get first and remaining letters
        first, rest = key[0], key[1:]

        # When there is no dictionary for the first letter yet create one
        if first not in trie:
            trie[first] = {}

        # Recursively insert the remaining letters
        trie_insert(trie[first], rest, value)

    else:
        # Store the value under True as key
        if True in trie:
            # When one or more string entries for the given key exist
            # already store the new string value by appending it to
            # those already existing using '\n' as separator.
            trie[True] += "\n" + value

        else:
            # When an entry does not exist yet store the new string
            # value using True als key.
            trie[True] = value
