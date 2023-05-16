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

"""src/glottai/cedict/utilities/paths.py:

Path utilities.

"""

__author__ = "Dietrich Bollmann"
__email__ = "dietrich@newskylabs.net"
__copyright__ = "Copyright 2023 Dietrich Bollmann"
__license__ = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__ = "2023/04/10"


import os
from pathlib import Path


def get_package_dir() -> str:
    """
    Return the directory of the glottai.cedict package.
    """
    this_file = Path(__file__)
    this_dir = this_file.parent
    package_dir = this_dir.parent
    return package_dir


def get_cedict_trie_package_dir():
    """Get the directory of the CEDICT trie files."""
    package_dir = get_package_dir()
    cedict_trie_package_dir = package_dir / "cedict"
    return cedict_trie_package_dir


def get_default_settings_file():
    """Get the file with the default settings."""
    package_dir = get_package_dir()
    default_settings_file = package_dir / "default_settings.toml"
    return default_settings_file


def get_settings_dir():
    """Get the directory where the cedict settings file is stored."""

    settings_dir = Path("~/.cedict").expanduser()

    return settings_dir


def get_settings_file():
    """Get the settings file."""

    # Get the directory where the cedict settings file is stored.
    settings_dir = get_settings_dir()

    # Calculate the user settings file
    settings_file = settings_dir / "settings.toml"

    return settings_file


def get_material_dir():
    """Get the directory where the cedict materials are stored."""

    package_dir = get_package_dir()
    material_dir = package_dir / "material"
    return material_dir


def get_settings_file_template():
    """Get the settings file template."""
    material_dir = get_material_dir()
    settings_file_template = material_dir / ".cedict" / "settings.toml"
    return settings_file_template
