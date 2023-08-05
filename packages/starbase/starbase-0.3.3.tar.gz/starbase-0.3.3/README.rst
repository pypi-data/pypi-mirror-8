=========================================
starbase
=========================================
HBase Stargate (REST API) client wrapper for Python.

Read the official documentation of the `Stargate <http://wiki.apache.org/hadoop/Hbase/Stargate>`_.

Description
=========================================
starbase is (at the moment) a client implementation of the Apache HBase REST API (Stargate).

What you have to know
=========================================
Beware, that REST API is slow (not to blame on this library!). If you can operate with HBase directly
better do so.

Prerequisites
=========================================
You need to have Hadoop, HBase, Thrift and Stargate running. If you want to make it easy for yourself,
read my instructions on installing Cloudera manager (free) on Ubuntu 12.04 LTS 
`here <http://barseghyanartur.blogspot.nl/2013/08/installing-cloudera-on-ubuntu-1204.html>`_ or
`there <https://bitbucket.org/barseghyanartur/simple-cloudera-install>`_.

Once you have everything installed and running (by default Stargate runs on 127.0.0.1:8000), you should
be able to run `src/starbase/client/test.py` without problems (UnitTest).

Supported Python versions
=========================================
- 2.6.8 and up
- 2.7
- 3.3

Features
=========================================
Project is still in development, thus not all the features of the API are available.

Features implemented
-----------------------------------------
- Connect to Stargate.
- Show software version.
- Show cluster version.
- Show cluster status.
- List tables.
- Retrieve table schema.
- Retrieve table meta data.
- Get a list of tables' column families.
- Create a table.
- Delete a table.
- Alter table schema.
- Insert (PUT) data into a single row (single or multiple columns).
- Update (POST) data of a single row (single or multiple columns).
- Select (GET) a single row from table, optionally with selected columns only.
- Delete (DELETE) a single row by id.
- Batch insert (PUT).
- Batch update (POST).
- Basic HTTP auth is working. You could provide a login and a password to the connection.
- Retrive all rows in a table (table scanning).

Features in-development
-----------------------------------------
- Table scanning.
- Syntax globbing.

Installation
=========================================
Install latest stable version from PyPI.

.. code-block:: none

    $ pip install starbase

Or latest stable version from github.

.. code-block:: none

    $ pip install -e git+https://github.com/barseghyanartur/starbase@stable#egg=starbase

Usage and examples
=========================================
Operating with API starts with making a connection instance.

Required imports
-----------------------------------------
.. code-block:: python

    from starbase import Connection

Create a connection instance
-----------------------------------------
Defaults to 127.0.0.1:8000. Specify ``host`` and ``port`` arguments when creating a connection instance,
if your settings are different.

.. code-block:: python

    c = Connection()

With customisations, would look simlar to the following.

.. code-block:: python

    c = Connection(host='192.168.88.22', port=8001)

Show tables
-----------------------------------------
Assuming that there are two existing tables named ``table1`` and ``table2``, the following would be
printed out.

.. code-block:: python

    c.tables()

Output.

.. code-block:: none

    ['table1', 'table2']

Operating with table schema
-----------------------------------------
Whenever you need to operate with a table (also, if you need to create one), you need to have a table
instance created.

Create a table instance (note, that at this step no table is created).

.. code-block:: python

    t = c.table('table3')

Create a new table
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Assuming that no table named ``table3`` yet exists in the database, create a table named ``table3`` with
columns (column families) ``column1``, ``column2``, ``column3`` (this is the point where the table is
actually created). In the example below, ``column1``, ``column2`` and ``column3`` are column families (in
short - columns). Columns are declared in the table schema.

.. code-block:: python

    t.create('column1', 'column2', 'column3')

Output.

.. code-block:: none

    201

Check if table exists
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

    t.exists()

Output.

.. code-block:: none

    True

Show table columns (column families)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

    t.columns()

Output.

.. code-block:: none

    ['column1', 'column2', 'column3']

Add columns to the table
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Add columns given (``column4``, ``column5``, ``column6``, ``column7``).

.. code-block:: python

    t.add_columns('column4', 'column5', 'column6', 'column7')

Output.

.. code-block:: none

    200

Drop columns from table
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Drop columns given (``column6``, ``column7``).

.. code-block:: python

    t.drop_columns('column6', 'column7')

Output.

.. code-block:: none

    201

Drop entire table schema
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

    t.drop()

Output.

.. code-block:: none

    200

Operating with table data
-----------------------------------------

Insert data into a single row
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
HBase is a key/value store. In HBase columns (also named column families) are part of declared table schema
and have to be defined when a table is created. Columns have qualifiers, which are not declared in the table
schema. Number of column qualifiers is not limited.

Within a single row, a value is mapped by a column family and a qualifier (in terms of key/value store
concept). Value might be anything castable to string (JSON objects, data structures, XML, etc).

In the example below, ``key11``, ``key12``, ``key21``, etc. - are the qualifiers. Obviously, ``column1``,
``column2`` and ``column3`` are column families.

Column families must be composed of printable characters. Qualifiers can be made of any arbitrary bytes.

