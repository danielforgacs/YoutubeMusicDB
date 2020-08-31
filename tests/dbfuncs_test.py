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
#     expected = {}
#
#
#
#     data = dbf.select_all_videos()
#
#     assert data == {}
