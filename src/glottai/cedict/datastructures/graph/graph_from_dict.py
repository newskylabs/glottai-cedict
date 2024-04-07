# ==========================================================
# Copyright 2024 Dietrich Bollmann
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

"""src/glottai/cedict/datastructures/graph/graph_from_dict.py:

Instantiate a Vertex graph object from a dictionary.

"""


__author__ = "Dietrich Bollmann"
__email__ = "dietrich@newskylabs.net"
__copyright__ = "Copyright 2024 Dietrich Bollmann"
__license__ = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__ = "2024/04/07"


from .graph import GraphException, Vertex


class GraphFromDictException(GraphException):
    pass


def graph_from_dict(dic):
    """Instantiate a Vertex graph from 'dic'."""

    if not isinstance(dic, dict):
        msg = (
            "graph_from_dict() can only be applied to instances of dict - "
            f"but {dic} is of type {type(dic)}!"
        )
        raise GraphFromDictException(msg)

    seen = {}

    root = Vertex()
    seen[id(dic)] = root

    _graph_from_dict(root, dic, seen)

    return root


def _graph_from_dict(source_vertex, dic, seen):
    """ """

    to_convert = []
    for key, value in dic.items():
        if key is True:
            # Connect to a value
            source_vertex.connect(key, value)

        elif isinstance(value, dict):
            # Convert to Vertex graph

            # Has the dict been seen and processed already?
            if id(value) in seen:
                print("seen", id(dic), source_vertex)
                target_vertex = seen[id(value)]

            else:
                print("NOT seen", id(dic))
                target_vertex = Vertex()
                seen[id(value)] = target_vertex
                to_convert.append((target_vertex, value))

            source_vertex.connect(key, target_vertex)

        else:
            msg = (
                "Expected either an arbitrary key with a dictionary as value or "
                "True as key or with an arbitrary value - "
                f"but got the key {repr(key)} with the value {repr(value)}!"
            )
            raise GraphFromDictException(msg)

    for vertex, dic in to_convert:
        _graph_from_dict(vertex, dic, seen)
