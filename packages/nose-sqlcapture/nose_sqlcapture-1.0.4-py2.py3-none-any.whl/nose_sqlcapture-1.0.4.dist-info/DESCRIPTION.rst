===============================
SQLCapture nose plugin
===============================

Capture SQL queries being generated from a nosetests run

.. image:: https://badge.fury.io/py/nose-sqlcapture.png
    :target: http://badge.fury.io/py/nose-sqlcapture
.. image:: https://travis-ci.org/freshbooks/nose-sqlcapture.svg?branch=master
    :target: https://travis-ci.org/freshbooks/nose-sqlcapture
.. image:: https://pypip.in/d/nose-sqlcapture/badge.png
    :target: https://crate.io/packages/nose-sqlcapture?version=latest

============
Installation
============

Do ```pip install nose-sqlcapture``` in your project.  Your project should already have ```nosetests``` and ```sqlalchemy``` installed.

=====
Usage
=====

```nosetests [other options] --with-sqlcapture --sqlcapture-filename=sql.log --sqlcapture-format=json```

* sqlcapture-filename the output file. Default: /tmp/sqlcapture.log
* sqlcapture-format the format of the log file, either json or plain.  Default: plain


=======
Formats
=======

^^^^^^^^^^^^^
Plain (plain)
^^^^^^^^^^^^^

Output in plain-text form that's meant for human consumption.  The output is of the following format::

    test1
    test2
    SQL1
    ---
    test1
    test3
    SQL2
    ---
    ...


^^^^^^^^^^^
JSON (json)
^^^^^^^^^^^

Ouptut the queries and their corresponding tests in json format::

    {
        SQL1: [test1, test2],
        SQL2: [test1, test3],
        ...
    }




