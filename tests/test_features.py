# noqa D100
from .tools import CALIBRATED_VALUES


def test_set_integration_time(smbus, AS7262):
    """Test the set_integration_time method against various values."""
    as7262 = AS7262()

    # Integration time is stored as 2.8ms per lsb
    # so returned values experience quantization
    # int(50/2.8)*2.8 == 50.0
    as7262.set_integration_time(50)
    assert as7262._as7262.INTEGRATION_TIME.get_ms() == 50.0

    # For example: 90 will alias to 89.6
    # int(90/2.8)*2.8 == 89.6
    as7262.set_integration_time(90)
    assert round(as7262._as7262.INTEGRATION_TIME.get_ms(), 1) == 89.6

    # All input values are masked by i2cdevice according
    # to the mask supplied.
    # In the case of Integration Time this is 0xFF
    # A value of 99999 multiplied by 2.8 and masked would
    # result in 189 being written to the device.
    as7262.set_integration_time(99999)
    assert as7262._as7262.INTEGRATION_TIME.get_ms() == (int(99999 * 2.8) & 0xFF) / 2.8


def test_set_gain(smbus, AS7262):
    """Test the set_gain method against various values."""
    as7262 = AS7262()

    as7262.set_gain(1)
    assert as7262._as7262.CONTROL.get_gain_x() == 1

    # Should snap to the highest gain value
    as7262.set_gain(999)
    assert as7262._as7262.CONTROL.get_gain_x() == 64

    # Should snap to the lowest gain value
    as7262.set_gain(-1)
    assert as7262._as7262.CONTROL.get_gain_x() == 1


def test_set_measurement_mode(smbus, AS7262):
    """Test the set_measurement_mode method."""
    as7262 = AS7262()

    as7262.set_measurement_mode(2)
    assert as7262._as7262.CONTROL.get_measurement_mode() == 2


def test_set_illumination_led_current(smbus, AS7262):
    """Test the set_illumination_led_current method."""
    as7262 = AS7262()

    as7262.set_illumination_led_current(12.5)
    assert as7262._as7262.LED_CONTROL.get_illumination_current_limit_ma() == 12.5

    as7262.set_illumination_led_current(20)
    assert as7262._as7262.LED_CONTROL.get_illumination_current_limit_ma() == 25

    as7262.set_illumination_led_current(101)
    assert as7262._as7262.LED_CONTROL.get_illumination_current_limit_ma() == 100


def test_set_indicator_led_current(smbus, AS7262):
    """Test the set_indicator_led_current method."""
    as7262 = AS7262()

    as7262.set_indicator_led_current(4)
    assert as7262._as7262.LED_CONTROL.get_indicator_current_limit_ma() == 4

    as7262.set_indicator_led_current(9)
    assert as7262._as7262.LED_CONTROL.get_indicator_current_limit_ma() == 8

    as7262.set_indicator_led_current(0)
    assert as7262._as7262.LED_CONTROL.get_indicator_current_limit_ma() == 1


def test_indicator_led(smbus, AS7262):
    """Test the indicator_led method."""
    as7262 = AS7262()

    as7262.set_indicator_led(1)
    assert as7262._as7262.LED_CONTROL.get_indicator_enable() == 1


def test_illumination_led(smbus, AS7262):
    """Test the illumination_led method."""
    as7262 = AS7262()

    as7262.set_illumination_led(1)
    assert as7262._as7262.LED_CONTROL.get_illumination_enable() == 1


def test_soft_reset(smbus, AS7262):
    """Test the soft_reset method."""
    as7262 = AS7262()

    as7262.soft_reset()
    assert as7262._as7262.CONTROL.get_reset() == 1


def test_get_calibrated_values(smbus, AS7262):
    """Test against fake calibrated values stored in hardware mock."""
    as7262 = AS7262()

    values = as7262.get_calibrated_values()

    # Deal with floating point nonsense
    values = [round(x, 1) for x in values]

    assert values == CALIBRATED_VALUES
