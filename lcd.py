import I2C_LCD_driver
from time import *

dolny_kwadrat = [
          0b00000,
          0b00000,
          0b00000,
          0b00000,
          0b11111,
          0b11111,
          0b11111,
          0b11111
        ]

gorny_kwadrat = [
          0b11111,
          0b11111,
          0b11111,
          0b11111,
          0b00000,
          0b00000,
          0b00000,
          0b00000
        ]

caly_kwadrat = [
          0b11111,
          0b11111,
          0b11111,
          0b11111,
          0b11111,
          0b11111,
          0b11111,
          0b11111
        ]
pusty = [
          0b00000,
          0b00000,
          0b00000,
          0b00000,
          0b00000,
          0b00000,
          0b00000,
          0b00000
        ]

ludzik_pusty_dol = [
          0b00000,
          0b00000,
          0b00000,
          0b00000,
          0b10001,
          0b01110,
          0b01110,
          0b10001
        ]

ludzik_pelny_dol = [
          0b11111,
          0b11111,
          0b11111,
          0b11111,
          0b10001,
          0b01110,
          0b01110,
          0b10001
        ]
ludzik_pusty_gora = [
          0b10001,
          0b01110,
          0b01110,
          0b10001,
          0b00000,
          0b00000,
          0b00000,
          0b00000
        ]

ludzik_pelny_gora = [
          0b10001,
          0b01110,
          0b01110,
          0b10001,
          0b11111,
          0b11111,
          0b11111,
          0b11111,
        ]

highlighted_right = [
          0b00001,
          0b00001,
          0b00001,
          0b00001,
          0b00001,
          0b00001,
          0b00001,
          0b00001,
]

highlighted_left = [
          0b10000,
          0b10000,
          0b10000,
          0b10000,
          0b10000,
          0b10000,
          0b10000,
          0b10000,
]

one = [
          0b00100,
          0b01100,
          0b00100,
          0b00100,
          0b00100,
          0b00100,
          0b01110,
          0b00000,
]

two = [
          0b01110,
          0b10001,
          0b00001,
          0b00010,
          0b00100,
          0b01000,
          0b11111,
          0b00000,
]

three = [
          0b11111,
          0b00010,
          0b00100,
          0b00010,
          0b00001,
          0b10001,
          0b01110,
          0b00000,
]

four = [
          0b00010,
          0b00110,
          0b01010,
          0b10010,
          0b11111,
          0b00010,
          0b00010,
          0b00000,
]

five = [
          0b11111,
          0b10000,
          0b11110,
          0b00001,
          0b00001,
          0b10001,
          0b01110,
          0b00000,
]


class Lcd:
    def __init__(self):
        self.mylcd = I2C_LCD_driver.lcd()
        self.custom = [caly_kwadrat, gorny_kwadrat, dolny_kwadrat, pusty, ludzik_pelny_dol, ludzik_pusty_dol, ludzik_pelny_gora,
              ludzik_pusty_gora]
        self.mylcd.lcd_load_custom_chars(self.custom)
        self.next = 0

    def show(self, mapa):
        pos = self.mapa_to_char(mapa)
        self.mylcd.lcd_write(0x80)
        for i in range(16):
            self.mylcd.lcd_write_char(pos[i])

        self.mylcd.lcd_write(0xC0)
        for i in range(16):
            self.mylcd.lcd_write_char(pos[i + 16])

    def win(self, result):
        self.mylcd.lcd_clear()
        self.mylcd.lcd_display_string("You have won!", 1)
        sleep(2)
        self.mylcd.lcd_clear()
        self.mylcd.lcd_display_string("Your result:", 1)
        self.mylcd.lcd_display_string(str(result), 2)
        self.mylcd.lcd_display_string("sec", 2, len(str(result)))
        sleep(2)
        self.mylcd.lcd_clear()
        self.mylcd.lcd_display_string("Nick:", 1)

    def nick(self, letter):
        self.mylcd.lcd_display_string(letter, 2, self.next)
        self.next += 1

    @staticmethod
    def mapa_to_char(mapa):
        pos = list()
        i = 0
        j = 0
        while j < 4:
            while i < 16:
                if mapa[j][i] == '#':
                    if mapa[j + 1][i] == '#':
                        pos.append(0)
                    elif mapa[j + 1][i] == ' ':
                        pos.append(1)
                    elif mapa[j + 1][i] == '@':
                        pos.append(4)
                elif mapa[j][i] == ' ' or mapa[j][i] == 'k':
                    if mapa[j + 1][i] == '#':
                        pos.append(2)
                    elif mapa[j + 1][i] == ' ':
                        pos.append(3)
                    elif mapa[j + 1][i] == '@':
                        pos.append(5)
                elif mapa[j][i] == '@':
                    if mapa[j + 1][i] == '#':
                        pos.append(6)
                    elif mapa[j + 1][i] == ' ':
                        pos.append(7)
                i += 1
            j += 2
            i = 0
        return pos


class LcdMainScreen:
    def __init__(self):
        self.mylcd = I2C_LCD_driver.lcd()
        self.custom_highlighted = [highlighted_right, highlighted_left, one, two, three, four, five, pusty]
        self.mylcd.lcd_load_custom_chars(self.custom_highlighted)

    def show(self, which):
        tab = []
        for i in range(11):
            if i % 2 == 1:
                tab.append(i // 2 + 2)
            else:
                tab.append(7)
        tab[(which-1)*2] = 0
        tab[((which-1)*2)+2] = 1

        self.mylcd.lcd_display_string("Labirynt:", 1)
        self.mylcd.lcd_write(0xC0)
        for i in tab:
            self.mylcd.lcd_write_char(i)

    def settings(self, ip, port):
        self.mylcd.lcd_display_string(ip, 1)
        self.mylcd.lcd_display_string("Port: ", 2)
        self.mylcd.lcd_display_string(port, 2, 6)

    def clear(self):
        self.mylcd.lcd_clear()

    def end(self):
        self.mylcd.lcd_clear()
        self.mylcd.lcd_display_string("Again?", 1, 4)
        self.mylcd.lcd_display_string("Press ENTER", 2, 2)


