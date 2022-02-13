from datetime import datetime

from freezegun import freeze_time
from pytest_mock import MockerFixture
from code import _set_listed_at

@freeze_time('2020-12-12')
def test__set_listed_at(mocker: MockerFixture):
    marketplace = mocker.MagicMock(value='ebay')
    item = mocker.MagicMock(ebay_listed_at=None)
    _set_listed_at(item, marketplace)
    assert item.ebay_listed_at == datetime(2020, 12, 12)
