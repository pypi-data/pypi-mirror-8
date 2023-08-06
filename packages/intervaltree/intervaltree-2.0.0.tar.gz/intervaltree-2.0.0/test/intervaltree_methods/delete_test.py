"""
intervaltree: A mutable, self-balancing interval tree for Python 2 and 3.
Queries may be by point, by range overlap, or by range envelopment.

Test module: IntervalTree, Basic deletion methods

Copyright 2013-2014 Chaim-Leib Halbert

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import absolute_import
from intervaltree import Interval, IntervalTree
import pytest
from test.intervaltrees import trees, sdata
try:
    import cPickle as pickle
except ImportError:
    import pickle


def test_delete():
    t = trees['ivs1']()
    try:
        t.remove(Interval(1, 3, "Doesn't exist"))
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")

    try:
        t.remove(Interval(500, 1000, "Doesn't exist"))
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")

    orig = t.print_structure(True)
    t.discard(Interval(1, 3, "Doesn't exist"))
    t.discard(Interval(500, 1000, "Doesn't exist"))
    assert orig == t.print_structure(True)

    assert sdata(t[14]) == set(['[8,15)', '[14,15)'])
    t.remove(Interval(14, 15, '[14,15)'))
    assert sdata(t[14]) == set(['[8,15)'])
    t.verify()

    t.discard(Interval(8, 15, '[8,15)'))
    assert sdata(t[14]) == set()
    t.verify()

    assert t[5]
    t.remove_overlap(5)
    t.verify()
    assert not t[5]


def test_emptying_iteration():
    t = trees['ivs1']()

    for iv in sorted(iter(t)):
        t.remove(iv)
        t.verify()
    assert len(t) == 0
    assert t.is_empty()
    assert not t


def test_emptying_clear():
    t = trees['ivs1']()
    assert t
    t.clear()
    assert len(t) == 0
    assert t.is_empty()
    assert not t

    # make sure emptying an empty tree does not crash
    t.clear()


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
