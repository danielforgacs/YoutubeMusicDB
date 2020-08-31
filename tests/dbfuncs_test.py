import dbaccess.dbfuncs as dbf
import tests.setup



def setup():
    tests.setup.init_test_db()



def test_select_all_videos_empty_db():
    data = dbf.select_all_videos()
    expected = {}

    assert data == {}



def test_select_all_videos_01():
    tests.setup.run_sql_file(sqlfile='testData_01')
    expected = {
        'id1': {
            'id': 'id1',
            'title': 'title1',
            'playlistid': None,
            'added': '2000-01-01 00:00:00',
            'is_down': False,
            'playlisttitle': None,
        },
    }

    data = dbf.select_all_videos()

    print('-'*79)
    print(expected)
    print(data)
    print('-'*79)

    assert data == expected
