"""Library for the AS7262 Visble Light Spectral Sensor."""
import as7262

if __name__ == '__main__':
    as7262.soft_reset()

    hw_type, hw_version, fw_version = as7262.get_version()

    print('{}'.format(fw_version))

    as7262.set_gain(64)

    as7262.set_integration_time(17.857)

    as7262.set_measurement_mode(2)

    # as7262.set_illumination_led_current(12.5)
    as7262.set_illumination_led(1)
    # as7262.set_indicator_led_current(2)
    # as7262.set_indicator_led(1)

    try:
        while True:
            values = as7262.get_calibrated_values()
            print("""
Red:    {}
Orange: {}
Yellow: {}
Green:  {}
Blue:   {}
Violet: {}""".format(*values))
    except KeyboardInterrupt:
        as7262.set_measurement_mode(3)
        as7262.set_illumination_led(0)
