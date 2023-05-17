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

"""src/glottai/cedict/utilities/diff.py:

Print the differences between the entries of two CC-CEDICT files.

"""


def _next_line(fh):
    """Get the next non-comment line."""

    while True:
        line = fh.readline()

        # if line is empty
        # end of file is reached
        if not line:
            return None

        if not line.startswith("#"):
            # Return line with trailing newlines removed
            return line.rstrip("\n")


def _get_entry(entry):
    """Get the (traditional) word represented by the entry.

    Example:

    entry: '伸縮性 伸缩性 [shen1 suo1 xing4] /flexibility/'
    word:  '伸縮性'

    """

    # The word corresponds to the first characters delimited by a blank
    # Find the index of the blank
    end = entry.find(" ")

    # Return None when no blank was found
    if end < 0:
        return None

    # Extract the word
    word = entry[:end]

    # And return it
    return word


def diff(file1, file2):
    """Compare the CC-CEDICT FILE1 with the CC-CEDICT FILE2 line by line.

    The FILE1 is supposed to be an older CC-CEDICT version compared to FILE2.

    Example:

    old file:
    --
    aaa aaa entry for aaa
    ccc ccc eliminated entry
    ddd ddd old entry for ddd
    --

    new file:
    --
    aaa aaa entry for aaa
    bbb bbb added entry for bbb
    ddd ddd new entry for ddd
    --

    diff:
    --

    + bbb bbb added entry for bbb

    - ccc ccc eliminated entry

    < ddd ddd old entry for ddd
    > ddd ddd new entry for ddd

    --

    """

    with open(file1, "r") as fh1:
        with open(file2, "r") as fh2:
            # Start with the first entries of both files
            line1 = _next_line(fh1)
            line2 = _next_line(fh2)

            print("")
            while True:
                # Compare the lines
                if line1 == line2:
                    # line1 and line2 are None
                    # both files have been consumed
                    # exit the loop
                    if line1 is None:
                        break

                    # When the lines are identical
                    # the corresponding word entry is still the same

                    # Get next non-comment lines from files
                    line1 = _next_line(fh1)
                    line2 = _next_line(fh2)

                    # and continue with them
                    continue

                # When the lines differ...
                else:  # line1 != line2
                    if line2 is None:
                        # The entry for word1 has been eliminated
                        print("-", line1)
                        print("")

                        # Get next non-comment line from file1
                        line1 = _next_line(fh1)

                        # and continue with the new line1 and the old line2
                        continue

                    if line1 is None:
                        # An entry for word2 has been newly added
                        print("+", line2)
                        print("")

                        # Get next non-comment line from file2
                        line2 = _next_line(fh2)

                        # and continue with the old line1 and the new line2
                        continue

                    # Get the (traditional) words represented by the entries
                    word1 = _get_entry(line1)
                    word2 = _get_entry(line2)

                    if word2 is None or word1 < word2:
                        # The entry for word1 has been eliminated
                        print("-", line1)
                        print("")

                        # Get next non-comment line from file1
                        line1 = _next_line(fh1)

                        # and continue with the new line1 and the old line2
                        continue

                    elif word1 > word2:
                        # An entry for word2 has been newly added
                        print("+", line2)
                        print("")

                        # Get next non-comment line from file2
                        line2 = _next_line(fh2)

                        # and continue with the old line1 and the new line2
                        continue

                    else:  # word1 == word2
                        # The entry for the given word has been edited
                        print("<", line1)
                        print(">", line2)
                        print("")

                        # Get next non-comment lines from files
                        line1 = _next_line(fh1)
                        line2 = _next_line(fh2)

                        # and continue with them
                        continue
