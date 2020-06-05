from unittest import TestCase
import mysql.connector
import mock
import utils


MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB = "psis_testdb"
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"


class TestUtils(TestCase):

    def setUp(self):
        testdb = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWORD,
            database=MYSQL_DB
        )
        cursor = testdb.cursor(dictionary=True)
        query = """CREATE TABLE `test_table` (
                  `id` varchar(30) NOT NULL PRIMARY KEY ,
                  `text` text NOT NULL,
                  `int` int NOT NULL
                );
                INSERT INTO `test_table` (`id`, `text`, `int`) VALUES
                ('1', 'test_text', 1),
                ('2', 'test_test_2',2);"""
        cursor.execute(query)
        testdb.commit()
        cursor.close()

        self.mock_db = mock.patch.object(utils, 'db', return_value=testdb)

    def test_db_read(self):
        with self.mock_db:
            print(utils.db)
            self.assertDictEqual(utils.db_read("""SELECT * FROM `test_table`""")[0], {
                'id': '1',
                'text': 'test_text',
                'int': 1
            })




    def test_db_write(self):
        pass

    def test_write_message(self):
        pass

    def get_user_messages(self):
        pass
