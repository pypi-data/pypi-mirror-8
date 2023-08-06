Introduction
============

|Build Status| |Latest Version| |Supported Python versions| |Development
Status| |Wheel Status| |Download format| |License|

RedBaron is a python library and tool powerful enough to be used into
IPython solely that intent to make the process of **writting code that
modify source code** as easy and as simple as possible. That include
writing custom refactoring, generic refactoring, tools, IDE or directly
modifying you source code into IPython with an higher and more powerful
abstraction than the advanced texts modification tools that you find in
advanced text editors and IDE.

RedBaron guaranteed you that **it will only modify your code where you
ask him to**. To achieve this, it is based on
`Baron <https://github.com/Psycojoker/baron>`__ a lossless
`AST <https://en.wikipedia.org/wiki/Abstract_syntax_tree>`__ for Python
that guarantees the operation ast\_to\_code(code\_to\_ast(source\_code))
== source\_code. (Baron's AST is called a FST, a Full Syntax Tree).

RedBaron API and feel is heavily inspired by BeautifulSoup. It tries to
be simple and intuitive and that once you've get the basics principles,
you are good without reading the doc for 80% of your operations.

**For now, RedBaron can be considered in alpha, the core is quite stable
but it is not battle tested yet and is still a bit rough.** Feedback is
very welcome.

Installation
============

::

    pip install redbaron

Links
=====

**RedBaron is fully documented, be sure to check the turorial and
documentation**.

-  `Tutorial <https://redbaron.readthedocs.org/en/latest/tuto.html>`__
-  `Documentation <https://redbaron.readthedocs.org>`__
-  `Baron <https://github.com/Psycojoker/baron>`__
-  IRC chat:
   `irc.freenode.net#baron <https://webchat.freenode.net/?channels=%23baron>`__

.. |Build Status| image:: https://travis-ci.org/Psycojoker/redbaron.svg?branch=master
   :target: https://travis-ci.org/Psycojoker/redbaron
.. |Latest Version| image:: https://pypip.in/version/redbaron/badge.svg
   :target: https://pypi.python.org/pypi/redbaron/
.. |Supported Python versions| image:: https://pypip.in/py_versions/redbaron/badge.svg
   :target: https://pypi.python.org/pypi/redbaron/
.. |Development Status| image:: https://pypip.in/status/redbaron/badge.svg
   :target: https://pypi.python.org/pypi/redbaron/
.. |Wheel Status| image:: https://pypip.in/wheel/redbaron/badge.svg
   :target: https://pypi.python.org/pypi/redbaron/
.. |Download format| image:: https://pypip.in/format/redbaron/badge.svg
   :target: https://pypi.python.org/pypi/redbaron/
.. |License| image:: https://pypip.in/license/redbaron/badge.svg
   :target: https://pypi.python.org/pypi/redbaron/


Changelog
=========

0.3 (2014-11-12)
----------------

- proxy lists, major improvement in the management of list of things
- .append_value is no more since it is useless now due to proxy lists
- .index has been renamed to .index_on_parent to be more coherent

0.2 (2014-09-23)
----------------

- for EVERY NODES in RedBaron, the automagic behavior when passing a string to
  modify an attribute has been done, this is HUGE improvement
  https://redbaron.readthedocs.org/en/latest/modifying.html#full-documentations
- it's now possible to use regex, globs, list/tuple and lambda (callable) in .find and
  .find_all, see https://redbaron.readthedocs.org/en/latest/querying.html#advanced-querying
- new method on node: .replace() to replace in place a node
  https://redbaron.readthedocs.org/en/latest/other.html#replace
- .map .filter and .apply are now documented https://redbaron.readthedocs.org/en/latest/other.html#map-filter-apply
- .edit() new helper method to launch a text editor on the selected node and
  replace the node with the modified code https://redbaron.readthedocs.org/en/latest/other.html#edit
- .root node attribute (property) that return the root node of the tree in which the
  node is stored https://redbaron.readthedocs.org/en/latest/other.html#root
- .index node attribute (property) that returns the index at which the node is
  store if it's store in a nodelist, None otherwise https://redbaron.readthedocs.org/en/latest/other.html#index
- setitem (a[x] = b) on nodelist now works as expected (accepting string, fst
  node and redbaron node)
- new method to handle indentation: .increase_indentation and .decrease_indentation https://redbaron.readthedocs.org/en/latest/other.html#increase-indentation-and-decrease-indentation
- various small bugfix
- we have one new contributor \o/ https://github.com/ze42
- to_node has been move to a class method of Node: Node.from_fst
- pretty print of nodes when using redbaron in a script

0.1 (2014-06-13)
----------------

- First release


