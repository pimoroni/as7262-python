# noqa D100


def test_fw_info(smbus, AS7262):
    """Test against fake device information stored in hardware mock."""
    as7262 = AS7262()

    hw_type, hw_version, fw_version = as7262.get_version()

    assert hw_version == 0x77
    assert hw_type == 0x88
    assert fw_version == '15.63.62'
