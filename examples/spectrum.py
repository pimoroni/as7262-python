from as7262 import AS7262

as7262 = AS7262()

as7262.set_gain(64)
as7262.set_integration_time(17.857)
as7262.set_measurement_mode(2)
as7262.set_illumination_led(1)

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

