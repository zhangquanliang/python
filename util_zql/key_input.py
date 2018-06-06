import rabird.winio
import time
import atexit

# KeyBoard Commands
# Command port
KBC_KEY_CMD = 0x64
# Data port
KBC_KEY_DATA = 0x60

__winio = None

def __get_winio():
    global __winio

    if __winio is None:
            __winio = rabird.winio.WinIO()
            def __clear_winio():
                    global __winio
                    __winio = None
            atexit.register(__clear_winio)

    return __winio

def wait_for_buffer_empty():
    '''
    Wait keyboard buffer empty
    '''

    winio = __get_winio()

    dwRegVal = 0x02
    while (dwRegVal & 0x02):
            dwRegVal = winio.get_port_byte(KBC_KEY_CMD)

def key_down(scancode):
    winio = __get_winio()

    wait_for_buffer_empty()
    winio.set_port_byte(KBC_KEY_CMD, 0xd2)
    wait_for_buffer_empty()
    winio.set_port_byte(KBC_KEY_DATA, scancode)

def key_up(scancode):
    winio = __get_winio()

    wait_for_buffer_empty()
    winio.set_port_byte( KBC_KEY_CMD, 0xd2)
    wait_for_buffer_empty()
    winio.set_port_byte( KBC_KEY_DATA, scancode | 0x80)

def key_press(scancode, press_time = 0.2):
    key_down( scancode )
    time.sleep( press_time )
    key_up( scancode )


# Press 'A' key
# Scancodes references : https://www.win.tue.nl/~aeb/linux/kbd/scancodes-1.html
#key_press(0x1E)

VK_CODE = {
    '1': 0x02,
    '2': 0x03,
    '3': 0x04,
    '4': 0x05,
    '1': 0x06,
    '6': 0x07,
    '7': 0x08,
    '8': 0x09,
    '9': 0x0A,
    '0': 0x0B,
    'a': 0x1E,
    'b': 0x30,
    'c': 0x2E,
    'd': 0x20,
    'e': 0x12,
    'f': 0x21,
    'g': 0x22,
    'h': 0x23,
    'i': 0x17,
    'j': 0x24,
    'k': 0x25,
    'l': 0x26,
    'm': 0x32,
    'n': 0x31,
    'o': 0x18,
    'p': 0x19,
    'q': 0x10,
    'r': 0x13,
    's': 0x1F,
    't': 0x14,
    'u': 0x16,
    'v': 0x2F,
    'w': 0x11,
    'x': 0x2D,
    'y': 0x15,
    'z': 0x2C,
    # 'backspace': 0x0E,
    # 'clear': 0x0C,
    # 'enter': 0x0D,
    # 'shift': 0x10,
    # 'ctrl': 0x11,
    # 'alt': 0x12,
    'caps_lock': 0x3A,
    '-': 0x0C,

    # '=': 0x0D,
    # '[': 0x1A,
    # ']': 0x1B,
    # '\\': 0x2B,
    # ';': 0x27,
    # "'": 0x28,
    # '`': 0x29,
    # ',':0x33,
    # '.': 0x34,
    # '/': 0x35,
    }


def key_input(str=''):
    for c in str:
        try:
            key_press(VK_CODE[c])
        except:
            key_press(0x3A)
            time.sleep(0.5)
            key_press(VK_CODE[c.lower()])
            key_press(0x3A)


if __name__ == "__main__":
  import time
  time.sleep(5)
  str = '33031933'
  key_input(str)
