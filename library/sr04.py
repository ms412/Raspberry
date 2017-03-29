
import RPi.GPIO as GPIO
import time


class sr04(object):

    def __init__(self,trig,echo):

        self._trig = int(trig)
        self._echo = int(echo)
        self._gpio = GPIO
        self._gpio.setmode(self._gpio.BCM)
        #self._gpio.cleanup()
        print('ports',self._trig,self._echo)
        self._gpio.setup(self._trig,self._gpio.OUT)
        self._gpio.setup(self._echo, self._gpio.IN)

        self._gpio.output(self._trig,False)
        time.sleep(2)

    def __del__(self):
        self._gpio.cleanup()

    def measure(self):

        self._gpio.output(self._trig, True)
        time.sleep(0.00001)
        self._gpio.output(self._trig, False)

        start = time.time()
       # print('hier',self._gpio.input(self._echo))

        while self._gpio.input(self._echo) == 0:
            start = time.time()

        while self._gpio.input(self._echo) == 1:
            stop = time.time()

        elapsed = stop - start

        print(elapsed)
        distance = (elapsed * 34300) /2

        return distance

    def measure_average(self):
        measure = 0
        for i in range(3):
            measure += self.measure()
            time.sleep(0.1)

        return measure/3






