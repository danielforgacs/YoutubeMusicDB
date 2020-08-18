import os


TEST_DB_NAME = 'ymdb_test'
os.environ['PGDATABASE'] = TEST_DB_NAME

SCHEMA_FILE = os.path.join(os.getcwd(), 'sql', 'schema.sql')




YOUTUBE_PLAYLISTS = [
    'https://www.youtube.com/playlist?list=PL9YsudagsL6hicXrha4zBId875lRXxc32',
    'https://www.youtube.com/playlist?list=PL9YsudagsL6h0n4ew9ibbicfGFIPdUKMU',
    'https://www.youtube.com/playlist?list=PL9YsudagsL6ipb5Yd7QKz0x9byLncwEs_',
]
YOUTUBE_VIDEOS = [
    'https://www.youtube.com/watch?v=HJq-6y2IYEQ',
    'https://www.youtube.com/watch?v=FIQ2F3T1ydM',
    'https://www.youtube.com/watch?v=HJq-6y2IYEQ',
    'https://www.youtube.com/watch?v=zrxuPkbIq4g',
    'https://www.youtube.com/watch?v=iI1M48eC3x4',
    'https://www.youtube.com/watch?v=EDQ1dmFEGiI',
    'https://www.youtube.com/watch?v=BPopaJsNWd4',
]
YOUTUBE_IDS = YOUTUBE_PLAYLISTS + YOUTUBE_VIDEOS
