import os
import psycopg2


conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    dbname=os.getenv('DB_DBNAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
)


def create_playlist(title, ytid):
    sql = "INSERT INTO playlist (title, youtubeid) VALUES (%s, %s)"
    cur = conn.cursor()
    cur.execute(sql, (title, ytid))
    conn.commit()



if __name__ == '__main__':
    pass
