import sqlite3
import uuid

DB_NAME = "diseases.db"

def get_database_connection():
    con = sqlite3.connect(DB_NAME)
    return con

def get_disease(nick):
    con = get_database_connection()
    cur = con.cursor()

    sql_query = "SELECT name,description,image FROM diseases WHERE nick = ?"

    cur.execute(sql_query,(nick.upper(),))
    results = cur.fetchall()

    cur.close()
    con.close()

    return results

def get_user(username,password):
    con = get_database_connection()
    cur = con.cursor()

    sql_query = "SELECT * FROM users WHERE username = ? AND password = ?"

    cur.execute(sql_query,(username,password,))
    results = cur.fetchall()

    cur.close()
    con.close()

    return results

def update_user_count(username,count):
    con = get_database_connection()
    cur = con.cursor()

    sql_query = "UPDATE users SET totalRequests = ? WHERE username = ? "

    cur.execute(sql_query,(count,username,))
    con.commit()

    cur.close()
    con.close()

def register_user(username,password):

    results = get_user(username,password)

    if len(results) == 0:
        con = get_database_connection()
        cur = con.cursor()

        sql_query = "INSERT INTO users(uuid,username,password,requestCount,totalRequests) VALUES(?,?,?,?,0)"

        cur.execute(sql_query,(str(uuid.uuid1()),username,password,100,))
        con.commit()

        cur.close()
        con.close()