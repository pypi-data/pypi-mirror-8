__title__ = 'starbase.tests'
__author__ = 'Artur Barseghyan'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'

import threading
import multiprocessing
import unittest
import uuid
import shutil
import os
import binascii

PROJECT_DIR = lambda base : os.path.abspath(os.path.join(os.path.dirname(__file__), base).replace('\\','/'))

from six import text_type, PY3, print_, BytesIO as StringIO

try:
    from six.moves import range as xrange
except ImportError:
    if PY3:
        xrange = range

try:
    from six.moves.urllib.request import build_opener
except ImportError:
    if PY3:
        from urllib.request import build_opener
    else:
        from urllib2 import build_opener

from requests.exceptions import HTTPError

from starbase import Connection, Table
from starbase.exceptions import DoesNotExist, ParseError

HOST = '127.0.0.1'
PORT = 8000
TABLE_NAME = 'messages'
NON_EXISTENT_TABLE_NAME = 'user_stats'

COLUMN_FROM_USER = 'from_user'
FIELD_FROM_USER_ID = 'id'
FIELD_FROM_USER_NAME = 'name'
FIELD_FROM_USER_EMAIL = 'email'
FIELD_FROM_USER_AVATAR = 'avatar'

COLUMN_TO_USER = 'to_user'
FIELD_TO_USER_ID = 'id'
FIELD_TO_USER_NAME = 'name'
FIELD_TO_USER_EMAIL = 'email'
FIELD_TO_USER_AVATAR = 'avatar'

COLUMN_MESSAGE = 'message'
FIELD_MESSAGE_SUBJECT = 'subject'
FIELD_MESSAGE_BODY = 'body'
FIELD_MESSAGE_PRIVATE = 'private'
FIELD_MESSAGE_PRIORITY = 'priority'

TEST_ROW_KEY_1 = 'row1'
TEST_ROW_KEY_2 = 'row2'
TEST_ROW_KEY_3 = 'row3'

TEST_DELETE_TABLE = True
TEST_CREATE_TABLE = True

NUM_ROWS = 10
NUM_THREADS = 8
NUM_PROCESSES = 8

class Registry(object):
    pass

ordering = []

registry = Registry()

PRINT_INFO = True
TRACK_TIME = False

def print_info(func):
    """
    Prints some useful info.
    """
    if not PRINT_INFO:
        return func

    def inner(self, *args, **kwargs):
        if TRACK_TIME:
            import simple_timer
            timer = simple_timer.Timer() # Start timer

        ordering.append(func.__name__)

        result = func(self, *args, **kwargs)

        if TRACK_TIME:
            timer.stop() # Stop timer

        print_('\n\n{0}'.format(func.__name__))
        print_('============================')
        if func.__doc__:
            print_('""" {0} """'.format(func.__doc__.strip()))
        print_('----------------------------')
        if result is not None:
            print_(result)
        if TRACK_TIME:
            print_('done in {0} seconds'.format(timer.duration))
        print_('\n++++++++++++++++++++++++++++')

        return result
    return inner

class StarbaseClient01ConnectionTest(unittest.TestCase):
    """
    Starbase Connection tests.
    """
    def setUp(self):
        self.connection = Connection(HOST, PORT, content_type='json')
        self.table = self.connection.table(TABLE_NAME)

    @print_info
    def test_01_version(self):
        res = self.connection.version
        self.assertTrue(isinstance(res, dict))
        return res

    @print_info
    def test_02_cluster_version(self):
        res = self.connection.cluster_version

        self.assertTrue(isinstance(res, text_type))

        return res

    @print_info
    def test_03_cluster_status(self):
        res = self.connection.cluster_status
        self.assertTrue(isinstance(res, dict))
        return res

    if TEST_DELETE_TABLE:
        @print_info
        def test_04_drop_table_schema(self):
            """
            Delete table schema. Deleting the table if it exists. After that
            checking if table still exists.
            """
            # First testing for non-existent table
            non_existent_res = self.connection.table('non-existent-table').drop()
            self.assertEqual(503, non_existent_res)

            res = None
            if self.connection.table_exists(TABLE_NAME):
                res = self.connection.table(TABLE_NAME).drop()
                self.assertEqual(200, res) # Checking the status code
                self.assertTrue(not self.connection.table_exists(TABLE_NAME)) # Checking for physical existence

            return non_existent_res, res

    if TEST_CREATE_TABLE:
        @print_info
        def test_05_create_table_schema(self):
            """
            Create table schema. After creating the table we just check if it exists.
            """
            # Success tests
            res = None
            if not self.connection.table_exists(TABLE_NAME):
                columns = [COLUMN_FROM_USER, COLUMN_TO_USER, COLUMN_MESSAGE]

                res = self.connection.table(TABLE_NAME).create(*columns)

            self.assertTrue(self.connection.table_exists(TABLE_NAME))

            # Now trying to create a table even if it exists.
            columns = [COLUMN_FROM_USER, COLUMN_TO_USER, COLUMN_MESSAGE]
            res_fail = self.connection.table(TABLE_NAME).create(*columns)
            self.assertEqual(res_fail, False)

            return res, res_fail

    @print_info
    def test_06_get_table_schema(self):
        """
        Get table schema.
        """
        # First testing for non existent table
        non_existent_table = self.connection.table('non-existent-table')
        self.assertTrue(non_existent_table.schema() is None)

        # Now for existing one
        res = self.table.schema()
        self.assertTrue(res is not None)
        return non_existent_table, res

    @print_info
    def test_07_table_list(self):
        res = self.connection.tables()
        self.assertTrue(isinstance(res, list))

        self.assertTrue(TABLE_NAME in res)
        return res


