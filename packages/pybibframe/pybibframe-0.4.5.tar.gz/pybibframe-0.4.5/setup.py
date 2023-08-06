# -*- coding: utf-8 -*-
import sys, os
from distutils.core import setup

versionfile = 'lib/version.py'
exec(compile(open(versionfile, "rb").read(), versionfile, 'exec'), globals(), locals())
__version__ = '.'.join(version_info)

LONGDESC = '''pybibframe
==========

Requires Python 3.4 or more recent. To install dependencies:

::

    pip install -r requirements.txt

Then install pybibframe:

::

    python setup.py install

Usage
=====

Converting MARC/XML to RDF or Versa output (command line)
---------------------------------------------------------

Note: Versa is a model for Web resources and relationships. Think of it
as an evolution of Resource Description Framework (RDF) that’s at once
simpler and more expressive. It’s the default internal representation
for PyBibframe, though regular RDF is an optional output.

::

    marc2bf records.mrx

Reads MARC/XML from the file records.mrx and outputs a Versa
representation of the resulting BIBFRAME records in JSON format. You can
send that output to a file as well:

::

    marc2bf -o resources.versa.json records.mrx

The Versa representation is the primary format for ongoing, pipeline
processing.

If you want an RDF/Turtle representation of this file you can do:

::

    marc2bf -o resources.versa.json --rdfttl resources.ttl records.mrx

If you want an RDF/XML representation of this file you can do:

::

    marc2bf -o resources.versa.json --rdfxml resources.rdf records.mrx

You can get the source from standard input:

::

    curl http://lccn.loc.gov/2006013175/marcxml | marc2bf -c /Users/uche/dev/zepheira/pybibframe-plus/test/resource/config1.json --mod=bibframe.zextra -o /tmp/marc2bf.versa.json

.. raw:: html

   <!--
       See also Das Innere des Glaspalastes in London from one of Eric Miller's favorite examples
       curl http://lccn.loc.gov/2012659481/marcxml | marc2bf -c /Users/uche/dev/zepheira/pybibframe-plus/test/resource/config1.json --mod=bibframe.zextra -o /tmp/marc2bf.versa.json
   -->

(Pulling a record from the Web, in particular Library of Congress Online
Catalog / LCCN Permalink)

You can process more than one MARC/XML file at a time by listing them on
the command line:

::

    marc2bf records1.mrx records2.mrx records3.mrx

Or by using wildcards:

::

    marc2bf records?.mrx

PyBibframe is highly extensible, and you can specify plug-ins from the
command line. You need to specify the Python module from which the
plugins can be imported and a configuration file specifying how the
plugins are to be used. For example, to use the ``linkreport`` plugin
that comes with PyBibframe you can do:

::

    marc2bf -c config1.json --mod=bibframe.plugin records.mrx

Where the contents of config1.json might be:

::

    {
        "plugins": [
            {"id": "https://github.com/uogbuji/pybibframe#linkreport",
            "output-file": "linkreport.html"}
        ]
    }

Which in this case will generate, in addition to the regular outputs
will create a file named ``linkreport.html`` listing any resource fields
in the form of URIs.

Converting MARC/XML to RDF or Versa output (API)
================================================

The ``bibframe.reader.marcxml.bfconvert`` method can be used from APIs
etc to run the conversion.

::

    >>> from bibframe.reader.marcxml import bfconvert
    >>> inputs = open('records.mrx', 'r')
    >>> out = open('resorces.versa.json', 'w')
    >>> bfconvert(inputs=inputs, base='http://example.org', out=out)

See also
========

Some open-source tools for working with BIBFRAME (see
http://bibframe.org)

Note: very useful to have around yaz-marcdump (which e.g. you can use to
conver other MARC formats to MARC/XML)

Download from http://ftp.indexdata.com/pub/yaz/ , unpack then do:

$ ./configure –prefix=$HOME/.local $ make && make install

`MarcEdit`_ can also convert to MARC/XML. Just install, select “MARC
Tools” from the menu, choose your input file, specify an output file,
and specify the conversion you need to perform, e.g. “MARC21->MARC21XML”
for MARC to MARC/XML. Note the availability of the UTF-8 output option
too.

.. _MarcEdit: http://marcedit.reeset.net/
'''

setup(
    name = 'pybibframe',
    version=__version__,
    description = 'Python tools for BIBFRAME (Bibliographic Framework), a Web-friendly framework for bibliographic descriptions in libraries, for example.',
    license = 'License :: OSI Approved :: Apache Software License',
    author = 'Uche Ogbuji',
    author_email = 'uche@ogbuji.net',
    maintainer = 'Zepheira',
    maintainer_email = 'uche@zepheira.com',
    url = 'http://zepheira.com/',
    package_dir={'bibframe': 'lib'},
    packages = ['bibframe', 'bibframe.reader', 'bibframe.writer', 'bibframe.contrib', 'bibframe.plugin'],
    scripts=['exec/marc2bf', 'exec/versa2ttl', 'exec/marcbin2xml'],
    classifiers = [ # From http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        #"Environment :: Other Environment",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Database",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Text Processing :: Markup :: XML",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
    ],
    long_description = LONGDESC
)
