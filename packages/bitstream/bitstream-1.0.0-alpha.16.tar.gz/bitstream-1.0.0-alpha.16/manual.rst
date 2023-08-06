**About this document.** It is originally a plain text file using the
`Markdown <http://daringfireball.net/projects/markdown/>`__ syntax, but
you may be reading a HTML, PDF or ReST version instead. In any case, the
contents are subject to a `Creative Commons Attribution
3.0 <http://creativecommons.org/licenses/by/3.0/>`__ license.

What is Bitstream ?
===================

Bitstream provides a binary data type with a stream interface for
`Python <http://www.python.org/>`__.

-  **Binary Data:** the ``BitStream`` class is a linearly ordered
   container of bits. The standard library is only convenient to manage
   binary data at the byte level. Consider using BitStream instead,
   especially you need to address the bit level.

-  **Stream Interface:** you can only read data at the start of a stream
   and write data at its end. This is a very simple way to interact with
   binary data, but it is also the pattern that comes naturally in many
   applications. To manage binary codes and formats, in my experience,
   random data access is not a requirement.

-  **Python and NumPy Types.** BitStream has built-in readers and
   writers for the common data types with a standard binary layout:
   bools, ASCII strings, fixed-size integers and floating-point
   integers.

-  **User-Defined Types.** The list of supported types and binary
   representation may be enlarged at will: new readers and writers can
   be implemented and associated to specific data types.

-  **Performance.** Bitstream is a Python C-extension module that has
   been optimized for the common use cases. Hopefully, it will be fast
   enough for your needs ! Under the hood, the
   `Cython <http://www.cython.org>`__ language and compiler are used to
   generate this extension module.

-  **Open-Source:** the Bitstream software is distributed under a `MIT
   license <http://opensource.org/licenses/MIT>`__, its documentation
   under a `Creative Commons Attribution
   3.0 <http://creativecommons.org/licenses/by/3.0/>`__ license. The
   development takes place on
   `GitHub <https://github.com/boisgera/bitstream>`__ and releases are
   also available on `PyPi <https://pypi.python.org/pypi/bitstream/>`__.

Requirements & Installation
===========================

Bitstream targets `Python
2.7 <http://www.python.org/download/releases/2.7>`__, you will need to
install it first.

**TODO:** move NumPy dependency here (? Dunno ...), talk about
Linux-only platform.

Then, several installation options are available: **TODO:** state
clearly what one should do depending on the aim.

-  **Easy install:** if the `pip <https://pypi.python.org/pypi/pip>`__
   package manager is available, execute the following command as root:

   ::

       $ pip install bitstream

   The dependencies of Bitstream will be handled automatically. If you
   don't have root privileges, use
   `virtualenv <https://pypi.python.org/pypi/virtualenv>`__.

-  **Install from source:** the releases of Bitstream are available on
   the `Python Package Index
   (PyPi) <https://pypi.python.org/pypi/bitstream/>`__. Once you have
   downloaded and unpacked the archive, to build the Bitstream module,
   you need `setuptools <https://pypi.python.org/pypi/setuptools>`__.
   You also need to install the `NumPy <http://www.numpy.org/>`__
   package, version 1.6.1 or later.

   **TODO: test if numpy is automatically download if needed**.

   Then, as root, execute

   ::

       $ python setup.py install

-  **Hack with git:** to experiment with the latest version of
   Bitstream, clone the GitHub repository:

   ::

       $ git clone git://github.com/boisgera/bitstream.git

   To actually build the module, you will need everything you need to
   build from source and will execute the same command. If in addition,
   you want to edit the source files, you will also need the
   `Cython <http://www.cython.org>`__ compiler, version 0.15.1 or later
   and will execute instead:

   ::

       $ python setup.py install --with-cython

Getting Started
===============

Most of the features of bitstream are available via the ``BitStream``
class.

::

    >>> from bitstream import BitStream

The module is tightly integrated with the
`NumPy <http://www.numpy.org/>`__ library. For convenience, we import
all symbols from its top-level module.

::

    >>> from numpy import *

Overview of Bitstream Features
==============================

