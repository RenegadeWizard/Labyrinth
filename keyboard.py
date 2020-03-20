import RPi.GPIO as GPIO


class Keyboard:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.delay = 0
        self.cols = [19, 13, 6, 5]
        self.rows = [21, 20, 16, 26]
        self.keys = (
            ('1', '2', '3', 'A'),
            ('4', '5', '6', 'B'),
            ('7', '8', '9', 'C'),
            ('*', '0', '#', 'D')
        )
        for i in self.rows:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, GPIO.LOW)

        for i in self.cols:
            GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # TODO: PULLDOWN

    def check(self, delay=0):
        # if self.delay > 0:
        #     self.delay -= 1
        if not self.delay:
            for i, row in enumerate(self.rows):
                GPIO.output(row, GPIO.HIGH)
                for j, col in enumerate(self.cols):
                    if GPIO.input(col):
                        return self.keys[i][j]
                GPIO.output(row, GPIO.LOW)
            # self.delay = delay
        return ''