Table rows are identified by row keys - unique identifiers (UID or so called primary key). In the example
below, ``my-key-1`` is the row key (UID).

То recap all what's said above, HBase maps (row key, column family, column qualifier and timestamp) to a
value.

.. code-block:: python

    t.insert(
        'my-key-1',
        {
            'column1': {'key11': 'value 11', 'key12': 'value 12',
                        'key13': 'value 13'},
            'column2': {'key21': 'value 21', 'key22': 'value 22'},
            'column3': {'key32': 'value 31', 'key32': 'value 32'}
        }
        )

Output.

.. code-block:: none

    200

Note, that you may also use the `native` way of naming the columns and cells (qualifiers). Result of
the following would be equal to the result of the previous example.

.. code-block:: python

    t.insert(
        'my-key-1',
        {
            'column1:key11': 'value 11', 'column1:key12': 'value 12',
            'column1:key13': 'value 13',
            'column2:key21': 'value 21', 'column2:key22': 'value 22',
            'column3:key32': 'value 31', 'column3:key32': 'value 32'
        }
        )

Output.

.. code-block:: none

    200

Update row data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

    t.update(
        'my-key-1',
        {'column4': {'key41': 'value 41', 'key42': 'value 42'}}
        )

Output.

.. code-block:: none

    200

Remove row, row column or row cell data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Remove a row cell (qualifier) data. In the example below, the ``my-key-1`` is table row UID, ``column4``
is the column family and the ``key41`` is the qualifier. Note, that only qualifer data (for the row given)
is being removed. All other possible qualifiers of the column ``column4`` will remain untouched.

.. code-block:: python

    t.remove('my-key-1', 'column4', 'key41')

Output.

.. code-block:: none

    200

Remove a row column (column family) data. Note, that at this point, the entire column data (data of all
qualifiers for the row given) is being removed.

.. code-block:: python

    t.remove('my-key-1', 'column4')

Output.

.. code-block:: none

    200

Remove an entire row data. Note, that in this case, entire row data, along with all columns and qualifiers
for the row given, is being removed.

.. code-block:: python

    t.remove('my-key-1')

Output.

.. code-block:: none

    200

Fetch table data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Fetch a single row data with all columns and qualifiers.

.. code-block:: python

    t.fetch('my-key-1')

Output.

.. code-block:: none

    {
        'column1': {'key11': 'value 11', 'key12': 'value 12', 'key13': 'value 13'},
        'column2': {'key21': 'value 21', 'key22': 'value 22'},
        'column3': {'key32': 'value 31', 'key32': 'value 32'}
    }

Fetch a single row data with selected columns (limit to ``column1`` and ``column2`` columns and all
their qualifiers).

.. code-block:: python

    t.fetch('my-key-1', ['column1', 'column2'])

Output.

.. code-block:: none

    {
        'column1': {'key11': 'value 11', 'key12': 'value 12', 'key13': 'value 13'},
        'column2': {'key21': 'value 21', 'key22': 'value 22'},
    }

Narrow the result set even more (limit to qualifiers ``key1`` and ``key2`` of column ``column1`` and
qualifier ``key32`` of column ``column3``).

.. code-block:: python

    t.fetch('my-key-1', {'column1': ['key11', 'key13'], 'column3': ['key32']})

Output.

.. code-block:: none

    {
        'column1': {'key11': 'value 11', 'key13': 'value 13'},
        'column3': {'key32': 'value 32'}
    }

Note, that you may also use the `native` way of naming the columns and cells (qualifiers). Example
below does exactly the same as example above.

.. code-block:: python

    t.fetch('my-key-1', ['column1:key11', 'column1:key13', 'column3:key32'])

Output.

.. code-block:: none

    {
        'column1': {'key11': 'value 11', 'key13': 'value 13'},
        'column3': {'key32': 'value 32'}
    }

If you set the `perfect_dict` argument to False, you'll get the `native` data structure.

.. code-block:: python

    t.fetch(
        'my-key-1',
        ['column1:key11', 'column1:key13', 'column3:key32'],
        perfect_dict=False
        )

Output.

.. code-block:: none

    {
        'column1:key11': 'value 11',
        'column1:key13': 'value 13',
        'column3:key32': 'value 32'
    }

Batch operations with table data
-----------------------------------------
Batch operations (insert and update) work similar to normal insert and update, but are done in a batch.
You are advised to operate in batch as much as possible.

Batch insert
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In the example below, we will insert 5000 records in a batch.

.. code-block:: python

    data = {
        'column1': {'key11': 'value 11', 'key12': 'value 12', 'key13': 'value 13'},
        'column2': {'key21': 'value 21', 'key22': 'value 22'},
    }
    b = t.batch()
    if b:
        for i in range(0, 5000):
            b.insert('my-key-%s' % i, data)
        b.commit(finalize=True)

Output.

.. code-block:: none

    {'method': 'PUT', 'response': [200], 'url': 'table3/bXkta2V5LTA='}

Batch update
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In the example below, we will update 5000 records in a batch.

