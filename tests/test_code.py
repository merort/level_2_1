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
    sqlite = mocker.Mock()
    obscene_words = [['first', 'second', 'third']]
    sqlite.connect.return_value.cursor.return_value.execute.return_value.fetchall.return_value = obscene_words
    mocker.patch('code.sqlite3', sqlite)
    assert code.load_obscene_words('path') == {'first', 'second', 'third'}
