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

"""tests/glottai/cedict/datastructures/graph/test_graph_from_dict.py:

Unit tests for graph_from_dict(),
a function to instantiate a Vertex graph object from a dictionary.

Run with:

pytest tests/glottai/cedict/datastructures/graph/test_graph_from_dict.py

"""


__author__ = "Dietrich Bollmann"
__email__ = "dietrich@newskylabs.net"
__copyright__ = "Copyright 2024 Dietrich Bollmann"
__license__ = "Apache License 2.0, http://www.apache.org/licenses/LICENSE-2.0"
__date__ = "2024/04/07"


import pytest

from glottai.cedict.datastructures.graph.graph import Vertex
from glottai.cedict.datastructures.graph.graph_from_dict import (
    GraphFromDictException,
    graph_from_dict,
)


# ==========================================================
# Test utilities
# ----------------------------------------------------------


def tprint(name, root):
    print(f">>> {name}:")
    print("")
    print(f">>> {name}.pretty_print():")
    root.pretty_print()
    print("")
    print(f">>> {name}.print_connection_graph():")
    root.print_connection_graph()
    print("")
    print(f">>> {name}.print_connections():")
    root.print_connections()
    print("")
    print(f">>> {name}.get_connections():")
    print(root.get_connections())
    print("")


# ==========================================================
# graph_from_dict(dic)
# ----------------------------------------------------------


def test_graph_from_non_dict000():
    """

    pytest tests/glottai/cedict/datastructures/graph/test_graph_from_dict.py::test_graph_from_non_dict000

    """

    arg = 123
    with pytest.raises(GraphFromDictException) as e:
        graph_from_dict(arg)

    error_msg = str(e.value)

    print(f'error_msg: "{error_msg}"')

    assert error_msg == (
        "graph_from_dict() can only be applied to instances of dict - " f"but {arg} is of type {type(arg)}!"
    )


def test_graph_from_illformed_dict000():
    """

    pytest tests/glottai/cedict/datastructures/graph/test_graph_from_dict.py::test_graph_from_illformed_dict000

    """

    dic = {"a": True}
    with pytest.raises(GraphFromDictException) as e:
        graph_from_dict(dic)

    error_msg = str(e.value)

    print(f'error_msg: "{error_msg}"')

    assert error_msg == (
        "Expected either an arbitrary key with a dictionary as value or "
        "True as key or with an arbitrary value - "
        "but got the key 'a' with the value True!"
    )


def test_graph_from_dict000():
    """

    pytest tests/glottai/cedict/datastructures/graph/test_graph_from_dict.py::test_graph_from_dict000

    """

    # Reset Vertex index
    Vertex.vertex_index = 0

    dic = {}
    graph = graph_from_dict(dic)
    tprint("graph", graph)

    assert graph.get_connections() == [{"index": 0, "in": [], "out": []}]


def graph_from_dict_testfunc(dic, expected_connections):
    """
    Testfunction for graph_from_dict().
    """

    # Reset Vertex index
    Vertex.vertex_index = 0

    graph = graph_from_dict(dic)
    tprint("graph", graph)

    assert graph.get_connections() == expected_connections


def test_graph_from_dict010():
    """

    pytest tests/glottai/cedict/datastructures/graph/test_graph_from_dict.py::test_graph_from_dict010

    """

    dic = {}
    con = [{"index": 0, "in": [], "out": []}]
    graph_from_dict_testfunc(dic, con)


def test_graph_from_dict020():
    """

    pytest tests/glottai/cedict/datastructures/graph/test_graph_from_dict.py::test_graph_from_dict020

    """

    dic = {"a": {}, "b": {}, "c": {}}
    con = [
        {"index": 0, "in": [], "out": [(0, "a", 1), (0, "b", 2), (0, "c", 3)]},
        {"index": 1, "in": [(0, "a", 1)], "out": []},
        {"index": 2, "in": [(0, "b", 2)], "out": []},
        {"index": 3, "in": [(0, "c", 3)], "out": []},
    ]
    graph_from_dict_testfunc(dic, con)


def test_graph_from_dict030():
    """

    pytest tests/glottai/cedict/datastructures/graph/test_graph_from_dict.py::test_graph_from_dict030

    """

    dic = {}
    dic["a"] = dic
    con = [{"index": 0, "in": [(0, "a", 0)], "out": [(0, "a", 0)]}]
    graph_from_dict_testfunc(dic, con)


