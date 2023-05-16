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

"""src/glottai/cedict/utilities/cedict.py:

CC-CEDICT utilities.

"""

import re
import requests
from pathlib import Path
from glottai.cedict.settings import settings


def _is_header_line(line):
    """True when LINE starts with the prefix '#! '; False otherwise."""
    return line.startswith("#! ")


def _readline(fh, binary=False):
    line = fh.readline()

    if binary:
        line = line.decode("utf-8")

    # | print('DEBUG line:', line)

    return line


def read_cedict_variables(cedict_filename):
    """Read the variables in the header of the cedict file.

    When CEDICT_FILENAME does not exist, None is returned.

    Example:

    CC-CEDICT file:
    --
    # CC-CEDICT
    # Community maintained free Chinese-English dictionary.
    #
    # ...snip...
    #
    #
    #! version=1
    #! subversion=0
    #! format=ts
    #! charset=UTF-8
    #! entries=121367
    #! publisher=MDBG
    #! license=https://creativecommons.org/licenses/by-sa/4.0/
    #! date=2022-11-29T02:38:09Z
    #! time=1669689489
    % % [pa1] /percent (Tw)/
    ...snip...
    --

    Resulting variable dir: {
        'version':     '1',
        'subversion':  '0',
        'format':      'ts',
        'charset':     'UTF-8',
        'entries':     '121367',
        'publisher':   'MDBG',
        'license':     'https://creativecommons.org/licenses/by-sa/4.0/',
        'date':        '2022-11-29T02:38:09Z',
        'time':        '1669689489',
    }

    """

    # When the cedict file does not exist
    # return None
    if not cedict_filename.is_file():
        return None

    if str(cedict_filename).endswith(".gz"):
        import gzip

        with gzip.open(cedict_filename, "rb") as fh:
            return _read_cedict_variables_fh(fh, binary=True)

    else:
        with open(cedict_filename, "r") as fh:
            return _read_cedict_variables_fh(fh, binary=False)


def _read_cedict_variables_fh(cedict_fh, binary=False):
    """Read the variables in the header of the cedict file.

    Example:

    CC-CEDICT file:
    --
    # CC-CEDICT
    # Community maintained free Chinese-English dictionary.
    #
    # ...snip...
    #
    #
    #! version=1
    #! subversion=0
    #! format=ts
    #! charset=UTF-8
    #! entries=121367
    #! publisher=MDBG
    #! license=https://creativecommons.org/licenses/by-sa/4.0/
    #! date=2022-11-29T02:38:09Z
    #! time=1669689489
    % % [pa1] /percent (Tw)/
    ...snip...
    --

    Resulting variable dir: {
        'version':     '1',
        'subversion':  '0',
        'format':      'ts',
        'charset':     'UTF-8',
        'entries':     '121367',
        'publisher':   'MDBG',
        'license':     'https://creativecommons.org/licenses/by-sa/4.0/',
        'date':        '2022-11-29T02:38:09Z',
        'time':        '1669689489',
    }

    """

    # Get first line from file
    line = _readline(cedict_fh, binary=binary)

    # Skip all lines before the variable section
    while not _is_header_line(line):
        # Read next line
        line = _readline(cedict_fh, binary=binary)

    # Read all variable section lines
    # and extract the variables.
    # Varialbe lines are lines of the form '#! variable=value'.
    # The first non-varialbe line ends the variable section.
    variables = {}
    while _is_header_line(line):
        # Get rid of prefix '#! '
        line = line[3:]

        # Get read of leading and trailing whitespace
        line = line.strip()

        # Split variable name and value
        name, value = line.split("=")

        # Store variable
        variables[name] = value

        # Read next line
        line = _readline(cedict_fh, binary=binary)

    # Return the variables
    return variables


def get_repository_cedict_version():
    """Get the current CC-CEDICT version (timestamp) from the repository."""

    # Get the URL of the CC-CEDICT hompage
    # and the regular expression necessary to extract the timestamp
    # from the CC-CEDICT hompage.
    cedict_homepage_url = settings.get_cedict_homepage_url()
    cedict_version_regex = settings.get_version_regex()
    # | print('DEBUG cedict_homepage_url: ', cedict_homepage_url)
    # | print('DEBUG cedict_version_regex:', cedict_version_regex)

    # Get the content of the homepage
    response = requests.get(cedict_homepage_url)
    # | print('DEBUG response:', dir(response))
    # | print('DEBUG response.content:', response.content)

    # Decode the content of the homepage
    content = response.content.decode("utf-8")

    # Extract the current CC-CEDICT timestamp from its homepage
    m = re.search(cedict_version_regex, content)
    timestamp = m.group(1) if m else None
    # | print('DEBUG timestamp:', timestamp)

    from dateutil import parser
    import pytz

    # Parse the timestamp
    date = parser.parse(timestamp)
    # | print('DEBUG date:', date)

    # Convert it to UTC
    date_utc = date.astimezone(pytz.UTC)
    # | print('DEBUG date_utc:', date_utc)

    # Return the time stamp
    return date_utc


def get_local_cedict_version():
    """Get the current version (timestamp) of the local CC-CEDICT copy.

    When there is no local CC-CEDICT copy, None is returned.

    """

    # Get the path of the local CC-CEDICT copy
    cedict_file = settings.get_cedict_file()
    cedict_file = Path(cedict_file).expanduser()
    # | print('DEBUG cedict_file:', cedict_file)

    # Read the variable section of the cedict file
    variables = read_cedict_variables(cedict_file)
    # | print('DEBUG local CC-CEDICT variables:', variables)
    # variables: {
    #     'version':     '1',
    #     'subversion':  '0',
    #     'format':      'ts',
    #     'charset':     'UTF-8',
    #     'entries':     '121367',
    #     'publisher':   'MDBG',
    #     'license':     'https://creativecommons.org/licenses/by-sa/4.0/',
    #     'date':        '2022-11-29T02:38:09Z',
    #     'time':        '1669689489',
    # }

    # When there is no local CC-CEDICT copy
    # return None
    if variables is None:
        return None

    # Get the CC-CEDICT timestamp
    date_str = variables.get("date", None)
    # | print('DEBUG date_str:', date_str)

    from dateutil.parser import isoparse
    import pytz

    # Parse the date string from the CEDICT header
    date = isoparse(date_str)
    # | print('DEBUG date:', date)

    # Convert it to UTC
    date_utc = date.astimezone(pytz.UTC)
    # | print('DEBUG date_utc:', date_utc)

    # Return the time stamp
    return date_utc
