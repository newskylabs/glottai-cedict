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

"""src/glottai/cedict/settings.py:

Utilities to manage project settings.

"""

import errno
import os
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

from glottai.cedict.utilities.paths import (
    get_default_settings_file,
    get_settings_file,
)


def set_recursively(structure, path, value):
    """Set a value in a recursive structure."""

    path = path.split(".")
    lastkey = path.pop()

    for key in path:
        if key not in structure or not isinstance(structure[key], dict):
            structure[key] = {}
        structure = structure[key]

    structure[lastkey] = value


def get_recursively(structure, keychain):
    """Get a value from a recursive structure."""

    val = structure

    # Follow the key chain to recursively find the value
    for key in keychain.split("."):
        if isinstance(val, dict) and key in val:
            val = val[key]
        elif key.isdigit() and isinstance(val, list) and int(key) < len(val):
            val = val[int(key)]
        else:
            return None

    return val


class Settings:
    """A simple class to manage project settings"""

    def __init__(self, default_settings_file, user_settings_file):
        """ """
        self._default_settings_file = default_settings_file
        self._user_settings_file = user_settings_file

        self.load_settings()

    def load_settings(self):
        """ """
        default_settings_file = self._default_settings_file
        user_settings_file = self._user_settings_file

        # Throw an error
        # when no default_settings file has been given
        if default_settings_file is None:
            raise TypeError(
                errno.ENOENT, "A default settings file has to be given!"
            )

        # Throw an error
        # when the default_settings file does not exist
        if not os.path.isfile(default_settings_file):
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), default_settings_file
            )

        # Load the default settings
        default_settings = self.load_settings_file(default_settings_file)
        self._settings = default_settings

        if user_settings_file:
            # Merge in the user settings
            # and use them to overwrite the defaults
            self.merge_settings_file(user_settings_file)

    def merge_settings_file(self, settings_file):
        """Merge in the settings of the given file"""

        settings = self.load_settings_file(settings_file)
        if settings:
            self._settings = self.merge_settings(self._settings, settings)

    @staticmethod
    def load_settings_file(settings_file):
        """Load a yaml settings file"""

        if os.path.isfile(settings_file):
            with open(settings_file, mode="rb") as fh:
                return tomllib.load(fh)

        else:
            return None

    @staticmethod
    def merge_settings(defaults, overwrite):
        """Recursively merge 'overwrite' settings into the 'default' settings.

        In the case of settings which are defined in both, the settings
        given in 'overwrite' overwrite the 'default' settings.

        The function is destructive: the original values are reused and
        thereby manipulated by the function.

        Parameters
        ----------
        defaults
            The default settings.
        overwrite
            The overwrite settings.

        Returns
        -------
        The merged settings.

        """

        if isinstance(overwrite, dict) and isinstance(defaults, dict):
            # When overwrite is a dictionary
            # and defaults as well

            # Start from the defaults
            merged = defaults

            # And merge in the overwritten settings
            for key, value in overwrite.items():
                if key in defaults:
                    # Recursively merge the values of keys
                    # exising in both: defaults and overwrite
                    merged[key] = Settings.merge_settings(merged[key], value)

                else:
                    # Extend the settings with new settings
                    # only defined in the 'overwrite' settings
                    merged[key] = value

        else:
            # In all other cases the 'overwrite' settings
            # are used
            merged = overwrite

        return merged

    def get_settings(self):
        """Retrive the dictionary with all settings."""

        return self._settings

    def set(self, keychain, value):
        """Set a setting."""

        set_recursively(self._settings, keychain, value)

    def get(self, keychain):
        """Retrive a setting"""

        return get_recursively(self._settings, keychain)

    def get_cedict_url(self):
        """Get the URL of the current CC-CEDICT dictionary file."""

        cedict_url = settings.get("repository.cedict-url")

        return cedict_url

    def get_cedict_homepage_url(self):
        """Get the URL of the CC-CEDICT homepage."""

        cedict_homepage_url = settings.get("repository.homepage-url")

        return cedict_homepage_url

    def get_version_regex(self):
        """Get the regular expression to be used to extract the
        current CC-CEDICT version from the CC-CEDICT homepage.

        """

        cedict_version_regex = settings.get("repository.version-regex")

        return cedict_version_regex

    def get_cedict_dir(self):
        """Get the directory where the local CC-CEDICT dictionary
        files are stored.

        """

        # Get the cedict directory
        # i.e. the directory where the cedict files will be stored
        cedict_dir = settings.get("local.cedict-dir")

        # Expand the filename
        # Example: '~/.cedict' -> '/Users/<user-name>/.cedict'
        cedict_dir = Path(cedict_dir).expanduser()

        return cedict_dir

    def get_cedict_file(self):
        """Get the file path of the local copy of the CC-CEDICT file."""

        cedict_dir = self.get_cedict_dir()
        cedict_file = settings.get("local.cedict-file")
        cedict_file_path = cedict_dir / cedict_file

        return cedict_file_path

    def get_cedict_gz_file(self):
        """Get the file path of the local copy of the CC-CEDICT
        archive file.

        """

        cedict_dir = self.get_cedict_dir()
        cedict_gz_file = settings.get("local.cedict-gz-file")
        cedict_gz_file_path = cedict_dir / cedict_gz_file

        return cedict_gz_file_path

    def get_cedict_trie_traditional_file(self):
        """Get the file path of the CC-CEDICT trie for traditional hanzi."""

        cedict_dir = self.get_cedict_dir()
        cedict_trie_traditional_file = settings.get(
            "local.cedict-trie-traditional-file"
        )
        cedict_trie_traditional_file_path = (
            cedict_dir / cedict_trie_traditional_file
        )

        return cedict_trie_traditional_file_path

    def get_cedict_trie_simplified_file(self):
        """Get the file path of the CC-CEDICT trie for simplified hanzi."""

        cedict_dir = self.get_cedict_dir()
        cedict_trie_simplified_file = settings.get(
            "local.cedict-trie-simplified-file"
        )
        cedict_trie_simplified_file_path = (
            cedict_dir / cedict_trie_simplified_file
        )

        return cedict_trie_simplified_file_path

    def assert_hanzi_form(self, form):
        """Assert that FORM is either 'traditional' or 'simplified'."""

        if form in ["traditional", "simplified"]:
            return True

        else:
            # ERROR Unknown hanzi form - exiting
            print(f"ERROR Unknown hanzi form: {form}")
            print("Only 'traditional' or 'simplified' are defined.")
            sys.exit(1)

    def get_cedict_trie_file(self, form="traditional"):
        """Get the file path of the compiled CC-CEDICT trie file for
        simplified or traditional hanzi.

        Use the parameter 'form' with either 'traditional' (this is
        the default) or 'simplified' as value to get the respective
        version.

        """

        if form == "traditional":
            return self.get_cedict_trie_traditional_file()

        elif form == "simplified":
            return self.get_cedict_trie_simplified_file()

        else:
            # ERROR Unknown hanzi form - exiting
            print(f"ERROR Unknown hanzi form: {form}")
            print("Only 'traditional' or 'simplified' are defined.")
            sys.exit(1)

    def get_number_of_backups(self):
        """Get the number of CC-CEDICT backups which should be available."""

        number_of_backups = settings.get("local.number-of-backups")
        number_of_backups = int(number_of_backups)

        return number_of_backups

    def get_hanzi_default_form(self):
        """Get the hanzi default form."""

        hanzi_default_form = settings.get("defaults.form")

        # Assert that FORM is either 'traditional' or 'simplified'
        self.assert_hanzi_form(hanzi_default_form)

        return hanzi_default_form

    def get_formatting_columns_settings(self):
        """Get the settings controlling the formatting of CC-CEDICT
        entries and assert that it has an adequate value.

        Example of the 'formatting' setting:

        formatting:
          columns:
            indent:       2
            simplified:  10
            traditional: 12
            pinyin:      14
            senses:      60

        """

        # Required keys for the columns setting
        required_columns_settings = {
            "indent",
            "simplified",
            "traditional",
            "pinyin",
            "senses",
        }

        # Get the setting for 'formatting.columns'
        columns = settings.get("formatting.columns")

        # Assert that they are well-formed
        if (
            not isinstance(columns, dict)
            or set(columns.keys()) != required_columns_settings
        ):
            # ERROR message
            # to be used when the 'formatting.columns' setting
            # is not well-formed.
            error_msg = (
                "ERROR The setting 'formatting.columns' is not well-formed.\n"
                "It should specify values for the following keys:\n"
                "indent, simplified, traditional, pinyin, and senses.\n"
                "\n"
                "Example:\n"
                "\n"
                "formatting:\n"
                "  columns:\n"
                "    indent:       2\n"
                "    simplified:  10\n"
                "    traditional: 12\n"
                "    pinyin:      14\n"
                "    senses:      60\n"
                "\n"
            )

            # Print error message and exit
            print(error_msg)
            sys.exit(1)

        # The columns setting is wellformed
        # Return it
        return columns


def init_settings():
    # Use the global settings variable
    global settings

    # Calculate the path of the default settings file
    default_settings_file = get_default_settings_file()

    # Calculate the path of the user setting file
    user_settings_file = get_settings_file()

    # Settings
    # The settings are calculated by
    # overwriting the default settings with and the user settings
    settings = Settings(default_settings_file, user_settings_file)


# ==========================================================
# settings
# ----------------------------------------------------------

settings = None

init_settings()
