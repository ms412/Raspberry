
import RPi.GPIO as GPIO
import time


class pulscount(object):

    def __init__(self,pin):

        self._gpio = GPIO
        self._gpio.setmode(self._gpio.BCM)

        self._gpio.setup(pin, self._gpio.IN, pull_up_down = self.gpio.PUD_DOWN)
        self._gpio.add_event_detect(pin, self._gpio.RISING,callback =self.pulscount(),bouncetimem=300)

        self._count = 0
        self._total_elapsed_time = 0

        self._state = 0
        self._t0 = 0
        self._t1 = 0

    def pulscount(self):
        self._count = self._count + 1

        if self._state > 1 and self._gg

        if self._t0 == 0:
            self._t0 = time.time()

        else:
            self._t1 = time.time() - self._t0
            self._t0 = time.time()

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

counter = 0
while True:
    GPIO.wait_for_edge(23, GPIO.RISING)
    counter += 1
    print "Counter is now", counter/800.0, "kWh"
    GPIO.wait_for_edge(23, GPIO.FALLING)

GPIO.cleanup()