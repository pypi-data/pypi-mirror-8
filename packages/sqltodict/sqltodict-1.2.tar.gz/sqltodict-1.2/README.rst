python-sqldict
==============

.. image:: https://travis-ci.org/RedXBeard/python-sqldict.svg?branch=master
    :target: https://travis-ci.org/RedXBeard/python-sqldict

Raw SQL results returns as dictionary.

Developers who has lots of works on databases, sometimes, especially written raw sql result or in other words selects become to much to handle, so to play with the result of that sqls become pain; columns has to be remembered which index of result list refers which column etc. (ORM usage is fix this issue but has consequences so even if you are using ORM sometimes as said writing raw sqls preferred)

To have a key value pair like dictionaries for sql results will be much more useful, and the pain will become less.

Installation
------------
Using pip library will be installed as following

.. code-block:: bash

  $ pip install sqltodict
  $ pip install psycopg2
  $ pip install mysql-connector-repackaged

Usage for PostgreSQL
--------------------
To play with postgress database, required connection is as following;

.. code-block:: python

  : from sqltodict.connections.postgresqlconnection import PostgreSQLConnection


There are two ways to make class one is giving all required attributes for making the connection;

.. code-block:: python

  : pc = PostgreSQLConnection(sql="""select id, code
                                     from product
                                     limit 10
                                  """,
                              database='template1'
                              user='dbuser'
                              host='localhost'
                              password='dbpass',
                              port=5433)


Other one is; cursor will be already generated and it could be enough to making the class;

.. code-block:: python

  : import psycopg2
  : conn = psycopg2.connect(dbname='template1',
                            user='dbuser',
                            host='localhost',
                            password='dbpass',
                            port=5433)
  : cursor = conn.cursor()
  : pc = PostgreSQLConnection(sql="""select id, code
                                     from product
                                     limit 10
                                  """,
                              cursor=cursor)


Execution is simple as it is;

.. code-block:: python

  : pc.execute_sql()


The result will as following, as default sql select result which is sometimes so hard to continue working.

.. code-block:: python

  : pc.result
  [(62392, '4YAL61165JW'),
   (41308, 'Y14FCD010394'),
   (61397, '4YAL16490IK'),
   (4396, 'W2WCR0040'),
   (61696, '4YAK71063AA'),
   (57895, '4YAK38077PW'),
   (64853, 'V0400710218'),
   (61870, 'Y14LGD021110'),
   (55054, '4YAM19187LK'),
   (61027, '4YAM19698LK')]


For dictionary conversion the sql result will be following, as understandable list.

.. code-block:: python

  : pc.execute_return_as_dict()
  [{'code': '4YAL61165JW', 'id': 62392},
   {'code': 'Y14FCD010394', 'id': 41308},
   {'code': '4YAL16490IK', 'id': 61397},
   {'code': 'W2WCR0040', 'id': 4396},
   {'code': '4YAK71063AA', 'id': 61696},
   {'code': '4YAK38077PW', 'id': 57895},
   {'code': 'V0400710218', 'id': 64853},
   {'code': 'Y14LGD021110', 'id': 61870},
   {'code': '4YAM19187LK', 'id': 55054},
   {'code': '4YAM19698LK', 'id': 61027}]


Usage for MYSQL
---------------
Playing with an mysql database there are slightly differences; starts with import;

.. code-block:: python

    : from sqltodict.connections.mysqlconnection import MYSQLConnection


There are two ways again to make the class usable;

.. code-block:: python

    : mc = MYSQLConnection(sql="""select id, code
                                  from product
                                  limit 10
                               """,
                           database='template1'
                           user='dbuser'
                           host='localhost'
                           password='dbpass',
                           port=3306)


... or in other way is as mentioned before, as following;

.. code-block:: python

    : import mysql.connector
    : conn = mysql.connector.connect(user='root',
                                     password='',
                                     host='localhost',
                                     database='template1',
                                     port=3306)
    : cursor = conn.cursor()
    : mc = MYSQLConnection(sql="""select id, code
                                  from product
                                  limit 10
                               """,
                           cursor=cursor)


Execution is simple if result is wanted as default one;

.. code-block:: python

    : mc.execute_sql()
    : mc.result
    [(62392, '4YAL61165JW'),
     (41308, 'Y14FCD010394'),
     (61397, '4YAL16490IK'),
     (4396, 'W2WCR0040'),
     (61696, '4YAK71063AA'),
     (57895, '4YAK38077PW'),
     (64853, 'V0400710218'),
     (61870, 'Y14LGD021110'),
     (55054, '4YAM19187LK'),
     (61027, '4YAM19698LK')]

If dictionary type of result is requested, directly;

.. code-block:: python

    : mc.execute_return_as_dict()
    [{'code': u'W2WCR0040', 'id': 4396},
     {'code': u'Y14FCD010394', 'id': 41308},
     {'code': u'4YAM19187LK', 'id': 55054},
     {'code': u'4YAK38077PW', 'id': 57895},
     {'code': u'4YAM19698LK', 'id': 61027},
     {'code': u'4YAL16490IK', 'id': 61397},
     {'code': u'4YAK71063AA', 'id': 61696},
     {'code': u'Y14LGD021110', 'id': 61870},
     {'code': u'4YAL61165JW', 'id': 62392},
     {'code': u'V0400710218', 'id': 64853}]
