=============
tinysegmenter
=============

------------------------------------------------
Python module implementing a Japanese tokenizer.
------------------------------------------------

:Date: 2012-09-24
:Version: 0.2
:Manual section: 7
:Author: tinysegmenter at zemarmot.net

SYNOPSIS
========

import tinysegmenter

DESCRIPTION
===========

``tinysegmenter`` is an extremely compact Japanese segmenter written natively in Python (supports Python 2 and 3).
It contains a unique class ``TinySegmenter`` which in turns defines a single "public" method ``tokenize()``.

The ``tokenize(text)`` call takes a natural language Japanese text as a unicode string parameter ``text``,
and returns a list of unicode strings, each element of the list being a lexical token of the initial parameter.

Interface::

    class tinysegmenter.TinySegmenter:
        def tokenize(ustring): # Return type list(ustring)

APPLICATION USAGE
=================

This module allows to simply break Japanese sentences into lexical tokens,
which in natural language could be considered as grammatical words.
This natural language processing (NLP) is particular for Japanese,
as this agglutinative does not use any space, and very few punctuations, making it
particularly difficult to tokenize a sentence.

EXAMPLE
=======

The sentence "I live in Tokyo" being written "東京で住んにいます", here is how you could tokenize it::

    import tinysegmenter
    segmenter = tinysegmenter.TinySegmenter() 
    tokens = segmenter.tokenize(u'東京に住む')

``tokens`` would now hold the value: [u'東京', u'に', u'住む'] ('Tokyo', location particle, and verb).

COMPATIBILITY
=============

``tinysegmenter.TinySegmenter`` ‘s interface is compatible with the *Natural Language Toolkit* (``NLTK``) python module’s ``TokenizerI`` class,
although the distribution does not directly depend on NLTK.
Here is one way to use it as a tokenizer in NLTK (order of the multiple base classes matters)::

    import nltk.tokenize.api
    class myTinySegmenter(tinysegmenter.TinySegmenter, nltk.tokenize.api.TokenizerI):
        pass
    segmenter = myTinySegmenter()
    # This segmenter can be used any place which expects a NLTK's TokenizerI subclass.

SEE ALSO
========

TinySegmenter's currently maintained website can be found here: http://tinysegmenter.tuxfamily.org/

It is available also as a pypi module: http://pypi.python.org/pypi/tinysegmenter

All bug, patch, question, etc. can be sent to ``tinysegmenter at zemarmot dot net``.

To know more about NLTK's ``TokenizerI``, and NLTK itself, see: http://nltk.org/api/nltk.tokenize.html#nltk.tokenize.api.TokenizerI

ABOUT
=====

Copyright (c) 2008, Taku Kudo
Copyright (c) 2010, Masato Hagiwara
Copyright (c) 2012, Jehan

This module is distributed under a **New BSD** license that you should find in this distribution.

