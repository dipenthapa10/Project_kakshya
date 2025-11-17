
import pymysql

def get_connection():
    try:
        conn = pymysql.connect(
            host="localhost",
            user= "root",
            password= "",
            database= "IDBS_project",
            cursorclass = pymysql.cursors.DictCursor
        )
        return conn
    except:
        print("connection error")
        return None

