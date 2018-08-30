import sys
import mock
from i2cdevice import MockSMBus


class SMBusFakeDevice(MockSMBus):
    def __init__(self, i2c_bus):
        MockSMBus.__init__(self, i2c_bus)
        self.status = 0b01    # Fake status register
        self.ptr = None       # Fake register pointer

        self.regs[0x00] = 0x88  # Fake HW type
        self.regs[0x01] = 0x77  # Fake HW version
        self.regs[0x02] = 0xFE  # Fake FW version MSB (Sub, Minor)
        self.regs[0x03] = 0xFF  # Fake FW version LSB (Minor, Major)

        # Major = 0b1111 = 15
        # Minor = 0b111111 = 63
        # Sub = 0b111110 = 62

    def write_byte_data(self, i2c_address, register, value):
        if self.ptr is None and register == 0x01:
            self.ptr = value & 0b1111111  # Mask out write bit

        elif self.ptr is not None:
            self.regs[self.ptr] = value
            self.ptr = None

    def read_byte_data(self, i2c_address, register):
        if register == 0x00:
            return self.status

        elif self.ptr is not None and register == 0x02:
            value = self.regs[self.ptr]
            self.ptr = None
            return value

        return 0


def test_fw_info():
    smbus = mock.Mock()
    smbus.SMBus = SMBusFakeDevice
    sys.modules['smbus'] = smbus
    import as7262

    hw_type, hw_version, fw_version = as7262.get_version()

    assert hw_version == 0x77
    assert hw_type == 0x88
    assert fw_version == "15.63.62"
