from app import app

import pymysql as sql
import hashlib
import string
import random

def md5(str):
    return hashlib.md5(str.encode()).hexdigest()

def register_user(username, password):
    if (get_user("username", username)): return False
    conn = sql.connect(
        host = "127.0.0.1",
        unix_socket = "/var/lib/mysql/mysql.sock",
        user = "root",
        passwd = "",
        db = "epitodo"
    )
    cursor = conn.cursor()
    CHARS = string.ascii_uppercase + string.ascii_lowercase + string.digits
    salt = ''.join(random.choice(CHARS) for _ in range(9))
    hashed_password = md5(password + salt);

    cursor.execute("INSERT INTO epitodo.user (username, password) " +
        "VALUES ({}, {});".format(
            conn.escape(username),
            conn.escape(hashed_password + ";" + salt)
        )
    )
    conn.commit()
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return True

def check_user(username, password):
    user_data = get_user("username", username)
    if (not user_data):
        return False;
    salt = user_data[2].split(";")[1]
    hashed_password = user_data[2].split(";")[0]
    if (hashed_password != md5(password + salt)):
        return False;
    return True;

def get_user(val, key):
    conn = sql.connect(
        host = "127.0.0.1",
        unix_socket = "/var/lib/mysql/mysql.sock",
        user = "root",
        passwd = "",
        db = "epitodo"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM epitodo.user WHERE {} = {} LIMIT 1;".format(
        str(val),
        conn.escape(str(key))
    ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result[0] if len(result) == 1 else None
