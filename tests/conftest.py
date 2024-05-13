
import sys

import mock
import pytest

from .tools import SMBusFakeAS7262


@pytest.fixture
def smbus():
    smbus = mock.Mock()
    smbus.SMBus = SMBusFakeAS7262
    sys.modules['smbus2'] = smbus
    yield smbus


@pytest.fixture
def AS7262():
    from as7262 import AS7262
    yield AS7262
    del sys.modules['as7262']