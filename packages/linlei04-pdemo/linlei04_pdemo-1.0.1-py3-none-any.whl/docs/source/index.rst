.. pdemo documentation master file, created by
   sphinx-quickstart on Thu Nov  2 17:17:12 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pdemo's documentation!
=================================

**Lumache** (/lu'make/) is a Python library for cooks and food lovers that
creates recipes mixing random ingredients.  It pulls data from the `Open Food
Facts database <https://world.openfoodfacts.org/>`_ and offers a *simple* and
*intuitive* API.

.. note::

   This project is under active development.

.. sidebar:: About Pdemo

    Pdemo is a demo for python project demo. This is ref: :ref:`my_ref`.

README
------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   README
   Other

Other
-----

.. toctree:: 
   :maxdepth: 1

   README
   Other


Code
----

.. py:function:: random.randint(a, b)

   Return random integer in range [a, b], including both end points.

   :param a: from.
   :type a: int
   :param b: to.
   :type b: int
   :return: rand.
   :rtype: int


The ``a`` and ``b`` should be int, otherwise :py:func:`random.randint` will raise exception.

.. autofunction:: pdemo.src.add.add


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