::

    >>> stream = BitStream()
    >>> stream
    <BLANKLINE>
    >>> stream.write(True, bool)
    >>> stream
    1
    >>> stream.write(False, bool)
    >>> stream
    10
    >>> stream.write(-128, int8)
    >>> stream
    1010000000
    >>> stream.write("AB", str)
    >>> stream
    10100000000100000101000010
    >>> stream.read(bool, 2)
    [True, False]
    >>> stream
    100000000100000101000010
    >>> stream.read(int8, 1)
    array([-128], dtype=int8)
    >>> stream
    0100000101000010
    >>> stream.read(str, 2)
    'AB'
    >>> stream
    <BLANKLINE>

Built-in Readers and Writers
============================

Bools
-----

Write single bits to a bitstream with the arguments ``True`` and
``False``:

::

    >>> stream = BitStream()
    >>> stream.write(False, bool)
    >>> stream.write(True , bool)
    >>> stream
    01

Lists of booleans may be used too write multiple bits at once:

::

    >>> stream = BitStream()
    >>> stream.write([], bool)
    >>> stream
    <BLANKLINE>
    >>> stream.write([False], bool)
    >>> stream.write([True] , bool)
    >>> stream
    01
    >>> stream.write([False, True], bool)
    >>> stream
    0101

The second argument to the ``write`` method -- the type information --
can also be specified with the keyword argument ``type``:

::

    >>> stream = BitStream()
    >>> stream.write(False, type=bool)
    >>> stream.write(True , type=bool)
    >>> stream
    01

For single bools or lists of bools, the type information is optional:

::

    >>> stream = BitStream()
    >>> stream.write(False)
    >>> stream.write(True)
    >>> stream.write([])
    >>> stream.write([False])
    >>> stream.write([True])
    >>> stream.write([False, True])
    >>> stream
    010101

Numpy ``bool_`` scalars or one-dimensional arrays can be used instead:

::

    >>> bool_
    <type 'numpy.bool_'>
    >>> stream = BitStream()
    >>> stream.write(bool_(False)  , bool)
    >>> stream.write(bool_(True)   , bool)
    >>> stream
    01

    >>> stream = BitStream()
    >>> empty = array([], dtype=bool)
    >>> stream.write(empty, bool)
    >>> stream
    <BLANKLINE>
    >>> stream.write(array([False]), bool)
    >>> stream.write(array([True]) , bool)
    >>> stream.write(array([False, True]), bool)
    >>> stream
    0101

For such data, the type information is also optional:

::

    >>> stream = BitStream()
    >>> stream.write(bool_(False))
    >>> stream.write(bool_(True))
    >>> stream.write(array([], dtype=bool))
    >>> stream.write(array([False]))
    >>> stream.write(array([True]))
    >>> stream.write(array([False, True]))
    >>> stream
    010101

Python and Numpy numeric types are also valid arguments: zero is
considered false and nonzero numbers are considered true.

**Q:** Use a predicate instead (non-zero) ? and check iff ?

::

    >>> small_integers = range(0, 64)
    >>> stream = BitStream()
    >>> for integer in small_integers:
    ...     stream.write(integer, bool)
    >>> stream
    0111111111111111111111111111111111111111111111111111111111111111
    >>> stream = BitStream()
    >>> for integer in small_integers:
    ...     stream.write(-integer, bool)
    >>> stream
    0111111111111111111111111111111111111111111111111111111111111111

    >>> large_integers = [2**i for i in range(6, 64)]
    >>> stream = BitStream()
    >>> for integer in large_integers:
    ...     stream.write(integer, bool)
    >>> stream
    1111111111111111111111111111111111111111111111111111111111
    >>> stream = BitStream()
    >>> for integer in large_integers:
    ...     stream.write(-integer, bool)
    >>> stream
    1111111111111111111111111111111111111111111111111111111111

**TODO:** use iinfo(type).min/max

**TODO:** write ``sample(type, r)`` iterator.

::

    >>> def irange(start, stop, r=1.0):
    ...     i = 0
    ...     while i < stop:
    ...         yield i
    ...         i = max(i+1, int(i*r))

    >>> unsigned = [uint8, uint16, uint32]
    >>> for integer_type in unsigned:
    ...     _min, _max = iinfo(integer_type).min, iinfo(integer_type).max
    ...     for i in irange(_min, _max + 1, r=1.001):
    ...         integer = integer_type(i)
    ...         if integer and BitStream(integer, bool) != BitStream(True):
    ...             type_name = integer_type.__name__
    ...             print "Failure for {0}({1})".format(type_name, integer)





    >>> stream = BitStream()
    >>> stream.write(0.0, bool)
    >>> stream.write(1.0, bool)
    >>> stream.write(pi , bool)
    >>> stream.write(float64(0.0), bool)
    >>> stream.write(float64(1.0), bool)
    >>> stream.write(float64(pi) , bool)
    >>> stream
    011011

