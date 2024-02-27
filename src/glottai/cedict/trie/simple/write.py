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

"""src/glottai/cedict/trie/write.py:

Utilities to write tries.

"""

__author__ = "Dietrich Bollmann"
__email__ = "dietrich@newskylabs.net"
__copyright__ = "Copyright 2023 Dietrich Bollmann"
__license__ = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__ = "2023/06/16"


from functools import cmp_to_key


def write_trie_to_file(fh, header, variables, trie, format="readable"):
    """Write the given HEADER, VARIABLES and TRIE to the file
    represented by FH.

    FORMAT can either be 'compact' or 'readable'.

    """

    # Write trie to file
    _write_header(fh, header)
    _write_variables(fh, variables)
    _write_trie(fh, trie, format=format)
    _write_footer(fh)


def _write_header(fh, header):
    """Format and write the trie HEADER to the file represented by
    FH.

    """

    # Write header prefix
    # for the Python trie version of CC-CEDICT
    fh.write(
        "# CC-CEDICT Python trie\n"
        "# \n"
        "# Generated from the CC-CEDICT text file published by MDBG\n"
        "# \n"
        "# Original header of the CC-CEDICT text file:\n"
    )

    # Marker for the begin of the original CC-CEDICT header
    fh.write("# --\n")

    # Write thr original header from the CC-CEDICT text file
    header_str = "\n".join(header)
    fh.write(header_str)
    fh.write("\n")

    # Marker for the end of the original CC-CEDICT header
    fh.write("# --\n")
    fh.write("\n")


def _write_variables(fh, variables):
    """Format and write the given VARIABLES to the file represented by
    FH.

    """

    # Write variable name
    fh.write("CEDICT_variables = {\n")

    i = 0
    for key, value in variables.items():
        if i > 0:
            fh.write(",\n")
        fh.write(f"  '{key}': '{value}'")
        i += 1
    fh.write("\n")

    fh.write("}\n")
    fh.write("\n")


def _write_trie(fh, trie, format="readable"):
    """Write the given TRIE to the file represented by FH.

    FORMAT can either be 'compact' or 'readable'.

    """

    # Should I print in 'readable' or 'compact' format?
    if format == "compact":
        _write_trie_compact(fh, trie)

    elif format == "readable":
        _write_trie_readable(fh, trie)

    elif format == "pretty":
        _write_trie_pretty(fh, trie)

    else:
        # ERROR Unknown hanzi format - exiting
        print(f"ERROR Print trie format: {format}")
        print("Only 'compact' and 'readable' are defined formats.")
        import sys

        sys.exit(1)


def _write_footer(fh):
    """Write the trie file footer to the file represented by FH.

    FORMAT can either be 'compact' or 'readable'.

    """

    fh.write("# fin.\n")


# ==========================================================


def _write_trie_compact(fh, trie):
    """Write TRIE to FH in compact format to the file represented by
    FH."""

    # Write variable name
    fh.write("CEDICT_trie = ")

    # Use the string representation of dictionaries
    # to write the trie dictionary in a compact form
    fh.write(str(trie))
    fh.write("\n")

    # Write an empty line
    fh.write("\n")


# ==========================================================


def _write_trie_readable(fh, trie):
    """Write TRIE to FH in readable format to the file represented by
    FH."""

    # Write variable name
    fh.write("CEDICT_trie = ")

    # Write the trie
    _write_trie_dict(fh, trie)
    fh.write("\n")

    # Write an empty line
    fh.write("\n")


def _trie_compare_keys(key_value1, key_value2):
    """Compare trie keys."""

    key1, key2 = key_value1[0], key_value2[0]

    key1_is_True = key1 is True
    key2_is_True = key2 is True

    if key1_is_True:
        if key2_is_True:
            return 0

        else:
            return -1

    elif key2_is_True:
        return 1

    else:
        key1, key2 = str(key1), str(key2)
        if key1 == key2:
            return 0

        if key1 < key2:
            return -1

        else:
            return 1


def _write_trie_dict(fh, trie, word=""):
    """Recursively write a TRIE as a dictionary."""

    # Begin dictionary
    fh.write("{")

    key_value_list = sorted(trie.items(), key=cmp_to_key(_trie_compare_keys))

    # key/value pair index
    i = 0

    for key, value in key_value_list:
        # Separate second, third, ... element with a ', '
        # from the element before
        if i > 0:
            fh.write(", ")

        # True is used as key for word entries
        if key is True:
            # The key/value pair represents a word entry

            # Write 'True' as key for the following word entry
            fh.write("True:\n")

            # Write a comment with the word represented by the word entry
            fh.write(f"# {word}\n")

            # Write the word entry itself
            fh.write(f"{repr(value)}\n")

        else:
            # | fh.write(f'DEBUG {key} -> {value}\n')
            fh.write(f"{repr(key)}: ")
            _write_trie_value(fh, value, word + key)
            # | fh.write(f'({i})')

        # Increment index
        i += 1

    # End dictionary
    fh.write("}")


def _write_trie_value(fh, value, word):
    """Write a trie VALUE as a dictionary."""

    if isinstance(value, dict):
        # Value is a subtrie
        _write_trie_dict(fh, value, word)

    else:
        fh.write("# DEBUG Not a dict\n")


# ==========================================================


def _write_trie_pretty(fh, trie):
    """Write TRIE to FH in pretty print format."""

    # Write variable name
    fh.write("CEDICT_trie = ")

    # Write the trie
    _pretty_print_trie(fh, trie)
    fh.write("\n")

    # Write an empty line
    fh.write("\n")


def pretty_print_trie(trie, file=None):
    """Pretty print the TRIE to the given FILE handle.  When no FILE
    handle is given, print to stdout.

    """

    # When no FILE is given
    # print to stdout
    if file is None:
        # Write to stdout
        import sys

        file = sys.stdout

    _pretty_print_trie(file, trie)

    # Flush the stream
    file.flush()


def _pretty_print_trie(fh, trie, indent=0):
    """Pretty print TRIE to the file represented by FH using the given
    INDENT."""

    # Open the dictionary
    print("{", end="", file=fh)

    i = 0
    for key, value in trie.items():
        if i > 0:
            print(",", end="", file=fh)
        print("", file=fh)

        print("    " * (indent + 1), end="", file=fh)
        if key is True:
            print(f"{key}: {repr(value)}", end="", file=fh)

        else:
            print(f"{repr(key)}: ", end="", file=fh)
            _pretty_print_trie(fh, value, indent + 1)

        i += 1

    # Print a newline
    # unless the dictionary is empty
    if i > 0:
        print("", file=fh)

    # Close the dictionary
    print("    " * indent + "}", end="", file=fh)