.. code-block:: python

    data = {
        'column3': {'key31': 'value 31', 'key32': 'value 32'},
    }
    b = t.batch()
    if b:
        for i in range(0, 5000):
            b.update('my-key-%s' % i, data)
        b.commit(finalize=True)

Output.

.. code-block:: none

    {'method': 'POST', 'response': [200], 'url': 'table3/bXkta2V5LTA='}

Note: The table `batch` method accepts an optional `size` argument (int). If set, an auto-commit is fired
each the time the stack is ``full``.

Table data search (row scanning)
-----------------------------------------
Table scanning is in development (therefore, the scanning API will likely be changed). Result set returned is a
generator.

Fetch all rows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

    t.fetch_all_rows()

Output.

.. code-block:: none

    <generator object results at 0x28e9190>

Fetch rows with a filter given
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

    rf = '{"type": "RowFilter", "op": "EQUAL", "comparator": {"type": "RegexStringComparator", "value": "^row_1.+"}}'
    t.fetch_all_rows(with_row_id=True, filter_string=rf)

Output.

.. code-block:: none

    <generator object results at 0x28e9190>

More information on table operations
=========================================
By default, prior further execution of the `fetch`, `insert`, `update`, `remove` (table row operations)
methods, it's being checked whether the table exists or not. That's safe, but comes in cost of an
extra (light though) HTTP request. If you're absolutely sure you want to avoid those checks, you can
disable them. It's possible to disable each type of row operation, by setting the following properties
of the table instance to False: ``check_if_exists_on_row_fetch``, ``check_if_exists_on_row_insert``,
``check_if_exists_on_row_remove`` and ``check_if_exists_on_row_update``.

.. code-block:: python

    t.check_if_exists_on_row_fetch = False
    t.fetch('row1')

It's also possible to disable
them all at once, by calling the ``disable_row_operation_if_exists_checks`` method of the table instance.

.. code-block:: python

    t.disable_row_operation_if_exists_checks()
    t.remove('row1')

Same goes for table scanner operations. Setting the value of ``check_if_exists_on_scanner_operations``
of a table instance to False, skips the checks for scanner operations.

.. code-block:: python

    t.check_if_exists_on_scanner_operations = False
    t.fetch_all_rows(flat=True)

Exception handling
=========================================
Methods that accept `fail_silently` argument are listed per class below.

starbase.client.connection.Connection
-----------------------------------------
- cluster_version
- cluster_status
- drop_table
- tables
- table_exists
- version

starbase.client.table.Table
-----------------------------------------
- add_columns
- batch
- create
- drop
- drop_columns
- exists
- insert
- fetch
- fetch_all_rows
- regions
- remove
- schema
- update

starbase.client.table.Batch
-----------------------------------------
- commit
- insert
- update

starbase.client.transport.HttpRequest
-----------------------------------------
Class `starbase.client.table.Batch` accepts `fail_silently` as a constructor argument.

More examples
=========================================

Show software version
-----------------------------------------
.. code-block:: python

    print connection.version

Output.

.. code-block:: none

    {u'JVM': u'Sun Microsystems Inc. 1.6.0_43-20.14-b01',
     u'Jersey': u'1.8',
     u'OS': u'Linux 3.5.0-30-generic amd64',
     u'REST': u'0.0.2',
     u'Server': u'jetty/6.1.26'}

Show cluster version
-----------------------------------------
.. code-block:: python

    print connection.cluster_version

Output.

.. code-block:: none

    u'0.94.7'

Show cluster status
-----------------------------------------
.. code-block:: python

    print connection.cluster_status

Output.

.. code-block:: none

    {u'DeadNodes': [],
     u'LiveNodes': [{u'Region': [{u'currentCompactedKVs': 0,
     ...
     u'regions': 3,
     u'requests': 0}

Show table schema
-----------------------------------------
.. code-block:: python

    print table.schema()

Output.

.. code-block:: none

    {u'ColumnSchema': [{u'BLOCKCACHE': u'true',
       u'BLOCKSIZE': u'65536',
     ...
       u'IS_ROOT': u'false',
     u'name': u'messages'}

Print table metadata
-----------------------------------------
.. code-block:: python

    print table.regions()

Failed requests
=========================================
By default, number of retries for a failed request is equal to zero. 
That means, the request isn't being repeated if failed. It's possible
to retry a failed request (for instance, in case of timeouts, etc).

In order to do that, two additional arguments of the
``starbase.client.connection.Connection`` have been introduced:

- retries (int)
- retry_delay (int)

.. code-block:: python

    c = Connection(
        retries = 3, # Retry 3 times
        retry_delay = 5 # Wait for 5 seconds between retries
        )

Beware! Number of retries can cause performance issues (lower
responsiveness) of your application. At the moment, failed requests,
such as deletion of non-existing column, row or a table, are handled
in the same way and would all cause a retry. This likely will change
in future (smarter detection of failures worth to retry a request).

License
=========================================
GPL 2.0/LGPL 2.1

Support
=========================================
For any issues contact me at the e-mail given in the `Author` section.

Author
=========================================
Artur Barseghyan <artur.barseghyan@gmail.com>