def test_graph_from_dict040():
    """

    pytest tests/glottai/cedict/datastructures/graph/test_graph_from_dict.py::test_graph_from_dict040

    """

    d0 = {}
    d1 = {}
    d2 = {}
    d3 = {}
    d4 = {}
    d5 = {}
    d6 = {}

    d0["a"] = d1
    d0["b"] = d2
    d0["c"] = d3

    d1["a"] = d4
    d1["b"] = d5
    d1["c"] = d6

    d2["a"] = d4
    d2["b"] = d5
    d2["c"] = d6

    d3["a"] = d4
    d3["b"] = d5
    d3["c"] = d6

    d4["a"] = d0
    d4["b"] = d0
    d4["c"] = d0

    d5["a"] = d0
    d5["b"] = d0
    d5["c"] = d0

    d6["a"] = d0
    d6["b"] = d0
    d6["c"] = d0

    con = [
        {
            "index": 0,
            "in": [
                (4, "a", 0),
                (4, "b", 0),
                (4, "c", 0),
                (5, "a", 0),
                (5, "b", 0),
                (5, "c", 0),
                (6, "a", 0),
                (6, "b", 0),
                (6, "c", 0),
            ],
            "out": [(0, "a", 1), (0, "b", 2), (0, "c", 3)],
        },
        {"index": 1, "in": [(0, "a", 1)], "out": [(1, "a", 4), (1, "b", 5), (1, "c", 6)]},
        {"index": 2, "in": [(0, "b", 2)], "out": [(2, "a", 4), (2, "b", 5), (2, "c", 6)]},
        {"index": 3, "in": [(0, "c", 3)], "out": [(3, "a", 4), (3, "b", 5), (3, "c", 6)]},
        {
            "index": 4,
            "in": [(1, "a", 4), (2, "a", 4), (3, "a", 4)],
            "out": [(4, "a", 0), (4, "b", 0), (4, "c", 0)],
        },
        {
            "index": 5,
            "in": [(1, "b", 5), (2, "b", 5), (3, "b", 5)],
            "out": [(5, "a", 0), (5, "b", 0), (5, "c", 0)],
        },
        {
            "index": 6,
            "in": [(1, "c", 6), (2, "c", 6), (3, "c", 6)],
            "out": [(6, "a", 0), (6, "b", 0), (6, "c", 0)],
        },
    ]
    graph_from_dict_testfunc(d0, con)


def test_graph_from_dict100():
    """

    pytest tests/glottai/cedict/datastructures/graph/test_graph_from_dict.py::test_graph_from_dict100

    """

    dic = {True: 123}
    con = [{"index": 0, "in": [], "out": [(0, True, 123)]}]
    graph_from_dict_testfunc(dic, con)


def test_graph_from_dict110():
    """

    pytest tests/glottai/cedict/datastructures/graph/test_graph_from_dict.py::test_graph_from_dict110

    """

    dic = {True: {"a": {"dictionary": {"as": "value"}}}}
    con = [{"index": 0, "in": [], "out": [(0, True, {"a": {"dictionary": {"as": "value"}}})]}]
    graph_from_dict_testfunc(dic, con)


def test_graph_from_dict120():
    """

    pytest tests/glottai/cedict/datastructures/graph/test_graph_from_dict.py::test_graph_from_dict120

    """

    dic = {"a": {"b": {"c": {True: "value"}}}}
    con = [
        {"index": 0, "in": [], "out": [(0, "a", 1)]},
        {"index": 1, "in": [(0, "a", 1)], "out": [(1, "b", 2)]},
        {"index": 2, "in": [(1, "b", 2)], "out": [(2, "c", 3)]},
        {"index": 3, "in": [(2, "c", 3)], "out": [(3, True, "value")]},
    ]
    graph_from_dict_testfunc(dic, con)


def test_graph_from_dict130():
    """

    pytest tests/glottai/cedict/datastructures/graph/test_graph_from_dict.py::test_graph_from_dict130

    """

    dic = {
        True: 1,
        "a": {True: 1.0, "a": {True: True}, "b": {True: False}},
        "b": {True: "foo", "a": {True: ["bar"]}, "b": {True: {"baz": "qux"}}},
    }
    dic["c"] = dic
    dic["a"]["c"] = dic
    dic["b"]["c"] = dic
    dic["a"]["a"]["c"] = dic
    dic["a"]["b"]["c"] = dic
    dic["b"]["a"]["c"] = dic
    dic["b"]["b"]["c"] = dic

    con = [
        {
            "index": 0,
            "in": [
                (0, "c", 0),
                (1, "c", 0),
                (2, "c", 0),
                (3, "c", 0),
                (4, "c", 0),
                (5, "c", 0),
                (6, "c", 0),
            ],
            "out": [(0, True, 1), (0, "a", 1), (0, "b", 2), (0, "c", 0)],
        },
        {
            "index": 1,
            "in": [(0, "a", 1)],
            "out": [(1, True, 1.0), (1, "a", 3), (1, "b", 4), (1, "c", 0)],
        },
        {
            "index": 2,
            "in": [(0, "b", 2)],
            "out": [(2, True, "foo"), (2, "a", 5), (2, "b", 6), (2, "c", 0)],
        },
        {"index": 3, "in": [(1, "a", 3)], "out": [(3, True, True), (3, "c", 0)]},
        {"index": 4, "in": [(1, "b", 4)], "out": [(4, True, False), (4, "c", 0)]},
        {"index": 5, "in": [(2, "a", 5)], "out": [(5, True, ["bar"]), (5, "c", 0)]},
        {"index": 6, "in": [(2, "b", 6)], "out": [(6, True, {"baz": "qux"}), (6, "c", 0)]},
    ]

    graph_from_dict_testfunc(dic, con)
