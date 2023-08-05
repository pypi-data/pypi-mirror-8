Change log
==========

1.0.1
===
 - 100% test coverage
 - fixed bug in result wrapping (etree._Element has __iter__ too!)

1.0
---
 - add python3 support
 - first production release

0.4.4
-----
 - fix inner_html method
 - added **kwargs to the parse function, added inner_html method to the Parser class
 - cssselect in deps

0.4.2
-----
 - Node attribute modification via node.href = '/blah'
 - Custom default value for get: document.get(selector, default=None)
 - Get element by index: document.get(selector, index)

0.4.1
-----
 - bool(node) returns True if element exists and False if element is None

0.4
---
 - First public version
