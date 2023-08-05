`rst2textile` is docutils textile writer convert reStructuredText(rst) to Textile format.

Features
==========

* Docutils writer for textile.

  * supported syntaxes are:

    * headings: h1/h2..
    * docinfo: field-list (like `:Date: today`) at top of rst file.
    * paragraph
    * emphasis: `*em*`
    * strong: `**strong**`
    * list-item: `* egg`
    * enum-item: `#. ham`
    * blockquote
    * link: `\`foo <http://example.com/>\`_`
    * image: `.. image:: http://example.com/image.png`
    * literal: `\`\`some code\`\`` and `::`

* Sphinx textile builder (experimental).

  #. write conf.py `extensions = ['docutils_textile']`
  #. build by `sphinx-build -b textile source _build/textile`

Install
========

::

   $ pip install rst2textile


If you wanto to use unrelease version, you can install from repository::

   $ pip install -e hg+https://bitbucket.org/shimizukawa/rst2textile#egg=rst2textile


Run
======

::

   $ rst2textile.py input.rst output.txt

or::

   $ python -m rst2textile input.rst output.txt


Test
=====

::

   $ python setup.py test

or::

   $ python test.py


Depends
========
* Python 2.6, 2.7, 3.3, 3.4
* Docutils 0.12, 0.11, 0.10


Limitation
============
* Not supported: some textile syntax at http://redcloth.org/textile


ToDo
=====
* Documentation
* Implement some textile format.

CHANGES
========

0.2.0 (2014/10/04)
------------------
* add support textile table output. Thanks to tell-k.
* remove pysetup related lines.
* change supported python versions: 2.6, 2.7, 3.3, 3.4
* change supported docutils versions: 0.12, 0.11, 0.10

0.1.1 (2012/4/29)
------------------
* add supported python versions: 2.4, 2.5, 2.6, 3.1, 3.2, 3.3

0.1.0 (2012/4/22)
------------------
* first release
* supported syntax: h1/h2.., docinfo, paragraph, *em*, **strong**, list-item, enum-item, blockquote, link, image, literal


Convert Samples
==================

Heading1
---------
.. container:: test, rst, textile

   rst::

      ==========
      Heading1
      ==========

   textile::

      h1. Heading1

Headings
---------
.. container:: test, rst, textile

   rst::

      ==========
      Heading1
      ==========

      Heading2
      ==========

      Heading3
      ----------

      Heading4
      ^^^^^^^^^^

   textile::

      h1. Heading1


      h2. Heading2


      h3. Heading3


      h4. Heading4


Document Information
-----------------------
.. container:: test, rst, textile

   rst::

      HelloWorld
      ===========

      :Date: Today
      :Author: SpamEgg
      :Location: Here

   textile::

      h1. HelloWorld

      Date:
         Today

      Author:
         SpamEgg

      Location:
         Here

Paragraph
----------

.. container:: test, rst, textile

   rst::

      Normal Text

   textile::

      Normal Text

Emphasized
-----------

.. container:: test, rst, textile

   rst::

      *emphasized* (e.g., italics)

   textile::

      _emphasized_ (e.g., italics)

Strongly emphasized
--------------------
.. container:: test, rst, textile

   rst::

      **strongly emphasized** (e.g., boldface)

   textile::

      *strongly emphasized* (e.g., boldface)

List items
-----------
.. container:: test, rst, textile

   rst::

      - An item in a bulleted (unordered) list

      - Another item in a bulleted list

        - Second Level

        * Second Level Items

          * Third level

   textile::

      * An item in a bulleted (unordered) list
      * Another item in a bulleted list
      ** Second Level
      ** Second Level Items
      *** Third level

Enumerated list items
----------------------
.. container:: test, rst, textile

   rst::

      #. An item in an enumerated (ordered) list xxxxxxx
      #. Another item in an enumerated list yyyyyy

         #. Another level in an enumerated list vvvvvvvv
         #. Another level in an enumerated list vvvvvvvv

      #. 3rd element at indent level1

   textile::

      # An item in an enumerated (ordered) list xxxxxxx
      # Another item in an enumerated list yyyyyy
      ## Another level in an enumerated list vvvvvvvv
      ## Another level in an enumerated list vvvvvvvv
      # 3rd element at indent level1

