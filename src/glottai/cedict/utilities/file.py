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

"""src/glottai/cedict/utilities/file.py:

File utilities.

"""

import requests
from glottai.cedict.settings import settings


def download(url, path):
    """Download the file represented by URL and store it locally as
    PATH.  A progress bar is shown during the download.

    """

    from clint.textui import progress

    # Request the file represented by the url
    r = requests.get(url, stream=True)

    # Download data and write to local file
    # while showing a progress bar
    with open(path, "wb") as f:
        total_length = int(r.headers.get("content-length"))
        for chunk in progress.bar(
            r.iter_content(chunk_size=1024),
            expected_size=(total_length / 1024) + 1,
        ):
            if chunk:
                f.write(chunk)
                f.flush()


def gunzip(filename_gz, filename):
    """Gunzip FILENAME_GZ and store the unzipped data as FILENAME."""

    import gzip
    import shutil

    with gzip.open(filename_gz, "rb") as f_in:
        with open(filename, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)


def get_cedict_backup_files():
    """Get a list of the local CC-CEDICT backup files."""

    # Assemble glob pattern for listing CC-CEDICT backup files
    glob_pattern = settings.get_cedict_file()
    glob_pattern = str(glob_pattern)
    if glob_pattern.endswith(".txt"):
        glob_pattern = glob_pattern[:-4]
    glob_pattern += ".*.*.txt"

    # List CC-CEDICT backup files
    import glob

    backup_files = glob.glob(glob_pattern)

    # Sort the list
    backup_files.sort()

    # Return the list of backup files
    return backup_files


def get_last_backup_cedict_file():
    """Get the last backup file."""

    # Get the sorted list of backup files
    backup_files = get_cedict_backup_files()

    # When there are no backup files
    # return None
    if len(backup_files) == 0:
        return None

    # The last backup file is the last one in the sorted list
    # get and return it
    last_backup_file = backup_files[-1]

    # Return the last backup file
    return last_backup_file
