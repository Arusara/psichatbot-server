import mysql.connector
from mysql.connector import errorcode
from unittest import TestCase
from mock import patch
import utils
from app import app

MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB = "psis_testdb"
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"


def add_data(query, cursor, cnx):
    try:
        cursor.execute(query)
        cnx.commit()
    except mysql.connector.Error as err:
        print("Data insertion to test_table failed \n" + err)


def add_table(query, cursor, cnx):
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


class MockDB(TestCase):
    @classmethod
    def setUpClass(cls):
        app.testing = True
        cls.app = app.test_client
        
        cnx = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            port=MYSQL_PORT
        )
        cursor = cnx.cursor(dictionary=True)

        # drop database if it already exists
        try:
            cursor.execute("DROP DATABASE {}".format(MYSQL_DB))
            cursor.close()
            print("DB dropped")
        except mysql.connector.Error as err:
            # print("{}".format(MYSQL_DB))
            pass

        cursor = cnx.cursor(dictionary=True)
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(MYSQL_DB))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
        cnx.database = MYSQL_DB

        add_table("""CREATE TABLE `user_data_package` (
                  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
                  `package_id` int(11) NOT NULL,
                  `user_id` int(11) NOT NULL UNIQUE ,
                  `package_name` text COLLATE utf8_unicode_ci NOT NULL,
                  `data_used` float NOT NULL DEFAULT '0',
                  `activated_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;""", cursor, cnx)
        add_table("""CREATE TABLE `user_voice_package` (
                      `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
                      `package_id` int(11) NOT NULL,
                      `user_id` int(11) NOT NULL UNIQUE ,
                      `package_name` text COLLATE utf8_unicode_ci NOT NULL,
                      `minutes_used` int(11) NOT NULL DEFAULT '0',
                      `activated_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;""", cursor, cnx)
        add_table("""CREATE TABLE `data_packages` (
                      `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
                      `name` text COLLATE utf8_unicode_ci NOT NULL,
                      `data` float NOT NULL,
                      `valid_period` float NOT NULL,
                      `price` float NOT NULL
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;""", cursor, cnx)
        add_table("""CREATE TABLE `voice_packages` (
                      `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
                      `name` text COLLATE utf8_unicode_ci NOT NULL,
                      `minutes` float NOT NULL,
                      `valid_period` int(11) NOT NULL,
                      `price` float NOT NULL
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;""", cursor, cnx)
        add_table("""CREATE TABLE `user_complaint_low_signal` (
                      `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                      `user_id` int(11) NOT NULL,
                      `location` text COLLATE utf8_unicode_ci NOT NULL,
                      `report` text COLLATE utf8_unicode_ci NOT NULL,
                      `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;""", cursor, cnx)
        add_table("""CREATE TABLE `user_complaint_no_signal` (
                      `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                      `user_id` int(11) NOT NULL,
                      `location` text COLLATE utf8_unicode_ci NOT NULL,
                      `report` text COLLATE utf8_unicode_ci NOT NULL,
                      `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;""", cursor, cnx)
        add_table("""CREATE TABLE `telecom_chatbot_messages` (
                        `id` varchar(30) COLLATE utf8_unicode_ci NOT NULL PRIMARY KEY ,
                        `user_id` int(11) NOT NULL,
                        `message` text COLLATE utf8_unicode_ci NOT NULL,
                        `isBot` tinyint(1) NOT NULL,
                        `date_time` datetime NOT NULL
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;""", cursor, cnx)
        add_data("""INSERT INTO `user_data_package` (`package_id`, `user_id`, `package_name`, `data_used`) VALUES
                    (3, 1, 'D99', 0),
                    (6, 2, 'D499', 0);""", cursor, cnx)
        add_data("""INSERT INTO `user_voice_package` (`package_id`, `user_id`, `package_name`, `minutes_used`) VALUES
                    (1, 1, 'V20', 0),
                    (4, 2, 'V200', 0);""", cursor, cnx)
        add_data("""INSERT INTO `data_packages` (`id`, `name`, `data`, `valid_period`, `price`) VALUES
                    (1, 'D29', 200, 2, 29),
                    (2, 'D49', 400, 7, 49),
                    (3, 'D99', 1000, 21, 99),
                    (4, 'D199', 2000, 30, 199),
                    (5, 'D349', 4000, 30, 349),
                    (6, 'D499', 6000, 30, 499),
                    (7, 'D649', 8500, 30, 649);
                    """, cursor, cnx)
        add_data("""INSERT INTO `voice_packages` (`id`, `name`, `minutes`, `valid_period`, `price`) VALUES
                    (1, 'V20', 30, 7, 20),
                    (2, 'V60', 100, 7, 60),
                    (3, 'V100', 200, 14, 100),
                    (4, 'V200', 400, 30, 200);""", cursor, cnx)

        cursor.close()
        cnx.close()

        testconfig = {
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