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

"""glottai/cedict/trie/utilities.py:

CC-CEDICT trie test utilities.

"""


def extract_test_trie(trie, text):
    """The entries of CC-CEDICT are constantly updated.  For testing
    dictionary-based functionality, however, we want the same entries
    being returned for the same queries.  For this purpose we can
    generate subsets of CC-CEDICT and use them for testing.

    Given a TEXT The current function extracts and returnes a subset
    of the current CC-CEDICT version which only contains the entries
    occuring in the given TEXT.  This subset then can be used for
    testing.

    """

    from glottai.cedict.lexer import TType, lexer
    from glottai.cedict.trie import trie_insert

    start = 0
    tokens = lexer(trie, text, start)

    trie = {}
    for token in tokens:
        if token.ttype == TType.CEDICT:
            trie_insert(trie, token.word, token.entry)

    return trie


def print_test_trie(text, trie=None, varname=None, file=None):
    """Extract and print a test trie dictionary.  When a TRIE is
    provided use it to extract the test trie; when no TRIE has been
    provided the current version of the simplified CC-CEDICT trie is
    used.  When a filehandle is provided via FILE, the test trie is
    printed to the corresponding stream; without a given filehandle
    stdout is used.  When a VARNAME is given, the dictionary encoding
    the trie is printed as an assignment to the variable VARNAME.

    """

    # When no TRIE is given
    # use glottai.cedict.cedict.cedict_trie_simplified
    if trie is None:
        from glottai.cedict.cedict.cedict_trie_simplified import CEDICT_trie

        trie = CEDICT_trie

    # When no FILE is given
    # print to stdout
    if file is None:
        # Write to stdout
        import sys

        file = sys.stdout

    # Extract the test trie
    test_trie = extract_test_trie(trie, text)

    if varname is not None:
        print(f"{varname} = ", end="", file=file)

    from glottai.cedict.trie import pretty_print_trie

    pretty_print_trie(test_trie, file=file)

    # Flush the stream
    file.flush()
