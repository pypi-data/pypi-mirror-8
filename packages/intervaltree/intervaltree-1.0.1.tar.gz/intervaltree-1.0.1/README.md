[![Build status badge][]][build status]

intervaltree
============

A mutable, self-balancing interval tree for Python 2 and 3. Queries may be by point, by range overlap, or by range envelopment.

This library was designed to allow tagging text and time intervals, where the intervals include the lower bound but not the upper bound.

Installing
----------

    pip install intervaltree

Features
--------

* Supports Python 2.6+ and Python 3.2+
* Initialize blank or from an iterable of `Intervals` in O(n * log n).
* Insertions

  * `tree[begin:end] = data`
  * `tree.add(interval)`
  * `tree.addi(begin, end, data)`
  * `tree.extend(list_of_interval_objs)`

* Deletions

  * `tree.remove(interval)`             (raises `ValueError` if not present)
  * `tree.discard(interval)`            (quiet if not present)
  * `tree.removei(begin, end, data)`    (short for `tree.remove(Interval(begin, end, data))`)
  * `tree.discardi(begin, end, data)`   (short for `tree.discard(Interval(begin, end, data))`)
  * `tree.remove_overlap(point)`
  * `tree.remove_overlap(begin, end)`   (removes all overlapping the range)
  * `tree.remove_envelop(begin, end)`   (removes all enveloped in the range)

* Overlap queries:

  * `tree[point]`
  * `tree[begin, end]`
  * `tree.search(point)`
  * `tree.search(begin, end)`

* Envelop queries:

  * `tree.search(begin, end, strict=True)`

* Membership queries:

  * `interval_obj in tree`              (this is fastest, O(1))
  * `tree.containsi(begin, end, data)`
  * `tree.overlaps(point)`
  * `tree.overlaps(begin, end)`

* Iterable:

  * `for interval_obj in tree:`
  * `tree.items()`

* Sizing:

  * `len(tree)`
  * `tree.is_empty()`
  * `not tree`
  * `tree.begin()`          (the `begin` coordinate of the leftmost interval)
  * `tree.end()`            (the `end` coordinate of the rightmost interval)

* Restructuring

  * `split_overlaps()`

* Copy- and typecast-able:

  * `IntervalTree(tree)`    (`Interval` objects are same as those in tree)
  * `tree.copy()`           (`Interval` objects are shallow copies of those in tree)
  * `set(tree)`             (can later be fed into `IntervalTree()`)
  * `list(tree)`            (ditto)

* Equal-able
* Pickle-friendly
* Automatic AVL balancing

Examples
--------

* Getting started

        from intervaltree import Interval, IntervalTree
        t = IntervalTree()

* Adding intervals - any object works!

        t[1:2] = "1-2"
        t[4:7] = (4, 7)
        t[5:9] = {5: 9}

* Query by point

        ivs = t[6]            # set([Interval(4, 7, (4, 7)), Interval(5, 9, {5: 9})])
        iv = sorted(ivs)[0]   # Interval(4, 7, (4, 7))

* Accessing an `Interval` object

        iv.begin  # 4
        iv.end    # 7
        iv.data   # (4, 7)

* Query by range

  Note that ranges are inclusive of the lower limit, but non-inclusive of the upper limit. So:

        t[2:4]    # set()

  But:

        t[1:5]    # set([Interval(1, 2, '1-2'), Interval(4, 7, (4, 7))])

* Constructing from lists of `Interval`s

  We could have made a similar tree this way:

        ivs = [(1, 2), (4, 7), (5, 9)]
        t = IntervalTree(
            Interval(begin, end, "%d-%d" % (begin, end)) for begin, end in ivs
        )

  Or, if we don't need the data fields:

        t = IntervalTree(Interval(*iv) for iv in ivs)

* Removing intervals

        t.remove( Interval(1, 2, "1-2") )
        list(t)     # [Interval(4, 7, '4-7'), Interval(5, 9, '5-9')]

        t.remove( Interval(500, 1000, "Doesn't exist")) # raises ValueError
        t.discard(Interval(500, 1000, "Doesn't exist")) # quietly does nothing

        t.remove_overlap(5)
        list(t)     # []

  We could also empty a tree by removing all intervals, from the lowest bound to the highest bound of the `IntervalTree`:

        t.remove_overlap(t.begin(), t.end())

Future improvements
-------------------

See the [issue tracker][] on GitHub.

Based on
--------

* Eternally Confuzzled's [AVL tree][Confuzzled AVL tree]
* Wikipedia's [Interval Tree][Wiki intervaltree]
* Heavily modified from Tyler Kahn's [Interval Tree implementation in Python][Kahn intervaltree] ([GitHub project][Kahn intervaltree GH])
* Incorporates modifications by [konstantint][Konstantin intervaltree]

Copyright
---------
* [Chaim-Leib Halbert][GH], 2014


[build status badge]: https://travis-ci.org/chaimleib/intervaltree.svg?branch=master
[build status]: https://travis-ci.org/chaimleib/intervaltree
[GH]: https://github.com/chaimleib/intervaltree
[issue tracker]: https://github.com/chaimleib/intervaltree/issues
[Konstantin intervaltree]: https://github.com/konstantint/PyIntervalTree
[Confuzzled AVL tree]: http://www.eternallyconfuzzled.com/tuts/datastructures/jsw_tut_avl.aspx
[Wiki intervaltree]: http://en.wikipedia.org/wiki/Interval_tree
[Kahn intervaltree]: http://zurb.com/forrst/posts/Interval_Tree_implementation_in_python-e0K
[Kahn intervaltree GH]: https://github.com/tylerkahn/intervaltree-python

