from log_ctl import g_log
import pymysql

def create_new_connect(host='127.0.0.1', unix_socket='/var/run/mysqld/mysqld.sock', user='root', passwd='#####', db='mysql'):
    g_log.debug('now try to connect the db with %s, %s, %s, %s, %s' % (host, unix_socket, user, passwd, db))
    try:
        conn = pymysql.connect(host=host, unix_socket=unix_socket, user=user, passwd=passwd, db=db, use_unicode=True, charset="utf8")
        return conn
    except Exception as e:
        g_log.error(e)
        return None

def create_new_cursor(conn):
    g_log.debug('Now try to create a new cur.')
    try:
        cur = conn.cursor()
        return cur
    except Exception as e:
        g_log.error(e)
        return None

def close_cursor(cursor):
    g_log.debug("now release cursor")
    cursor.close()

def close_conn(conn):
    g_log.debug("now release connection")
    conn.close()
