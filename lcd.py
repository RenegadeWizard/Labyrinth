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


class Lcd:
    def __init__(self):
        self.mylcd = I2C_LCD_driver.lcd()
        self.custom = [caly_kwadrat, gorny_kwadrat, dolny_kwadrat, pusty, ludzik_pelny_dol, ludzik_pusty_dol, ludzik_pelny_gora,
              ludzik_pusty_gora]
        self.mylcd.lcd_load_custom_chars(self.custom)

    def show(self, mapa):
        pos = self.mapa_to_char(mapa)
        self.mylcd.lcd_write(0x80)
        for i in range(16):
            self.mylcd.lcd_write_char(pos[i])

        self.mylcd.lcd_write(0xC0)
        for i in range(16):
            self.mylcd.lcd_write_char(pos[i + 16])

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
                elif mapa[j][i] == ' ':
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
