import usb.core
import binascii
from constants import *


class Keyboard(object):
    def __init__(self):
        self.device: usb.core.Device = usb.core.find(
            idVendor=VENDOR_ID, idProduct=PRODUCT_ID
        )

    def __enter__(self):
        if self.device.is_kernel_driver_active(INTERFACE):
            print('Detaching kernel driver')
            self.device.detach_kernel_driver(INTERFACE)

        configuration = self.device.get_active_configuration()
        interface = configuration[(INTERFACE, SETTING)]
        self._in = interface[IN_ENDPOINT_NUM]
        self._out = interface[OUT_ENDPOINT_NUM]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.device.reset()
        except Exception:
            print("Couldn't reset USB device.")
            pass
        return any([exc_type, exc_val, exc_tb])

    def write(self, data):
        self._out.write(data + ZEROES)
        result = self._in.read(64)
        return result

    def set_key_color(self, key, r, g, b):
        # Turns out that the second bit actually doesn't have an impact on
        # things. I'll leave it at 00 until something breaks.
        # if second_bit == None:
        #    second_bit = get_second_bit(key, int(r, 16), int(g, 16), int(b, 16))  # noqa
        # second_bit_bytes = to_bytes(second_bit)
        actual_key = KEYS[key]
        section = get_section(key)
        second_bit_bytes = b'\x00'
        key_hex_bytes = to_bytes(hex(actual_key)[2:])
        section_bytes = to_bytes(str(section))
        r_bytes = to_bytes(r)
        g_bytes = to_bytes(g)
        b_bytes = to_bytes(b)

        data = b''.join(
            [
                b'\x04',
                second_bit_bytes,
                b'\x01',
                Commands.WRITE_CUSTOM_COLOR_DATA,
                b'\x03',
                key_hex_bytes,
                section_bytes,
                b'\x00',
                r_bytes,
                g_bytes,
                b_bytes,
            ]
        )
        return self.write(data)

    def color_all(self, r, g, b):
        for i in range(0, TOTAL_KEY_COUNT):
            self.set_key_color(i, r, g, b)


def get_second_bit(key, r, g, b):
    """Calculate the value of the second bit."""
    # In case it's not clear, the second bit is the last two characters from:
    # hex(23 + (r + g + b) + key numeric value(0,3,6,...))
    sum_string = hex(23 + ((int(key)) * 3) + (r + g + b))
    second_bit = sum_string[len(sum_string) - 2: len(sum_string)]
    return second_bit


def to_bytes(arg):
    return binascii.unhexlify(arg.zfill(2))


def get_section(key_num):
    return 1 if key_num > SECTION_0_KEY_COUNT - 1 else 0


def read_rgb():
    return input('Enter R: '), input('Enter G: '), input('Enter B: ')


if __name__ == '__main__':
    command = ''
    with Keyboard() as keyboard:
        while command != 'stop':
            command = input('Enter a mode: ')
            if command == 'stop':
                break
            elif command == 'key':
                key = input('Enter a key: ')
                r, g, b = read_rgb()
                keyboard.set_key_color(int(key), r, g, b)
                continue
            elif command == 'colorall':
                r, g, b = read_rgb()
                keyboard.color_all(r, g, b)
                continue
            elif command == 'brightness':
                level = int(input('Enter a brightness level(0-4): '))
                command = BRIGHTNESS_COMMANDS[level]
                keyboard.write(command)
                continue
            elif command == 'raw':
                raw = input('Enter raw data: ')
                keyboard.write(to_bytes(raw))
                continue

            hex_value = MODE_COMMANDS.get(command, '')
            if hex_value == '':
                print('Invalid input, try again.')
            else:
                keyboard.write(hex_value)
