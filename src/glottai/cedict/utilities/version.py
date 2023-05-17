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

"""src/glottai/cedict/utilities/version.py:

Cedict version utilities.

"""

__author__ = "Dietrich Bollmann"
__email__ = "dietrich@newskylabs.net"
__copyright__ = "Copyright 2023 Dietrich Bollmann"
__license__ = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__ = "2023/03/24"


import sys

from glottai.cedict.utilities.cedict import get_local_cedict_version
from glottai.cedict.utilities.format import format_UTC_date_for_humans
from glottai.cedict.utilities.paths import get_package_dir


def get_version() -> str:
    """
    Return the cedict version, e.g.
    "2023.3.24" or "2023.3.24+editable".
    """
    from importlib.metadata import version

    package_name = "glottai-cedict"
    return version(package_name)


def get_python_version() -> str:
    """
    Return the version of the current Python as a string, e.g.
    "Python 3.9.2".
    """
    version = sys.version_info
    version_str = f"Python {version.major}.{version.minor}.{version.micro}"
    return version_str


def get_CC_CEDICT_version() -> str:
    """
    Return the version of the installed CC-CEDICT dictionary file, e.g.
    "CC-CEDICT 2023/05/14 06:17".
    """

    # Get the local CC-CEDICT version
    cedict_version_local = get_local_cedict_version()

    # Format human readable
    if cedict_version_local is None:
        cedict_version_local = "not installed"

    else:
        cedict_version_local = format_UTC_date_for_humans(cedict_version_local)

    return f"CC-CEDICT {cedict_version_local}"


def get_version_long() -> str:
    """Get the current cedict version, e.g.
    "2023.3.24+editable from /some/path/cedict \
    (Python 3.9.2, CC-CEDICT 2023/05/14 06:17)".
    """

    version_long = "{} from {} ({}, {})".format(
        get_version(),
        get_package_dir(),
        get_python_version(),
        get_CC_CEDICT_version(),
    )

    return version_long
