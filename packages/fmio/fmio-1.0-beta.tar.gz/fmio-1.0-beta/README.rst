==========================================
fmio - Fast stream I/O for numeric matrices
==========================================

If you have ever piped large CSV or TSV numeric data between
scripts, you might realize just how much time is taken parsing
strings rather than performing actual computations.

``fmio`` is a simple compressed, binary format and Python library
to read and write matrices -- defined as 2D numeric data with row
and column names, analogous to pandas DataFrames that only accept
numeric data.

Installation
============

The only dependencies are numpy and pandas.

.. code-block:: bash
    $ pip install fmio

Usage
=====

From the command-line, you can serialize and deserialize fmio
matrices.

.. code-block:: bash
    
    $ fmio < in.tsv > out.fmio
    $ fmio -dc < out.fmio
    <same as input>

The real purpose is to perform fast reads from within Python:

``run.py``
.. code-block:: python

    import fmio, sys
    with fmio.Reader(sys.stdin) as h:
        for r in h:
            print(r.name, r.sum())

.. code-block:: bash
    
    $ python run.py < out.fmio

Warnings
========

The file format is in machine-native format. Although almost all
modern processors are "little-endian", these files may not be
completely portable.

The library is still in development. The file format is mostly
stable but still subject to change. Don't use this for long-term
data storage.

License
=======

AGPLv3
