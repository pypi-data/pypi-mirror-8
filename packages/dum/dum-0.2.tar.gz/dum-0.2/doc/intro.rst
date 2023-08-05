############
Introduction
############

With the :mod:`dum` module you can easily map data from structured files
to a set of python classes. 
The current version can be used with json, csv or xlm formats, 
more are expected to come.


Parsing and projecting
======================

The main idea is that your code is designed with objects that share more or less the same
organization than the data in the original file.  With a few directives, it must then be possible 
to directly project the data parsed from the file to the class model of your application.

For sample a minimal (all the display methods are still to write...)  `Atom <https://en.wikipedia.org/wiki/Atom_%28standard%29>`_ application
could look like 

.. code-block:: python
    
    class Author:
        class dum: 
            name =""
            email=""
 
    class Link:
        class dum:
            rel=""
            href=""

    class Entry:
        class dum:
            title = ""
            author = [Author]
            link = [Link]
            updated = dateutil.parser.parse

    class Atom:
        class dum:
            title =""
            subtitle= ""
            entry = [Entry]
            link = [Link]
            updated = dateutil.parser.parse
        
    atom = dum.xml(Atom, open("myrss"))




About
=====
It's free software, available under the MIT license

The library has been tested for Python 3.4 but should work with any Python 3 version.
There is no external dependencies.

To get last version of dum :
 * `Mercurial repository on Bitbucket <https://bitbucket.org/sebkeim/dum>`_ 
 * `From the Python Package Index <https://pypi.python.org/pypi/dum>`_ 



