from unittest import TestCase
import mysql.connector
from mysql.connector import errorcode
from mock import patch
import utils


MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB = "psis_testdb"
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"


class TestUtils(TestCase):

    @classmethod
    def setUpClass(cls):
        cnx = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            port = MYSQL_PORT
        )
        cursor = cnx.cursor(dictionary=True)

        # drop database if it already exists
        try:
            cursor.execute("DROP DATABASE {}".format(MYSQL_DB))
            cursor.close()
            print("DB dropped")
        except mysql.connector.Error as err:
            print("{}".format(MYSQL_DB, err))

        cursor = cnx.cursor(dictionary=True)
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(MYSQL_DB))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
        cnx.database = MYSQL_DB

        query = """CREATE TABLE `test_table` (
                  `id` varchar(30) NOT NULL PRIMARY KEY ,
                  `text` text NOT NULL,
                  `int` int NOT NULL
                )"""
        try:
            cursor.execute(query)
            cnx.commit()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("test_table already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

        insert_data_query = """INSERT INTO `test_table` (`id`, `text`, `int`) VALUES
                            ('1', 'test_text', 1),
                            ('2', 'test_text_2',2)"""
        try:
            cursor.execute(insert_data_query)
            cnx.commit()
        except mysql.connector.Error as err:
            print("Data insertion to test_table failed \n" + err)
        cursor.close()
        cnx.close()

        testconfig ={
            'host': MYSQL_HOST,
            'user': MYSQL_USER,
            'password': MYSQL_PASSWORD,
            'database': MYSQL_DB
        }
        cls.mock_db_config = patch.dict(utils.config, testconfig)

    @classmethod
    def tearDownClass(cls):
        cnx = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        cursor = cnx.cursor(dictionary=True)

        # drop test database
        try:
            cursor.execute("DROP DATABASE {}".format(MYSQL_DB))
            cnx.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print("Database {} does not exists. Dropping db failed".format(MYSQL_DB))
        cnx.close()

    def test_db_read(self):
        with self.mock_db_config:
            self.assertDictEqual(utils.db_read("""SELECT * FROM `test_table`""")[0], {
                'id': '1',
                'text': 'test_text',
                'int': 1
            })
            self.assertDictEqual(utils.db_read("""SELECT * FROM `test_table`""")[1], {
                'id': '2',
                'text': 'test_text_2',
                'int': 2
            })

    def test_db_write(self):
        with self.mock_db_config:
            self.assertEqual(utils.db_write("""INSERT INTO `test_table` (`id`, `text`, `int`) VALUES
                            ('3', 'test_text_3', 3)"""), True)
            self.assertEqual(utils.db_write("""INSERT INTO `test_table` (`id`, `text`, `int`) VALUES
                            ('1', 'test_text_3', 3)"""), False, "Insert entry to already existing primary key")
            self.assertEqual(utils.db_write("""DELETE FROM `test_table` WHERE id='1' """), True)
            self.assertEqual(utils.db_write("""DELETE FROM `test_table` WHERE id='4' """), True, "Delete non-existent entry" )