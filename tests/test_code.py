from datetime import datetime
from pathlib import PosixPath

import pytest
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
    assert sqlite.connect.cursor.execute.called_with('SELECT word FROM words')


@pytest.mark.parametrize(
    'source_path, expected_path',
    [
        ('path1', 'path1/file.so'),
        ('path2', 'path2/file.so'),
    ],
)
def test_get_all_filepathes_recursively(mocker: MockerFixture, source_path, expected_path):
    def isdir(path: str):
        return 'dir' in path

    def fake_glob(path: PosixPath, wildcard):
        extension = wildcard.split('.')[-1]
        for filename in ['file.', 'dir.']:
            yield path.joinpath(filename + extension)

    mocker.patch('code.os.path.isdir', isdir)
    mocker.patch('code.Path.glob', fake_glob)

    assert code.get_all_filepathes_recursively(source_path, 'so') == [expected_path]
