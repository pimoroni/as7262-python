"""Test tools for the AS7262 sensor."""
import struct
from i2cdevice import MockSMBus

CALIBRATED_VALUES = [1.1, 2.2, 3.3, 4.4, 5.5, 6.6]

REG_STATUS = 0x00
REG_WRITE = 0x01
REG_READ = 0x02


class SMBusFakeAS7262(MockSMBus):
    """Fake the AS7262 non-standard i2c-based protocol.

    The AS7262 uses 3 registers- status, write and read.

    Internally it maintains a register pointer that is set
    using a write operation (register 0x01).

    This pointer uses the 7th bit (0b10000000) to indicate
    a write versus a read but we can mostly ignore it.

    Any write or read operation will begin with a write
    to register 0x01 - the real "write" register.

    A read will then follow with a read from register 0x02
    - the real "read" register.

    In our case, we use the previously written register
    as a pointer into self.regs, which is our virtual
    register space.

    A read to 0x00 will always return the status,
    regardless of how the pointer is currently set.

    This mimics the AS7262's behaviour closely enough
    to facilitate testing.

    """

    def __init__(self, i2c_bus):
        """Initialise the class.

        :param i2c_bus: i2c bus ID.

        """
        MockSMBus.__init__(self, i2c_bus)
        self.status = 0b01    # Fake status register
        self.ptr = None       # Fake register pointer

        # Virtual registers, thes contain the data actually used
        self.regs[0x00] = 0x88  # Fake HW type
        self.regs[0x01] = 0x77  # Fake HW version
        self.regs[0x02] = 0xFE  # Fake FW version MSB (Sub, Minor)
        self.regs[0x03] = 0xFF  # Fake FW version LSB (Minor, Major)
        self.regs[0x04] = 0x02  # Control Register

        # Prime the Calibrated Data registers with fake data
        self.regs[0x14:24] = [ord(c) if type(c) is str else c for c in struct.pack(
            '>ffffff',
            *reversed(CALIBRATED_VALUES)
        )]

        # Major = 0b1111 = 15
        # Minor = 0b111111 = 63
        # Sub = 0b111110 = 62

    def write_byte_data(self, i2c_address, register, value):
        """Write a single  byte."""
        if self.ptr is None and register == REG_WRITE:
            self.ptr = value & 0b1111111  # Mask out write bit

        elif self.ptr is not None:
            self.regs[self.ptr] = value
            self.ptr = None

    def read_byte_data(self, i2c_address, register):
        """Read a single byte."""
        if register == REG_STATUS:
            return self.status

        elif self.ptr is not None and register == REG_READ:
            value = self.regs[self.ptr]
            self.ptr = None
            return value

        return 0