class StarbaseClient02TableTest(unittest.TestCase):
    """
    Starbase Table tests.
    """
    def setUp(self):
        self.connection = Connection(HOST, PORT, content_type='json')
        self.table = self.connection.table(TABLE_NAME)

    @print_info
    def test_01_columns_list(self):
        res = self.table.columns()
        self.assertTrue(isinstance(res, list))

        self.assertTrue(COLUMN_FROM_USER in res)
        self.assertTrue(COLUMN_TO_USER in res)
        self.assertTrue(COLUMN_MESSAGE in res)
        return res

    @print_info
    def test_02_table_put_multiple_column_data(self, process_number=0, perfect_dict=False):
        """
        Insert multiple-colums into a single row of HBase using Stagate REST API using normal dict as input.
        """
        # Success test
        key = 'row_{0}_{1}'.format(('perfect_' if perfect_dict else ''), str(uuid.uuid4()))

        columns = {}

        if perfect_dict:
            columns = {
                COLUMN_FROM_USER: {
                    FIELD_FROM_USER_ID: '123',
                    FIELD_FROM_USER_NAME: 'John Doe',
                    FIELD_FROM_USER_EMAIL: 'john@doe.com'
                },
                COLUMN_TO_USER: {
                    FIELD_TO_USER_ID: '456',
                    FIELD_TO_USER_NAME: 'Lorem Ipsum',
                    FIELD_TO_USER_EMAIL: 'lorem@ipsum.com'
                },
                COLUMN_MESSAGE: {
                    FIELD_MESSAGE_SUBJECT: 'Lorem ipsum',
                    FIELD_MESSAGE_BODY: 'Lorem ipsum dolor sit amet.'
                },
            }
        else:
            columns = {
                '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_ID): '123',
                '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_NAME): 'John Doe',
                '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_EMAIL): 'john@doe.com',
                '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_ID): '456',
                '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_NAME): 'Lorem Ipsum',
                '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_EMAIL): 'lorem@ipsum.com',
                '{0}:{1}'.format(COLUMN_MESSAGE, FIELD_MESSAGE_SUBJECT): 'Lorem ipsum',
                '{0}:{1}'.format(COLUMN_MESSAGE, FIELD_MESSAGE_BODY): 'Lorem ipsum dolor sit amet.'
            }

        res = self.table.insert(key, columns)
        self.assertEqual(res, 200)
        return res

    def test_03_table_put_multiple_column_data_normal_dict(self, process_number=0):
        """
        Insert multiple-colums into a single row of HBase using Stagate REST API using perfect dict as input.
        """
        return self.test_02_table_put_multiple_column_data(process_number=process_number, perfect_dict=True)

    @print_info
    def test_04_table_batch_put_multiple_column_data(self, process_number=0, perfect_dict=False):
        """
        Insert multiple-colums in batch into a HBase using Stagate REST API using normal dict as input.
        """
        batch = self.table.batch()

        keys = []
        for i in range(0, NUM_ROWS):
            key = 'row_{0}_{1}'.format(('perfect_' if perfect_dict else ''), str(uuid.uuid4()))
            keys.append(key)

            columns = {}

            if perfect_dict:
                columns = {
                    COLUMN_FROM_USER: {
                        FIELD_FROM_USER_ID: '123',
                        FIELD_FROM_USER_NAME: 'John Doe',
                        FIELD_FROM_USER_EMAIL: 'john@doe.com'
                    },
                    COLUMN_TO_USER: {
                        FIELD_TO_USER_ID: '456',
                        FIELD_TO_USER_NAME: 'Lorem Ipsum',
                        FIELD_TO_USER_EMAIL: 'lorem@ipsum.com'
                    },
                    COLUMN_MESSAGE: {
                        FIELD_MESSAGE_SUBJECT: 'Lorem ipsum',
                        FIELD_MESSAGE_BODY: 'Lorem ipsum dolor sit amet.'
                    },
                }
            else:
                columns = {
                    '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_ID): '123',
                    '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_NAME): 'John Doe',
                    '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_EMAIL): 'john@doe.com',
                    '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_ID): '456',
                    '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_NAME): 'Lorem Ipsum',
                    '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_EMAIL): 'lorem@ipsum.com',
                    '{0}:{1}'.format(COLUMN_MESSAGE, FIELD_MESSAGE_SUBJECT): 'Lorem ipsum',
                    '{0}:{1}'.format(COLUMN_MESSAGE, FIELD_MESSAGE_BODY): 'Lorem ipsum dolor sit amet.'
                }

            batch.insert(key, columns)

        res = batch.commit(finalize=True)
        self.assertEqual(res.get('response', None), [200])
        registry.keys = keys
        return res

    def test_05_table_batch_put_multiple_column_data_perfect_dict(self, process_number=0):
        """
        Insert multiple-colums in batch into a HBase using Stagate REST API using perfect dict as input.
        """
        return self.test_04_table_batch_put_multiple_column_data(process_number=process_number, perfect_dict=True)

    @print_info
    def test_06_table_batch_post_multiple_column_data(self, process_number=0, perfect_dict=False):
        """
        Update multiple-colums in batch into a HBase using Stagate REST API using normal dict as input.
        """
        # Updating the records inserted by `test_04_table_batch_put_multiple_column_data` and
        # `test_05_table_batch_put_multiple_column_data_perfect_dict`.
        batch = self.table.batch()

        for key in registry.keys:
            columns = {}

            if perfect_dict:
                columns = {
                    COLUMN_FROM_USER: {
                        FIELD_FROM_USER_AVATAR: '://example.com/avatar_from_user.jpg',
                    },
                    COLUMN_TO_USER: {
                        FIELD_TO_USER_AVATAR: '://example.com/avatar_to_user.jpg',
                    },
                    COLUMN_MESSAGE: {
                        FIELD_MESSAGE_PRIVATE: '1',
                        FIELD_MESSAGE_PRIORITY: 'high'
                    },
                }
            else:
                columns = {
                    '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_AVATAR): '://example.com/avatar_from_user.jpg',
                    '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_AVATAR): '://example.com/avatar_to_user.jpg',
                    '{0}:{1}'.format(COLUMN_MESSAGE, FIELD_MESSAGE_PRIVATE): '1',
                    '{0}:{1}'.format(COLUMN_MESSAGE, FIELD_MESSAGE_PRIORITY): 'high'
                }

            batch.update(key, columns)

        res = batch.commit(finalize=True)
        self.assertEqual(res.get('response', None), [200])


        if perfect_dict:
            output = {
                COLUMN_FROM_USER: {
                    FIELD_FROM_USER_ID: '123',
                    FIELD_FROM_USER_NAME: 'John Doe',
                    FIELD_FROM_USER_EMAIL: 'john@doe.com',
                    FIELD_FROM_USER_AVATAR: '://example.com/avatar_from_user.jpg',
                },
                COLUMN_TO_USER: {
                    FIELD_TO_USER_ID: '456',
                    FIELD_TO_USER_NAME: 'Lorem Ipsum',
                    FIELD_TO_USER_EMAIL: 'lorem@ipsum.com',
                    FIELD_TO_USER_AVATAR: '://example.com/avatar_to_user.jpg',
                },
                COLUMN_MESSAGE: {
                    FIELD_MESSAGE_SUBJECT: 'Lorem ipsum',
                    FIELD_MESSAGE_BODY: 'Lorem ipsum dolor sit amet.',
                    FIELD_MESSAGE_PRIVATE: '1',
                    FIELD_MESSAGE_PRIORITY: 'high'
                }
            }
        else:
            output = {
                '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_ID): '123',
                '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_NAME): 'John Doe',
                '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_EMAIL): 'john@doe.com',
                '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_AVATAR): '://example.com/avatar_from_user.jpg',
                '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_ID): '456',
                '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_NAME): 'Lorem Ipsum',
                '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_EMAIL): 'lorem@ipsum.com',
                '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_AVATAR): '://example.com/avatar_to_user.jpg',
                '{0}:{1}'.format(COLUMN_MESSAGE, FIELD_MESSAGE_SUBJECT): 'Lorem ipsum',
                '{0}:{1}'.format(COLUMN_MESSAGE, FIELD_MESSAGE_BODY): 'Lorem ipsum dolor sit amet.',
                '{0}:{1}'.format(COLUMN_MESSAGE, FIELD_MESSAGE_PRIVATE): '1',
                '{0}:{1}'.format(COLUMN_MESSAGE, FIELD_MESSAGE_PRIORITY): 'high'
            }

        # Now testing the data
        rows = []
        for key in registry.keys:
            row = self.table.fetch(key, perfect_dict=perfect_dict)
            self.assertEqual(row, output)
            rows.append(row)

        return res

    def test_07_table_batch_post_multiple_column_data_perfect_dict(self, process_number=0):
        """
        Update multiple-colums in batch into a HBase using Stagate REST API using perfect dict as input.
        """
        return self.test_06_table_batch_post_multiple_column_data(process_number=process_number, perfect_dict=True)

    def __table_put_column_data_2(self, key, num_rows):
        res = []

        for i in xrange(num_rows):
            columns = {
                '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_ID): str(11 * (i + 1)),
                '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_NAME): 'John Doe',
                '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_EMAIL): 'john@doe.net',
                '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_ID): str(22 * (i + 1)),
                '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_NAME): 'Lorem Ipsum',
                '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_EMAIL): 'lorem@ipsum.net',
                '{0}:{1}'.format(COLUMN_MESSAGE, FIELD_MESSAGE_SUBJECT): 'Lorem ipsum',
                '{0}:{1}'.format(COLUMN_MESSAGE, FIELD_MESSAGE_BODY): 'Lorem ipsum dolor sit amet.',
                }
            res.append(self.table.insert('{0}{1}'.format(key, i), columns))

        return res

    @print_info
    def test_08_table_put_column_data(self, process_number=0):
        """
        Insert single column data into a single row of HBase using starbase REST API.
        """
        key = 'row_1_'
        num_rows = NUM_ROWS

        res = self.__table_put_column_data_2(key, num_rows)

        self.assertEqual(res, [200 for i in xrange(num_rows)])
        return res

    @print_info
    def test_09_table_put_column_data(self, process_number=0):
        """
        Insert single column data into a single row of HBase using starbase REST API.

        ..note: Used in ``test_13_table_post_column_data``.
        """
        key = 'row_1_abcdef'

        columns = {
            '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_ID): '110',
            '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_NAME): 'John Doe',
            '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_EMAIL): 'john@doe.net',
            #'{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_ID): '220',
            #'{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_NAME): 'Lorem Ipsum',
            #'{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_EMAIL): 'lorem@ipsum.net',
            #'{0}:{1}'.format(COLUMN_MESSAGE, FIELD_MESSAGE_SUBJECT): 'Lorem ipsum',
            #'{0}:{1}'.format(COLUMN_MESSAGE, FIELD_MESSAGE_BODY): 'Lorem ipsum dolor sit amet.',
            }
        res = self.table.insert(key, columns)
        self.assertEqual(res, 200)
        return res

    def __table_put_column_data(self, key='row_2_abcdef'):
        columns = {
            '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_ID): '110',
            '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_NAME): 'John Doe',
            '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_EMAIL): 'john@doe.net',
            '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_ID): '220',
            '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_NAME): 'Lorem Ipsum',
            '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_EMAIL): 'lorem@ipsum.net',
            '{0}:{1}'.format(COLUMN_MESSAGE, FIELD_MESSAGE_SUBJECT): 'Lorem ipsum',
            '{0}:{1}'.format(COLUMN_MESSAGE, FIELD_MESSAGE_BODY): 'Lorem ipsum dolor sit amet.',
            }
        res = self.table.insert(key, columns)
        return res

    @print_info
    def test_10_table_put_column_data(self, process_number=0):
        """
        Insert multiple column data into a single row of HBase using starbase REST API.

        ..note: Used in ``test_11_get_single_row_with_all_columns`` and ``test_08b_get_single_row_with_all_columns``.
        """
        key = 'row_2_abcdef'

        res = self.__table_put_column_data(key)
        self.assertEqual(res, 200)
        return res

    @print_info
    def test_11_get_single_row_with_all_columns(self, row_key='row_2_abcdef__11'):
        """
        Fetches a single row from HBase using starbase REST API with all columns of that row as simple dict.
        """
        self.__table_put_column_data(row_key)

        res = self.table.fetch(row=row_key, perfect_dict=False)
        output = {
            'from_user:id': '110',
            'from_user:name': 'John Doe',
            'from_user:email': 'john@doe.net',
            'message:body': 'Lorem ipsum dolor sit amet.',
            'message:subject': 'Lorem ipsum',
            'to_user:id': '220',
            'to_user:name': 'Lorem Ipsum',
            'to_user:email': 'lorem@ipsum.net'
        }
        self.assertEqual(res, output)
        return res

    @print_info
    def test_16_get_single_row_with_all_columns_as_perfect_dict(self, row_key='row_2_abcdef__16'):
        """
        Fetches a single row from HBase using starbase REST API with all columns of that row as perfect dict.
        """
        self.__table_put_column_data(row_key)

        res = self.table.fetch(row=row_key, perfect_dict=True)
        output = {
            'to_user': {'id': '220', 'name': 'Lorem Ipsum', 'email': 'lorem@ipsum.net'},
            'message': {'body': 'Lorem ipsum dolor sit amet.', 'subject': 'Lorem ipsum'},
            'from_user': {'id': '110', 'name': 'John Doe', 'email': 'john@doe.net'}
        }
        self.assertEqual(res, output)
        return res

    @print_info
    def test_13_table_post_column_data(self, process_number=0):
        """
        Updates (POST) data of a single row of HBase using starbase REST API. Updates data set in
        ``test_09_table_put_column_data``.
        """
        # TODO: This is not a well done test.

        key = 'row_1_abcdef'

        columns = {
            #'{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_ID): '110',
            #'{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_NAME): 'John Doe',
            #'{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_EMAIL): 'john@doe.net',
            '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_ID): '220',
            '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_NAME): 'Lorem Ipsum',
            '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_EMAIL): 'lorem@ipsum.net',
            '{0}:{1}'.format(COLUMN_MESSAGE, FIELD_MESSAGE_SUBJECT): 'Lorem ipsum',
            '{0}:{1}'.format(COLUMN_MESSAGE, FIELD_MESSAGE_BODY): 'Lorem ipsum dolor sit amet.',
            }

        output = {
            '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_ID): '110',
            '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_NAME): 'John Doe',
            '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_EMAIL): 'john@doe.net',
            '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_ID): '220',
            '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_NAME): 'Lorem Ipsum',
            '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_EMAIL): 'lorem@ipsum.net',
            '{0}:{1}'.format(COLUMN_MESSAGE, FIELD_MESSAGE_SUBJECT): 'Lorem ipsum',
            '{0}:{1}'.format(COLUMN_MESSAGE, FIELD_MESSAGE_BODY): 'Lorem ipsum dolor sit amet.',
            }
        res = self.table.insert(key, columns)

        #print_('expected output: ', output)

        check_response = self.table.fetch(row=key, perfect_dict=False)

        #print_('response received: ', check_response)
        return res

    @print_info
    def test_14_get_single_row_with_all_columns(self, row_key='row_1_abcdef__14'):
        """
        Fetches a single row from HBase using starbase REST API with all columns of that row.
        """
        self.__table_put_column_data(row_key)

        res = self.table.fetch(row=row_key, perfect_dict=True)
        output = {
            'to_user': {'id': '220', 'email': 'lorem@ipsum.net', 'name': 'Lorem Ipsum'},
            'message': {'body': 'Lorem ipsum dolor sit amet.',
            'subject': 'Lorem ipsum'},
            'from_user': {'id': '110', 'name': 'John Doe', 'email': 'john@doe.net'}
        }
        self.assertEqual(res, output)
        return res

    @print_info
    def test_15_table_delete_rows_one_by_one(self, process_number=0):
        """
        Insert single column data into a single row of HBase using starbase REST API. Deletes data set by
        ``test_08_table_put_column_data`` (all except the last record)..
        """
        key = 'row_1_15_'
        res = []
        num_rows = NUM_ROWS - 1

        res2 = self.__table_put_column_data_2(key, num_rows)

        output = []
        for i in xrange(num_rows):
            #columns = {
            #    '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_ID): str(11 * (i + 1)),
            #    }
            res.append(self.table.remove('{0}{1}'.format(key, i)))
            output.append(200)

        self.assertEqual(res, output)

        return res

    @print_info
    def test_16_get_single_row_with_all_columns(self, row_key='row_1_9'):
        """
        Fetches a single row from HBase using starbase REST API with all columns of that row.
        """
        res = self.table.fetch(row=row_key, perfect_dict=True)
        output = {
            'to_user': {'id': '220', 'email': 'lorem@ipsum.net', 'name': 'Lorem Ipsum'},
            'message': {'body': 'Lorem ipsum dolor sit amet.', 'subject': 'Lorem ipsum'},
            'from_user': {'id': '110', 'email': 'john@doe.net', 'name': 'John Doe'}
        }
        self.assertEqual(res, output)

        return res

    @print_info
    def test_17_get_single_row_with_selective_columns(self, row_key='row_1_9_17'):
        """
        Fetches a single row selective columns from HBase using starbase REST API.
        """
        # TODO: This is not a well done test.

        self.__table_put_column_data(row_key)

        # Columns to fetch (normal list)
        columns = [
            '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_ID),
            #'{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_NAME),
            #'{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_EMAIL),

            '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_ID),
            #'{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_NAME),
            #'{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_EMAIL),

            #'{0}:{1}'.format(COLUMN_MESSAGE, FIELD_MESSAGE_SUBJECT),
            #'{0}:{1}'.format(COLUMN_MESSAGE, FIELD_MESSAGE_BODY),
        ]

        # Get table row data
        res = self.table.fetch(row=row_key, columns=columns, perfect_dict=True)

        return res

    @print_info
    def test_18_get_single_row_with_selective_columns(self, row_key='row_1_9'):
        """
        Fetches a single row selective columns from HBase using starbase REST API.
        """
        t = self.connection.table('register')
        t.create('users', 'groups', 'sites', 'messages')

        data = {
            'users': {'id': '1', 'name': 'Artur Barseghyan', 'email': 'artur.barseghyan@gmail.com'},
            'groups': {'id': '1', 'name': 'admins'},
            'sites': {'url': ['http://foreverchild.info', 'http://delusionalinsanity.com']},
        }

        # Note, that since we're inserting a structure into HBase cell, it's automatically turned into a string.
        # In this case the data inserted won't be equal to the data fetched.
        output_data = {
            'users': {'email': 'artur.barseghyan@gmail.com', 'name': 'Artur Barseghyan', 'id': '1'},
            'groups': {'id': '1', 'name': 'admins'},
            'sites': {'url': "['http://foreverchild.info', 'http://delusionalinsanity.com']"}
        }

        res = t.insert('aaa', data)

        self.assertEqual(res, 200)

        # Getting entire row
        res = t.fetch('aaa')
        self.assertEqual(res, output_data)

        # Getting selected columns
        res = t.fetch('aaa', ['users', 'groups'])
        self.assertEqual(res, {'users': data['users'], 'groups': data['groups']})

        # Getting selected cells only
        res = t.fetch('aaa', {'users': ['id', 'email'], 'sites': ['url']})
        output_data['users'].pop('name')
        output_data.pop('groups')
        self.assertEqual(res, output_data)

        return res

    @print_info
    def test_19_table_get_all_rows(self, raw=True, perfect_dict=True):
        """
        Get all rows.
        """
        data1 = {'from_user': {'id': 'ku', 'name': 'tra'}, 'to_user': {'order': '2', 'she': '1'}}
        self.table.insert('papa', data1)
        data2 = {'from_user': {'id': 'zu', 'name': 'za'}, 'to_user': {'genius': 'yep', 'she': 'likes'}}
        self.table.insert('mama', data2)

        res = list(self.table.fetch_all_rows(perfect_dict=perfect_dict))
        self.assertEqual(res[0]['to_user'], data2['to_user'])
        self.assertEqual(res[1]['from_user'], data1['from_user'])
        return res

    @print_info
    def test_19b_table_get_all_rows_with_filter(self, raw=True, perfect_dict=True):
        """
        Get all rows with filter string
        """
        data = {
            'row_1_9': {'to_user': {'email': 'lorem@ipsum.net', 'name': 'Lorem Ipsum', 'id': '220'},
            'message': {'body': 'Lorem ipsum dolor sit amet.', 'subject': 'Lorem ipsum'},
            'from_user': {'email': 'john@doe.net', 'name': 'John Doe', 'id': '110'}}
        }

        key_prefix = 'pow_1'

        for i in xrange(20):
            self.table.insert('{0}_{1}'.format(key_prefix, i), data)

        row_filter_string = '{{"type": "RowFilter", "op": "EQUAL", "comparator": {{"type": "RegexStringComparator", "value": "^{0}.+" }}}}'.format(key_prefix)

        res = list(self.table.fetch_all_rows(with_row_id=True, perfect_dict=perfect_dict, filter_string=row_filter_string))

        for row in res:
            self.assertEqual(row, data)
            break

        return res

    @print_info
    def test_19c_table_get_all_rows_with_scanner_config(self, raw=True, perfect_dict=True):
        """
        Get all rows with scanner config
        """
        data = {
            'row_1_9_19': {'to_user': {'email': 'lorem@ipsum.net', 'name': 'Lorem Ipsum', 'id': '220'},
            'message': {'body': 'Lorem ipsum dolor sit amet.', 'subject': 'Lorem ipsum'},
            'from_user': {'email': 'john@doe.net', 'name': 'John Doe', 'id': '110'}}
        }

        key_prefix = 'bow_1'

        for i in xrange(20):
            self.table.insert('{0}_{1}'.format(key_prefix, i), data)

        scanner_config = '<Scanner maxVersions="1"><filter>{{"op":"EQUAL", "type":"RowFilter", "comparator":{{"value":"^{0}.+","type":"RegexStringComparator"}}}}</filter></Scanner>'.format(key_prefix)

        res = list(self.table.fetch_all_rows(with_row_id=True, perfect_dict=perfect_dict, scanner_config=scanner_config))

        for row in res:
            self.assertEqual(row, data)
            break

        return res

    #@print_info
    def test_20_table_put_multiple_column_data_in_multithreading(self, number_of_threads=NUM_THREADS):
        """
        Speed test.
        """
        def local_test():
            key = 'row_1_'
            results = []
            num_rows = NUM_ROWS

            for i in xrange(num_rows):
                columns = {
                    '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_ID): str(11 * (i + 1)),
                    '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_NAME): 'John Doe',
                    '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_EMAIL): 'john@doe.net',
                    '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_ID): str(22 * (i + 1)),
                    '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_NAME): 'Lorem Ipsum',
                    '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_EMAIL): 'lorem@ipsum.net',
                    '{0}:{1}'.format(COLUMN_MESSAGE, FIELD_MESSAGE_SUBJECT): 'Lorem ipsum',
                    '{0}:{1}'.format(COLUMN_MESSAGE, FIELD_MESSAGE_BODY): 'Lorem ipsum dolor sit amet.',
                    }
                results.append(self.table.insert('{0}{1}'.format(key, i), columns))
            return results

        import simple_timer
        timer = simple_timer.Timer()

        threads = []

        for thread_number in xrange(number_of_threads):
            t = threading.Thread(target=local_test, args=[])
            threads.append(t)
            t.start()

        [t.join() for t in threads]

        print_('test_20_table_put_multiple_column_data_in_multithreading')
        print_("==============================")
        print_('{0} records inserted in total'.format(number_of_threads * NUM_ROWS))
        print_("total number of threads {0}".format(number_of_threads))
        print_("{0} seconds elapsed".format(timer.stop_and_return_duration()))
        print_("making it {0} of records inserted per second\n".format(number_of_threads * NUM_ROWS / timer.duration))

    @print_info
    def test_21_table_delete_row(self):
        """
        Delete row.
        """
        # First create a row.
        row = 'aaa'
        data = {
            COLUMN_MESSAGE: {FIELD_MESSAGE_SUBJECT: 'subject aaa', FIELD_MESSAGE_BODY: 'body aaa'},
            COLUMN_FROM_USER: {FIELD_FROM_USER_ID: '1', FIELD_FROM_USER_NAME: 'fr@m.com'}
        }
        res = self.table.insert(row, data)
        self.assertEqual(res, 200)

        # Get the row and make sure the result is equal
        res = self.table.fetch(row)
        self.assertEqual(res, data)

        # Now first delete the single cell from the row.
        res = self.table.remove(row, COLUMN_MESSAGE, FIELD_MESSAGE_SUBJECT)
        self.assertEqual(res, 200)

        # Make sure it's definitely gone
        res = self.table.fetch(row)
        data[COLUMN_MESSAGE].pop(FIELD_MESSAGE_SUBJECT) # Remove the element
        self.assertEqual(res, data)

        # Now deleting entire column
        res = self.table.remove(row, COLUMN_FROM_USER)
        self.assertEqual(res, 200)

        # Make sure it's definitely gone
        res = self.table.fetch(row)
        data.pop(COLUMN_FROM_USER) # Remove the element
        self.assertEqual(res, data)

        # Delete entire row
        res = self.table.remove(row)
        self.assertEqual(res, 200)

        # Make sure it's definitely gone
        res = self.table.fetch(row)
        self.assertTrue(not res)

        return res

    @print_info
    def test_22_alter_table(self):
        """
        Testing altering the table (add/remove columns).
        """
        # First creating a new table
        t = self.connection.table('new_table')

        if t.exists():
            t.drop()

        res = t.create('first_col', 'second_col', 'third_col')
        self.assertEqual(res, 201)

        # Make sure it's barely there
        res = t.columns()
        res.sort()
        cols = ['first_col', 'second_col', 'third_col']
        cols.sort()
        self.assertEqual(res, cols)

        # Now add more columns
        res = t.add_columns('fourth', 'fifth')
        self.assertEqual(res, 200)

        # Make sure it's barely there
        res = t.columns()
        res.sort()
        cols = ['first_col', 'second_col', 'third_col', 'fourth', 'fifth']
        cols.sort()
        self.assertEqual(res, cols)

        return res

    def __set_test_23_data(self):
        """
        Not a test. Just sets some data for test #23 ``test_23_test_extract_usable_data_as_perfect_dict``.
        """
        # ***************** Input data *******************
        self.sample_1 = {
               "Row": {
                  "key": "key1",
                  "Cell": {
                     "column": "ColFam:Col1",
                     "$": "someData"
                  }
               }
            }

        self.sample_2 = {
               "Row":
                  {
                     "key": "key1",
                     "Cell": [
                        {
                           "column": "ColFam:Col1",
                           "$": "someData"
                        },
                        {
                           "column": "ColFam:Col2",
                           "$": "moreData"
                        }
                     ]
                  }
            }

        self.sample_3 = {
               "Row":[
                  {
                     "key": "key1",
                     "Cell": [
                        {
                           "column": "ColFam:Col1",
                           "$": "someData"
                        },
                        {
                           "column": "ColFam:Col2",
                           "$": "moreData"
                        },
                     ]
                  },
                  {
                     "key": "key2",
                     "Cell": [
                        {
                           "column": "ColFam:Col1",
                           "$": "someData2"
                        },
                        {
                           "column": "ColFam:Col2",
                           "$": "moreData2"
                        },
                     ]
                  }

               ]
            }

        self.sample_4 = {
            'Row': {
                'Cell': [
                    {'column': '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_ID), \
                     'timestamp': '1369247627546', '$': '123'},
                    {'column': '{0}:{1}'.format(COLUMN_FROM_USER, FIELD_FROM_USER_EMAIL), \
                     'timestamp': '1369247627546', '$': 'john@doe.com'},
                    {'column': '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_ID), \
                     'timestamp': '1369247627546', '$': '345'},
                    {'column': '{0}:{1}'.format(COLUMN_TO_USER, FIELD_TO_USER_EMAIL), \
                     'timestamp': '1369247627546', '$': 'lorem@ipsum.com'},
                ],
                'key': 'row81d70d7c-8f30-42fd-be1c-772308b25889908'
            }
        }

        # ***************** Expected output data *******************
        self.sample_1_output_pd = {'ColFam': {'Col1': 'someData'}}

        self.sample_2_output_pd = {'ColFam': {'Col2': 'moreData', 'Col1': 'someData'}}

        self.sample_3_output_pd = [
            {'ColFam': {'Col2': 'moreData', 'Col1': 'someData'}},
            {'ColFam': {'Col2': 'moreData2', 'Col1': 'someData2'}}
        ]

        self.sample_4_output_pd = {
            'to_user': {'id': '345', 'email': 'lorem@ipsum.com'},
            'from_user': {'id': '123', 'email': 'john@doe.com'}
        }

        self.sample_1_output = {'ColFam:Col1': 'someData'}

        self.sample_2_output = {'ColFam:Col1': 'someData', 'ColFam:Col2': 'moreData'}

        self.sample_3_output = [
            {'ColFam:Col1': 'someData', 'ColFam:Col2': 'moreData'},
            {'ColFam:Col1': 'someData2', 'ColFam:Col2': 'moreData2'}
        ]

        self.sample_4_output = {
            'to_user:id': '345',
            'from_user:id': '123',
            'to_user:email': 'lorem@ipsum.com',
            'from_user:email': 'john@doe.com'
        }

    @print_info
    def test_23_test_extract_usable_data_as_perfect_dict(self):
        """
        Test ``_extract_usable_data`` method of ``starbase.client.Table`` as perfect dict.
        """
        self.__set_test_23_data()

        r1 = Table._extract_usable_data(self.sample_1, perfect_dict=True)
        self.assertEqual(r1, self.sample_1_output_pd)

        r2 = Table._extract_usable_data(self.sample_2, perfect_dict=True)
        self.assertEqual(r2,self.sample_2_output_pd)

        r3 = Table._extract_usable_data(self.sample_3, perfect_dict=True)
        self.assertEqual(r3,self.sample_3_output_pd)

        r4 = Table._extract_usable_data(self.sample_4, perfect_dict=True)
        self.assertEqual(r4, self.sample_4_output_pd)

        return (r1, r2, r3, r4)

    @print_info
    def test_24_test_extract_usable_data(self):
        """
        Test ``_extract_usable_data`` method of ``starbase.client.Table`` as normal dict.
        """
        self.__set_test_23_data()

        r1 = Table._extract_usable_data(self.sample_1, perfect_dict=False)
        self.assertEqual(r1, self.sample_1_output)

        r2 = Table._extract_usable_data(self.sample_2, perfect_dict=False)
        self.assertEqual(r2, self.sample_2_output)

        r3 = Table._extract_usable_data(self.sample_3, perfect_dict=False)
        self.assertEqual(r3, self.sample_3_output)

        r4 = Table._extract_usable_data(self.sample_4, perfect_dict=False)
        self.assertEqual(r4,self.sample_4_output)

        return (r1, r2, r3, r4)

    def __insert_binary_file(self, url):
        """
        Insert a binary file. First download the file and then insert.
        """
        opener = build_opener()
        page = opener.open(url)
        image = binascii.b2a_hex(page.read())
        return image.decode()

    @print_info
    def test_25_insert_binary_file(self):
        """
        Store binary file.
        """
        # Write binary file into HBase
        url = 'https://raw.github.com/barseghyanartur/delusionalinsanity.images/master/images/32013_394119419025_539104025_3916154_3598710_n.jpg'
        image = self.__insert_binary_file(url)

        data = {
            COLUMN_MESSAGE: {'text': 'John', 'new': 'yes', 'image': image},
            COLUMN_FROM_USER: {'id': '555', 'email': 'fr@m.com'},
        }

        row_key = 'image_test_1'
        write_res = self.table.insert(row_key, data)

        self.assertEqual(write_res, 200)

        # Get file from HBase and compare source
        read_res = self.table.fetch(row_key, {COLUMN_MESSAGE: ['image']})

        self.assertEqual(read_res[COLUMN_MESSAGE]['image'], image)

        f = open('file.jpg', 'wb')
        f.write(binascii.a2b_hex(read_res[COLUMN_MESSAGE]['image']))

    def __insert_row_into_non_existing_table(self, fail_silently=True):
        """
        Insert row into non-existing table.
        """
        # Success test
        perfect_dict = True

        key = 'row_{0}_{1}'.format(('perfect_' if perfect_dict else ''), str(uuid.uuid4()))

        columns = {
            COLUMN_FROM_USER: {
                FIELD_FROM_USER_ID: '123',
                FIELD_FROM_USER_NAME: 'John Doe',
                FIELD_FROM_USER_EMAIL: 'john@doe.com'
            },
            COLUMN_TO_USER: {
                FIELD_TO_USER_ID: '456',
                FIELD_TO_USER_NAME: 'Lorem Ipsum',
                FIELD_TO_USER_EMAIL: 'lorem@ipsum.com'
            },
            COLUMN_MESSAGE: {
                FIELD_MESSAGE_SUBJECT: 'Lorem ipsum',
                FIELD_MESSAGE_BODY: 'Lorem ipsum dolor sit amet.'
            },
        }
        table = self.connection.table(NON_EXISTENT_TABLE_NAME)
        res = table.insert(key, columns, fail_silently=fail_silently)
        return res

    @print_info
    def test_26_insert_row_into_non_existing_table_fail_silently(self):
        """
        Insert row into non-existing table (`fail_silently` set to True).
        """
        res = self.__insert_row_into_non_existing_table(fail_silently=True)
        self.assertEqual(res, None)

    @print_info
    def test_27_insert_row_into_non_existing_table_raise_exception(self):
        """
        Insert row into non-existing table (`fail_silently` set to False).
        """
        try:
            res = self.__insert_row_into_non_existing_table(fail_silently=False)
            raise Exception("`starbase.exceptions.DoesNotExist` is expected to be raised, but it's not!")
        except DoesNotExist as e:
            pass

    def __update_row_of_non_existing_table(self, fail_silently=True):
        """
        Update row of non-existing table.
        """
        # Success test
        perfect_dict = True

        key = 'row_{0}_{1}'.format(('perfect_' if perfect_dict else ''), str(uuid.uuid4()))

        columns = {
            COLUMN_FROM_USER: {
                FIELD_FROM_USER_ID: '123',
                FIELD_FROM_USER_NAME: 'John Doe',
                FIELD_FROM_USER_EMAIL: 'john@doe.com'
            },
            COLUMN_TO_USER: {
                FIELD_TO_USER_ID: '456',
                FIELD_TO_USER_NAME: 'Lorem Ipsum',
                FIELD_TO_USER_EMAIL: 'lorem@ipsum.com'
            },
            COLUMN_MESSAGE: {
                FIELD_MESSAGE_SUBJECT: 'Lorem ipsum',
                FIELD_MESSAGE_BODY: 'Lorem ipsum dolor sit amet.'
            },
        }
        table = self.connection.table(NON_EXISTENT_TABLE_NAME)
        res = table.update(key, columns, fail_silently=fail_silently)
        return res

    @print_info
    def test_28_update_row_of_non_existing_table_fail_silently(self):
        """
        Update row of non-existing table (`fail_silently` set to True).
        """
        res = self.__update_row_of_non_existing_table(fail_silently=True)
        self.assertEqual(res, None)

    @print_info
    def test_29_update_row_of_non_existing_table_raise_exception(self):
        """
        Update row of non-existing table (`fail_silently` set to False).
        """
        try:
            res = self.__update_row_of_non_existing_table(fail_silently=False)
            raise Exception("`starbase.exceptions.DoesNotExist` is expected to be raised, but it's not!")
        except DoesNotExist as e:
            pass

    def __drop_non_existing_table_fail_silently(self, fail_silently=True):
        """
        Drop non-existing table.
        """
        table = self.connection.table(NON_EXISTENT_TABLE_NAME)
        return table.drop(fail_silently=fail_silently)

    @print_info
    def test_30_drop_non_existing_table_fail_silently(self):
        """
        Drop non-existing table (`fail_silently` set to True).
        """
        res = self.__drop_non_existing_table_fail_silently(fail_silently=True)
        self.assertEqual(res, 503)

    @print_info
    def test_31_drop_non_existing_table_raise_exception(self):
        """
        Drop non-existing table  (`fail_silently` set to False).
        """
        try:
            res = self.__drop_non_existing_table_fail_silently(fail_silently=False)
            raise Exception("`requests.exceptions.HTTPError` is expected to be raised, but it's not!")
        except HTTPError as e:
            pass

    def __fetch_row_of_non_existing_table(self, fail_silently=True):
        """
        Fetch row of non existing table.
        """
        table = self.connection.table(NON_EXISTENT_TABLE_NAME)
        return table.fetch('bla_01', fail_silently=fail_silently)

    @print_info
    def test_32_fetch_row_of_non_existing_table_fail_silently(self):
        """
        Drop non-existing table (`fail_silently` set to True).
        """
        res = self.__fetch_row_of_non_existing_table(fail_silently=True)
        self.assertEqual(res, None)

    @print_info
    def test_33_fetch_row_of_non_existing_table_raise_exception(self):
        """
        Drop non-existing table  (`fail_silently` set to False).
        """
        try:
            res = self.__fetch_row_of_non_existing_table(fail_silently=False)
            raise Exception("`starbase.exceptions.DoesNotExist` is expected to be raised, but it's not!")
        except DoesNotExist as e:
            pass

    def __remove_row_of_non_existing_table(self, fail_silently=True):
        """
        Remove row of non existing table.
        """
        table = self.connection.table(NON_EXISTENT_TABLE_NAME)
        return table.remove('bla_01', fail_silently=fail_silently)

    @print_info
    def test_34_remove_row_of_non_existing_table_fail_silently(self):
        """
        Remove row of non-existing table (`fail_silently` set to True).
        """
        res = self.__remove_row_of_non_existing_table(fail_silently=True)
        self.assertEqual(res, 500)

    @print_info
    def test_35_remove_row_of_non_existing_table_raise_exception(self):
        """
        Remove row of non-existing table  (`fail_silently` set to False).
        """
        try:
            res = self.__remove_row_of_non_existing_table(fail_silently=False)
            raise Exception("`starbase.exceptions.DoesNotExist` is expected to be raised, but it's not!")
        except HTTPError as e:
            pass


class StarbaseClient03TableTestDisabledIfExists(unittest.TestCase):
    """
    Starbase table tests with disabled if exists checks.
    """
    def setUp(self):
        self.connection = Connection(HOST, PORT, content_type='json')
        self.table = self.connection.table('non_existing')
        self.table.disable_if_exists_checks()

    @print_info
    def test_01_fetch_row(self):
        """
        Testing row operations (`fetch` method) of the `starbase.client.table.Table`.
        """
        res = self.table.fetch('row1')
        self.assertTrue(res is None)
        return res

    @print_info
    def test_02_insert_row(self):
        """
        Testing row operations (`insert` method) of the `starbase.client.table.Table`.
        """
        res = self.table.insert('row1', {'column1': {'id': '1', 'name': 'nn'}, 'column2': {'id': '2', 'age': '3'}})
        self.assertTrue(res == 500)
        return res

    @print_info
    def test_03_update_row(self):
        """
        Testing row operations (`update` method) of the `starbase.client.table.Table`.
        """
        res = self.table.update('row1', {'column1': {'id': '1', 'name': 'nn'}, 'column2': {'id': '2', 'age': '3'}})
        self.assertTrue(res == 500)
        return res

    @print_info
    def test_04_remove_row(self):
        """
        Testing row operations (`remove` method) of the `starbase.client.table.Table`.
        """
        res = self.table.remove('row1')
        self.assertTrue(res == 500)
        return res

    @print_info
    def test_05_scanner_operations(self):
        """
        Testing scanner operations (`fetch_all_rows` method) of the `starbase.client.table.Table`.
        """
        res = self.table.fetch_all_rows(flat=True)
        self.assertTrue(res is None)
        return res

    @print_info
    def test_06_batch_operations(self):
        """
        Testing batch operations (`batch` method) of the `starbase.client.table.Table`.
        """
        res = self.table.batch()
        self.assertTrue(res is None)
        return res


if __name__ == '__main__':
    unittest.main()
