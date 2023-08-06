===========
citeproc-py
===========

citeproc-py is a `CSL`_ processor for Python. It aims to implement the
`CSL 1.0.1 specification`_. citeproc-py can output styled citations and
bibliographies in a number of different output formats. Currently
supported are plain text, reStructuredText and HTML. Other formats can
be added easily.

citeproc-py uses `semantic versioning`_. Currently, its major version
number is still at 0, meaning the API is not yet stable. However, you
should not expect to see any major API changes soon.

.. _CSL: http://citationstyles.org/
.. _CSL 1.0.1 specification: http://citationstyles.org/documentation/
.. _semantic versioning: http://semver.org/


Requirements
------------

citeproc-py has been developed for Python 3 but also runs on Python
2.6+. It depends on `lxml`_ for parsing and navigating the CSL style and
locale files.

.. _lxml: http://lxml.de/


Getting Started
---------------

To get started with citeproc-py, take a look at the examples under
``examples/``. Two examples are provided, one parsing references from a
JSON representation of references as supported by citeproc-js, another
parsing the references from a BibTeX file. Both show and explain how to
cite references and render the bibliography.


CSL Compatibility
-----------------

Currently, citeproc-py passes almost 60% of the (relevant) tests in the
`citeproc-test suite`_. However, it is more than 60% complete, as
citeproc-py doesn't take care of double spaces and repeated punctuation
marks yet, making a good deal of the tests fail. In addition, the
following features have not yet been implemented (there are probably
some I forgot though):

-  disambiguation/year-suffix
-  et-al-subsequent-min/et-al-subsequent-use-first
-  collapsing
-  punctuation-in-quote
-  display

Also, some `citeproc-js`_ functionality that is not part of the CSL spec
is not (yet) supported:

-  raw dates
-  static-ordering
-  literal names

.. _citeproc-test suite: https://bitbucket.org/bdarcus/citeproc-test
.. _citeproc-js: http://bitbucket.org/fbennett/citeproc-js/wiki/Home


Running the Tests
-----------------

First clone the `citeproc-test suite`_ so that it sits next to the
citeproc-py directory. Then run the ``processor.py`` script to generate
the test fixtures (using Python 2.x). After that, you can run
``citeproc-test.py`` (in the ``tests`` directory). Run
``citeproc-test.py --help`` to see its usage information.

.. _citeproc-test suite: https://bitbucket.org/bdarcus/citeproc-test