**TODO:** arrays of numeric type (non-bools), written as bools

--------------

**TODO:** Mark all following behaviors as undefined ? Probably safer ...

Actually, any single data written as a bool, is conceptually cast into a
bool first, with the semantics of the ``bool`` constructor. List and
one-dimensional numpy array arguments are considered holders of multiple
data, each of which is converted to bool. Any other sequence type
(strings, tuples, etc.) is considered single data.

::

    >>> bool("")
    False
    >>> bool(" ")
    True
    >>> bool("A")
    True
    >>> bool("AAA")
    True

    >>> stream = BitStream()
    >>> stream.write("", bool)
    >>> stream.write(" ", bool)
    >>> stream.write("A", bool)
    >>> stream.write("AAA", bool)
    >>> stream
    0111
    >>> stream = BitStream()
    >>> stream.write(["", " " , "A", "AAA"], bool)
    >>> stream
    0111
    >>> stream = BitStream()
    >>> stream.write(array(["", " " , "A", "AAA"]), bool)
    >>> stream
    0111

    >>> stream = BitStream()
    >>> stream.write(    (), bool)
    >>> stream.write(  (0,), bool)
    >>> stream.write((0, 0), bool)
    >>> stream
    011

    >>> stream = BitStream()
    >>> stream.write([[], [0], [0, 0]], bool)
    >>> stream
    011

    >>> class BoolLike(object):
    ...     def __init__(self, value):
    ...         self.value = bool(value)
    ...     def __nonzero__(self):
    ...         return self.value
    >>> false = BoolLike(False)
    >>> true = BoolLike(True)
    >>> stream = BitStream()
    >>> stream.write(false, bool)
    >>> stream.write(true, bool)
    >>> stream.write([false, true], bool)
    >>> stream
    0101

TODO:

-  direct call to ``write_bool`` (import the symbol first)
-  reader tests

Integers
--------

**TODO**

Floating-Point Numbers
----------------------

::

    >>> import struct
    >>> struct.pack(">d", pi)
    '@\t!\xfbTD-\x18'

    >>> stream = BitStream()
    >>> stream.write(0.0)
    >>> stream.write([1.0, 2.0, 3.0])
    >>> stream.write(arange(4.0, 10.0))
    >>> len(stream)
    640
    >>> output = stream.read(float, 10)
    >>> type(output)
    <type 'numpy.ndarray'>
    >>> all(output == arange(10.0))
    True

    >>> BitStream(1.0) == BitStream(1.0, float) == BitStream(1.0, float64)
    True
    >>> BitStream(1.0) == BitStream([1.0]) == BitStream(ones(1))
    True

The byte order is big endian:

::

    >>> BitStream(struct.pack(">d", pi)) == BitStream(pi)
    True

Extra Methods
=============

**TODO:**:

-  length

-  str, repr

-  \_extend ? Make it public ? This is low-level ... but may be
   necesssary to implement new readers/writers. Don't specify it now, as
   we don't specify the offsets / stream state, let the user only rely
   on the high-level methods.

-  copy

-  hash, comparison.

Custom Writers and Readers
==========================

::

    >>> import bitstream

Definition and Registration of Writers and Readers
--------------------------------------------------

Let's define a writer for the binary representation of natural numbers:

::

    >>> def write_integer(stream, data):
    ...     if isinstance(data, list):
    ...         for integer in data:
    ...             write_integer(stream, integer)
    ...     else:
    ...         integer = int(data)
    ...         if integer < 0:
    ...             error = "negative integers cannot be encoded"
    ...             raise ValueError(error)
    ...         bools = []
    ...         while integer:
    ...             bools.append(integer & 1)
    ...             integer = integer >> 1
    ...         bools.reverse()
    ...         stream.write(bools, bool)

We can check that this writer behaves as expected:

::

    >>> stream = BitStream()
    >>> write_integer(stream, 42)
    >>> stream
    101010
    >>> write_integer(stream, [1, 2, 3])
    >>> stream
    10101011011

Then, we can associate it to the type ``int``:

::

    >>> bitstream.register(int, writer=write_integer)

After this step, ``BitStream`` will redirect all data of type ``int`` to
this writer:

