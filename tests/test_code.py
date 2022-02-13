from datetime import datetime

from freezegun import freeze_time
from pytest_mock import MockerFixture
from code import _set_listed_at
import code


@freeze_time('2020-12-12')
def test__set_listed_at(mocker: MockerFixture):
    marketplace = mocker.MagicMock(value='ebay')
    item = mocker.MagicMock(ebay_listed_at=None)
    _set_listed_at(item, marketplace)
    assert item.ebay_listed_at == datetime(2020, 12, 12)


def test_load_obscene_words(mocker: MockerFixture):
    def fetchall():
        return [['first', 'second', 'third']]

    def execute(query: str):
            return mocker.Mock(fetchall=fetchall)

    def cursor():
        return mocker.Mock(execute=execute)

    connection = mocker.Mock(cursor=cursor)

    def connect(path):
        return connection

    sqlite = mocker.Mock(connect=connect)
    mocker.patch('code.sqlite3', sqlite)
    assert code.load_obscene_words('path') == {'first', 'second', 'third'}
