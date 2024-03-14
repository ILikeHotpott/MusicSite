import MySQLdb

try:
    db = MySQLdb.connect(host="localhost", user="root", passwd="Lcy741125", db="music")
    print("Connected to the database successfully")
except MySQLdb.Error as e:
    print(f"Error connecting to MySQL: {e}")