::

    >>> BitStream(42)
    101010
    >>> BitStream([1, 2, 3])
    11011

If the type information is explicit, other kind of data can use this
writer too:

::

    >>> BitStream(uint8(42), int)
    101010
    >>> BitStream("42", int)
    101010

A possible implementation of the corresponding reader is given by:

::

    >>> def read_integer(stream, n=None):
    ...     if n is not None:
    ...         error = "unsupported argument n"
    ...         raise NotImplementedError(error)
    ...     else:
    ...         integer = 0
    ...         for _ in range(len(stream)):
    ...             integer = integer << 1
    ...             if stream.read(bool):
    ...                 integer += 1
    ...     return integer

    >>> read_integer(BitStream(42))
    42

Once this reader is registered with

::

    >>> bitstream.register(int, reader=read_integer)

the calls to ``read_integer`` can be made through the ``read`` method of
``BitStream``.

::

    >>> BitStream(42).read(int)
    42

In all readers, the second argument of readers, named ``n``, represents
the number of values to read from the stream. Here, this argument is not
supported, instead any call to this reader interprets the complete
stream content as a single value.

Writer and Reader Factories
---------------------------

We actually had a legitimate reason not to support the number of values
argument in the binary representation reader. Indeed, when the binary
representation is used to code sequence of integers instead of a single
integer, it becomes ambiguous: the same bitstream may represent several
sequences of integers. For example, we have:

::

    >>> BitStream(255)
    11111111
    >>> BitStream([15, 15])
    11111111
    >>> BitStream([3, 7, 3, 1])
    11111111
    >>> BitStream([3, 3, 3, 3])
    11111111

We say that this code is not *self-delimiting*, as there is no way to
know where is the boundary between the bits coding for different
integers.

For natural numbers with known bounds, we may solve this problem by
setting a number of bits to be used for each integer. However, to do
that, we would have to define and register a new writer for every
possible number of bits. Instead, we register a single but configurable
writer, defined by a writer factory.

Let's define a type tag ``uint`` whose instances hold a number of bits:

::

    >>> class uint(object):
    ...     def __init__(self, num_bits):
    ...         self.num_bits = num_bits

Then, we define a factory that given a ``uint`` instance, returns a
stream writer:

::

    >>> def write_uint_factory(instance):
    ...     num_bits = instance.num_bits
    ...     def write_uint(stream, data):
    ...         if isinstance(data, list):
    ...             for integer in data:
    ...                 write_uint(stream, integer)
    ...         else:
    ...             integer = int(data)
    ...             if integer < 0:
    ...                 error = "negative integers cannot be encoded"
    ...                 raise ValueError(error)
    ...             bools = []
    ...             for _ in range(num_bits):
    ...                 bools.append(integer & 1)
    ...                 integer = integer >> 1
    ...             bools.reverse()
    ...             stream.write(bools, bool)
    ...     return write_uint

Finally, we register this writer factory with ``bitstream``:

::

    >>> bitstream.register(uint, writer=write_uint_factory)

To select a writer, we use the proper instance of type tag:

::

    >>> BitStream(255, uint(8))
    11111111
    >>> BitStream(255, uint(16))
    0000000011111111
    >>> BitStream(42, uint(8))
    00101010
    >>> BitStream(0, uint(16))
    0000000000000000

**TODO: reader, give details, comment.**

::

    >>> def read_uint_factory(instance): # use the name factory ?
    ...     num_bits = instance.num_bits
    ...     def read_uint(stream, n=None):
    ...         if n is None:
    ...             integer = 0
    ...             for _ in range(num_bits):
    ...                 integer = integer << 1
    ...                 if stream.read(bool):
    ...                     integer += 1
    ...             return integer
    ...         else:
    ...             integers = [read_uint(stream) for _ in range(n)]
    ...             return integers
    ...     return read_uint

    >>> bitstream.register(uint, reader=read_uint_factory)

    >>> stream = BitStream([0, 1, 2, 3, 4], uint(8))
    >>> stream.read(uint(8))
    0
    >>> stream.read(uint(8), 1)
    [1]
    >>> stream.read(uint(8), 3)
    [2, 3, 4]

Unit Tests
==========

The text version of the document you are reading is also an executable
specification. Check that the code examples produce the expected results
with

::

    $ python -m doctest -v manual.txt

Examples
========

Unary coder / Rice coder ? Huffman tree/table coder ?
