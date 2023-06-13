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

"""src/glottai/cedict/pinyin.py:

Pinyin utilities.

"""

__author__ = "Dietrich Bollmann"
__email__ = "dietrich@newskylabs.net"
__copyright__ = "Copyright 2023 Dietrich Bollmann"
__license__ = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__ = "2020/04/15"


import re


def _tone_numbers_to_marks_vowel(vowel, tone):
    """Add a tone mark for the given TONE to VOWEL."""

    i = tone - 1
    if vowel == "a":
        return "āáǎàa"[i]

    elif vowel == "e":
        return "ēéěèe"[i]

    elif vowel == "i":
        return "īíǐìi"[i]

    elif vowel == "o":
        return "ōóǒòo"[i]

    elif vowel == "u":
        return "ūúǔùu"[i]

    elif vowel == "ü":
        return "ǖǘǚǜü"[i]

    elif vowel == "A":
        return "ĀÁǍÀA"[i]

    elif vowel == "E":
        return "ĒÉĚÈE"[i]

    elif vowel == "I":
        return "ĪÍǏÌI"[i]

    elif vowel == "O":
        return "ŌÓǑÒO"[i]

    elif vowel == "U":
        return "ŪÚǓÙU"[i]

    elif vowel == "Ü":
        return "ǕǗǙǛÜ"[i]

    else:
        return vowel


def _tone_numbers_to_marks_vowels(vowels, tone):
    """Add tone mark for TONE to the given vowels.

    The rules implemented in this function have been taken from:

    - Where do the tone marks go?
      http://www.pinyin.info/rules/where.html

    Where do the tone marks go?
    ===========================

    Tone marks in Hanyu Pinyin always go over vowels, not
    consonants. But even those familiar with Hanyu Pinyin are often
    uncertain about which in a string of vowels takes the tone
    mark. If, for example, you are given "huai4" -- is it hùai, huài,
    or huaì? (Answer: the second choice.)

    Fortunately there are no ambiguities to worry about, even where
    there are several vowels in a row. Various complicated rules
    explain the placement. Fortunately, in application they boil down
    to a few very simple guidelines:

    - A and e trump all other vowels and always take the tone
      mark. There are no Mandarin syllables in Hanyu Pinyin that
      contain both a and e.
    - In the combination ou, o takes the mark.
    - In all other cases, the final vowel takes the mark.

    The possible vowel combinations are listed below, with the vowel
    that receives the tone marked as second tone.

    X |   a    e    i    o    u    ü
    --+-----------------------------
    a |             ái   áo
    e |             éi
    i | iá,iáo ié        ió   iú
    o |                       óu
    u | uá,uái ué   uí   uó
    ü |        üé

    Note: Early versions of Hanyu Pinyin also used ê. But since it
    never was combined with other vowels it is not included here. (It
    has since been supplanted by ei.)

    """

    if len(vowels) == 1:
        vowels = _tone_numbers_to_marks_vowel(vowels, tone)

    elif "a" in vowels:
        # A and e trump all other vowels and always take the tone
        # mark. There are no Mandarin syllables in Hanyu Pinyin that
        # contain both a and e.
        i = vowels.find("a")
        pre = vowels[:i]
        vowel = _tone_numbers_to_marks_vowel(vowels[i], tone)
        post = vowels[i + 1 :]
        vowels = pre + vowel + post

    elif "e" in vowels:
        # A and e trump all other vowels and always take the tone
        # mark. There are no Mandarin syllables in Hanyu Pinyin that
        # contain both a and e.
        i = vowels.find("e")
        pre = vowels[:i]
        vowel = _tone_numbers_to_marks_vowel(vowels[i], tone)
        post = vowels[i + 1 :]
        vowels = pre + vowel + post

    elif "ou" == vowels:
        # In the combination ou, o takes the mark.
        vowels = _tone_numbers_to_marks_vowel("o", tone) + "u"

    elif "uo" == vowels:
        # In the combination uo, o takes the mark.
        vowels = "u" + _tone_numbers_to_marks_vowel("o", tone)

    else:
        # In all other cases, the final vowel takes the mark.
        pre = vowels[:-1]
        last = _tone_numbers_to_marks_vowel(vowels[-1], tone)
        vowels = pre + last

    return vowels


# Regular expression
_tone_numbers_to_marks_syllable_regex = re.compile(
    "^([^aeiouü]*)([aeiouü]+)([^12345]*)([12345])(.*)", re.UNICODE
)


def tone_numbers_to_marks_syllable(syllable):
    # Allow for 'ü' to be written as 'u:'
    syllable = syllable.replace("u:", "ü")

    # Analyse syllable
    result = _tone_numbers_to_marks_syllable_regex.match(syllable)

    if result:
        # The parsed groups
        pre = result.group(1)
        vowels = result.group(2)
        post = result.group(3)
        tone = result.group(4)

        # Convert the tone to an integer
        tone = int(tone)

        # Apply the tone mark to the vowels
        vowels = _tone_numbers_to_marks_vowels(vowels, tone)

        # Assemble the converted syllable
        syllable = pre + vowels + post

    return syllable


def tone_numbers_to_marks(word):
    """
    Tone numbers to tone marks.

    Example:

    'jiao1 peng2 you5' -> 'jiāo péng you'
    """

    # 'jiao1 peng2 you5' -> ['jiao1', 'peng2', 'you5']
    syllables = word.split()

    # ['jiao1', 'peng2', 'you5'] -> ['jiāo', 'péng', 'you']
    syllables = [
        tone_numbers_to_marks_syllable(syllable) for syllable in syllables
    ]

    # ['jiāo', 'péng', 'you'] -> 'jiāo péng you'
    word = " ".join(syllables)

    return word


def tone_numbers_to_marks_string(string):
    """
    Tone numbers to tone marks.

    Example:

    Original string with tone numbers:
      "[Hui4 zhou1]; Baoshan 保山[Bao3 shan1]; Luzhou city 泸州市[Lu2 zhou1 shi4]."

    Result string with tone marks:
      "[Huì zhōu]; Baoshan 保山[Bǎo shān]; Luzhou city 泸州市[Lú zhōu shì]."

    """

    # Is there a '[Pin1 yin1]' section in string?
    beg = string.find("[")
    end = string.find("]")

    # When not, return string as it is
    if beg < 0 or end < 0 or end < beg:
        return string

    # When there is a '[Pin1 yin1]' section in string,
    # convert it to tone mark representation
    # And call funtion recursively with the rest of the string.

    # Dissect string into prefix, pinyin, postifix
    pre = string[:beg]
    pinyinN = string[beg + 1 : end]
    restN = string[end + 1 :]

    # Convert pinyin sectino to tone mark representation
    pinyin = tone_numbers_to_marks(pinyinN)

    # Recursively convert the rest of the string to tone mark representation
    rest = tone_numbers_to_marks_string(restN)

    # Reassemble the string
    return "{}[{}]{}".format(pre, pinyin, rest)
