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

"""src/glottai/cedict/utilities/metadata.py:

Accessing package metadata.

"""

__author__ = "Dietrich Bollmann"
__email__ = "dietrich@newskylabs.net"
__copyright__ = "Copyright 2023 Dietrich Bollmann"
__license__ = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__ = "2023/03/24"


from importlib.metadata import metadata


class Metadata:
    def __init__(self, package_name):
        self.package_name = package_name

        # Get the metadata object
        # The metadata object is of type email.message.Message
        self.metadata_msg = metadata(package_name)

        # Parse the metadata into a dictionary format
        self.metadata = self.parse_metadata_msg(self.metadata_msg)

    def parse_metadata_msg(self, metadata_msg):
        """DEBUG the information returned by metadata()."""

        # The metadata object is of type email.message.Message

        # Get a list of the names of all fields
        # with doubles
        all_field_names = metadata_msg.keys()

        # Remove doubles
        field_names = []
        for field_name in all_field_names:
            if field_name not in field_names:
                field_names.append(field_name)

        # Parse the metadata into a dictionary
        metadata = {}
        for field_name in field_names:
            all_values = metadata_msg.get_all(field_name, failobj=None)
            number_of_values = len(all_values)

            # DEBUG
            # | print(f'DEBUG field_name: "{field_name}": {all_values}')

            if field_name == "Project-URL":
                metadata[field_name] = self.parse_project_urls(all_values)

            elif field_name == "Keywords":
                metadata[field_name] = self.parse_keywords(all_values[0])

            elif number_of_values == 1:
                metadata[field_name] = all_values[0]

            elif number_of_values > 1:
                metadata[field_name] = all_values

        # The README.md
        # is stored as the "payload" of the email.message.Message object
        payload = self.metadata_msg.get_payload()
        metadata["readme"] = {"content": payload}
        if "Description-Content-Type" in metadata:
            metadata["readme"]["content-type"] = metadata[
                "Description-Content-Type"
            ]
            del metadata["Description-Content-Type"]

        return metadata

    def parse_project_urls(self, project_urls):
        """Parse project URLs.

        Example:

        ['Homepage, https://foo.bar/homepage',
         'Documentation, https://foo.bar/documentation',
         'Repository, https://foo.bar/repository',
         'Issues, https://foo.bar/issues']

        =>

        {'homepage':      'https://foo.bar/homepage',
         'documentation': 'https://foo.bar/documentation',
         'repository':    'https://foo.bar/repository',
         'issues':        'https://foo.bar/issues'}

        """

        project_url_dic = {}
        for project_url in project_urls:
            key, value = project_url.split(", ", 1)
            project_url_dic[key.lower()] = value

        return project_url_dic

    def parse_keywords(self, keywords):
        """Parse project keywords.

        Example:

        "foo bar baz" => ["foo", "bar", "baz"]

        """

        return keywords.split()

    def as_string(self):
        """Get the package metadata information flattened as a string."""
        return self.metadata_msg.as_string()

    def get(self, key, default=None):
        """Get the value for KEY from the package metadata."""

        return self.metadata.get(key, default)

    def get_project_urls(self):
        """Return the project URLs."""

        project_urls = self.get("Project-URL")
        return project_urls

    def get_documentation_url(self):
        """Return the URL of the documentation."""

        project_urls = self.get_project_urls()
        documentation_url = project_urls.get("documentation", None)
        return documentation_url

    def dump_as_string(self):
        """Dump the metadata as string."""
        print(self.as_string().strip())

    def dump_as_yaml(self):
        """Dump the metadata in yaml form."""

        metadata = self.metadata

        if metadata is not None:
            import yaml

            print(yaml.dump(metadata).strip())

    def dump(self):
        """Print some information about the package metadata."""

        print("============================================================")
        print("METADATA (flattened as a string):")
        print("------------------------------------------------------------")
        self.dump_as_string()
        print("============================================================")
        print("")

        print("============================================================")
        print("METADATA (parsed and printed in yaml format):")
        print("------------------------------------------------------------")
        self.dump_as_yaml()
        print("============================================================")


_metadata = None


def get_metadata():
    """
    Return the cedict version, e.g.
    "2023.3.24" or "2023.3.24+editable".
    """

    global _metadata

    if _metadata is None:
        package_name = "glottai-cedict"
        _metadata = Metadata(package_name)

    # DEBUG
    # _metadata.dump()

    return _metadata
