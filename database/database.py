import mysql.connector
from mysql.connector import errorcode

from settings import MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_HOST

db = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    passwd=MYSQL_PASSWORD,
    database=MYSQL_DB
)