Blockquotes
------------
.. container:: test, rst, textile

   rst::

      Blockquotes

         This text will be enclosed in an HTML blockquote element.

         Second Paragraph.

   textile::

      Blockquotes

      bq. This text will be enclosed in an HTML blockquote element.
      bq. Second Paragraph.

Links
-------
.. container:: test, rst, textile

   rst::

      `link text and link target url <http://www.example.com/link/target/address>`_

   textile::

      "link text and link target url":http://www.example.com/link/target/address

Images
-------
.. container:: test, rst, textile

   rst::

       .. image:: http://example.com/image.jpg

       .. figure:: local/image/path.png

   textile::

      !http://example.com/image.jpg!

      !local/image/path.png!


Inner Reference
----------------
.. container:: test, rst, textile

   rst::

      HelloWorld
      ===========

      reference to HelloWorld_ !

   textile::

      h1. HelloWorld

      reference to "HelloWorld" !


Literal (code)
----------------
.. container:: test, rst, textile

   rst::

      ::

         class Foo(object):

             def __init__(self, value):
                 print "value = %d" % value
                 raise NotImplementedError(u'EmptyClass')

   textile::

      <pre>
      class Foo(object):

          def __init__(self, value):
              print "value = %d" % value
              raise NotImplementedError(u'EmptyClass')
      </pre>

Tables
----------------
.. container:: test, rst, textile

   rst::

      +------------------------+------------+----------+----------+
      | Header row, column 1   | Header 2   | Header 3 | Header 4 |
      | (header rows optional) |            |          |          |
      +========================+============+==========+==========+
      | body row 1, column 1   | column 2   | column 3 | column 4 |
      +------------------------+------------+----------+----------+
      | body row 2             | ...        | ...      |          |
      +------------------------+------------+----------+----------+

   textile::

      |_.  Header row, column 1
      (header rows optional)|_.  Header 2     |_.  Header 3   |_.  Header 4   |
      | body row 1, column 1     | column 2     | column 3   | column 4   |
      | body row 2               | ...          | ...        |            |


.. container:: test, rst, textile

   rst::

      =====  =====  =======
      A      B      A and B
      =====  =====  =======
      False  False  False
      True   False  False
      False  True   False
      True   True   True
      =====  =====  =======

   textile::

      |_.  A     |_.  B     |_.  A and B |
      | False | False | False   |
      | True  | False | False   |
      | False | True  | False   |
      | True  | True  | True    |


CSV Table
----------------
.. container:: test, rst, textile

   rst::

      .. csv-table::
         :header: "Treat", "Quantity", "Description"
         :widths: 15, 10, 30

         "Albatross", 2.99, "On a stick!"
         "Crunchy Frog", 1.49, "If we took the bones out, it wouldn't be
         crunchy, now would it?"
         "Gannet Ripple", 1.99, "On a stick!"

   textile::

      |_.  Treat           |_.  Quantity   |_.  Description                    |
      | Albatross       | 2.99       | On a stick!                    |
      | Crunchy Frog    | 1.49       | If we took the bones out, it wouldn't be
      crunchy, now would it?|
      | Gannet Ripple   | 1.99       | On a stick!                    |


List Table
---------------

.. container:: test, rst, textile

   rst::

      .. list-table::
         :widths: 15 10 30
         :header-rows: 1

         * - Treat
           - Quantity
           - Description
         * - Albatross
           - 2.99
           - On a stick!
         * - Crunchy Frog
           - 1.49
           - If we took the bones out, it wouldn't be
             crunchy, now would it?
         * - Gannet Ripple
           - 1.99
           - On a stick!

   textile::
       
       |_.  Treat           |_.  Quantity   |_.  Description                    |
       | Albatross       | 2.99       | On a stick!                    |
       | Crunchy Frog    | 1.49       | If we took the bones out, it wouldn't be
       crunchy, now would it?|
       | Gannet Ripple   | 1.99       | On a stick!                    |
