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

"""src/glottai/cedict/utilities/format.py:

Formatting utilities.

"""

from glottai.cedict.utilities.cedict import read_cedict_variables


def format_UTC_date_for_humans(date_utc):
    """Format the UTC date for humans."""

    # Return the formatted date
    return date_utc.strftime("%Y/%m/%d %H:%M")


def format_UTC_date_as_file_extension(date_str):
    """Reformat the time stamp from the CEDICT header
    to a string which can be used in the backup file name.

    Example:

    '2022-11-29T02:38:09Z' -> 2022-11-29.02-38-09

    Note:

    The postfix 'Z' indicates that that time is UTC (zero hour offset).

    """

    from dateutil.parser import isoparse
    import pytz

    # Parse the date string from the CEDICT header
    date = isoparse(date_str)

    # Convert it to UTC
    date_utc = date.astimezone(pytz.UTC)

    # Format it as time stamp
    # | timestamp = date_utc.strftime("%Y-%m-%d.%H-%M-%S.%Z")
    timestamp = date_utc.strftime("%Y-%m-%d.%H-%M-%S")

    # Return the time stamp
    return timestamp


def format_backup_extension(cedict_file):
    """Get the DATE variable from the CC-CEDICT file variable section,
    format it as a backup extension and return it.

    """

    # Read the variable section of the cedict file
    variables = read_cedict_variables(cedict_file)
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

    # Reformat the DATE to be usable as timestamp in the file name
    date_str = variables["date"]
    backup_extension = format_UTC_date_as_file_extension(date_str)

    return backup_extension
