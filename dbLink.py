import mysql.connector
from mysql.connector import cursor
from datetime import datetime
import _secret

default_radius = 2
default_max_displayed = 5


def initDB():
    global cursor, db
    db = mysql.connector.connect(
        host=_secret.db_host,
        user=_secret.db_user,
        password=_secret.db_password,
        database=_secret.db_database,
    )
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(dt_string + " --> dbLink.py --> Connected to:", db.get_server_info())
    cursor = db.cursor()


def addUser(user_id, max_displayed, radius):
    reConnectDB()
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(dt_string + " --> dbLink.py --> Creating new user " + str(user_id))
    sql = "INSERT INTO users (id, max_displayed, radius, total_requests) VALUES (%s, %s, %s, %s)"
    values = (user_id, max_displayed, radius, 0)
    cursor.execute(sql, values)
    db.commit()


def updateData(user_id, max_displayed, radius):
    reConnectDB()
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(
        dt_string + " --> dbLink.py --> Updating data for user " + str(user_id) + "\n\n"
    )
    sql = "UPDATE users SET radius = %s, max_displayed=%s WHERE id = %s"
    values = (radius, max_displayed, user_id)
    cursor.execute(sql, values)
    db.commit()


def performRequest(user_id):
    reConnectDB()
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(
        dt_string + " --> dbLink.py --> Updating request count for user " + str(user_id)
    )
    sql = "UPDATE users SET last_request=%s, total_requests = total_requests+1 WHERE id = %s"
    dt_string = now.strftime("%y-%m-%d %H:%M:%S")
    values = (dt_string, user_id)
    cursor.execute(sql, values)
    db.commit()


def getData(user_id):
    reConnectDB()
    sql = "SELECT max_displayed, radius from users WHERE id=%s"
    values = (user_id,)
    cursor.execute(sql, values)
    result = cursor.fetchone()
    try:
        return [int(result[0]), float(result[1])]
    except TypeError:
        return 0


def reConnectDB():
    if db.is_connected() != True:
        initDB()
