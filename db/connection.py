import psycopg2
import os
def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='files',
                            user=os.environ['postgres'],
                            password=os.environ['Almaty111'])
    return conn