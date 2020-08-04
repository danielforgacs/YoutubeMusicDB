import os
import psycopg2
import app.data as data


conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    dbname=os.getenv('DB_DBNAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
)



def test_can_create_playlist():
    title = 'test-playlist-01'
    ytid = 'id-01'

    data.create_playlist(
        title=title,
        ytid=ytid,
    )

    cur = conn.cursor()
    cur.execute(query="""
        SELECT
            title,
            youtubeid
        FROM
            playlist
        WHERE
            title = %s
        ;
    """, vars=(title,))
    result = cur.fetchall()
    cur.close()

    assert len(result) == 1
    assert result[0][0] == title
    assert result[0][1] == ytid
