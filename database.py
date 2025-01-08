import mysql.connector
from mysql.connector import Error

try:
    conn = mysql.connector.connect(host="localhost",
                                   database="tetris",
                                   user="root",
                                   password="")
    print("Connected")
except Error as e:
    print("Error", e)