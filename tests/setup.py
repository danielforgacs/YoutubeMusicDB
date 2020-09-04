import os
import psycopg2
# import dbf
import dbaccess.dbfuncs as dbf


PGDATABASE = os.environ['PGDATABASE']
SCHEMA_FILE = os.path.join(os.getcwd(), 'sql', 'schema.sql')
DB_ACCESS_HOST = os.environ['DBACCESS_RPC_HOST']
DB_ACCESS_PORT = int(os.environ['DBACCESS_RPC_PORT'])
DB_ACCESS_URL = 'http://{host}:{port}'.format(host=DB_ACCESS_HOST, port=DB_ACCESS_PORT)

YOUTUBE_PLAYLISTS = [
    'https://www.youtube.com/playlist?list=PL9YsudagsL6h0n4ew9ibbicfGFIPdUKMU',
    'https://www.youtube.com/playlist?list=PL9YsudagsL6hicXrha4zBId875lRXxc32',
    'https://www.youtube.com/playlist?list=PL9YsudagsL6ipb5Yd7QKz0x9byLncwEs_',
]
YOUTUBE_VIDEOS = [
    'https://www.youtube.com/watch?v=R2kovI6tpRE',
    'https://www.youtube.com/watch?v=EDQ1dmFEGiI',
    'https://www.youtube.com/watch?v=FIQ2F3T1ydM',
    'https://www.youtube.com/watch?v=HJq-6y2IYEQ',
    'https://www.youtube.com/watch?v=iI1M48eC3x4',
    'https://www.youtube.com/watch?v=zrxuPkbIq4g',
]
YOUTUBE_IDS = YOUTUBE_PLAYLISTS + YOUTUBE_VIDEOS




def init_test_db():
    with open(SCHEMA_FILE, 'r') as schemafile:
        schemasql = schemafile.read()

    with dbf.PGConnection(dbname='postgres') as conn1:
        conn1.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn1.cursor()

        try:
            cur.execute(query="drop database %s;" % PGDATABASE)
        except psycopg2.errors.InvalidCatalogName:
            pass

    with dbf.PGConnection(dbname='postgres') as conn1:
        conn1.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn1.cursor()
        cur.execute(query="create database %s;" % PGDATABASE)

    with dbf.PGConnection() as conn2:
        conn2.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn2.cursor()
        cur.execute(query=schemasql)



def run_sql_file(sqlfile):
    sqlpath = os.path.join(
        os.path.dirname(os.path.dirname(__file__))
        , 'sql', sqlfile+'.sql')

    with open(sqlpath, 'r') as schemafile:
        schemasql = schemafile.read()

    with dbf.PGConnection() as conn:
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute(query=schemasql)
