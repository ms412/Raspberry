import requests
import time
import json
from threading import Thread


class bulb(object):
    def __init__(self,ip,mac):
       # self._ip = ip
      # self._mac = mac
        print('bulb class',ip, mac)
        self._url = 'http://'+ ip +'/api/v1/device/'+ mac

        self._payload = {'action': 'on'}

    def post(self,payload):
        r = requests.post(self._url,data=payload)
        print(r.text)

    def switch(self,value):
        payload = {'action': value}
        print(payload)
        self.post(payload)


    def color(self,white = None,red = None,green = None,blue = None):
        _w_mask = 0xFF000000
        _r_mask = 0x00FF0000
        _g_mask = 0x0000FF00
        _b_mask = 0x000000FF

        self.mode('rgb')
        status = self.status()
        for each in status:
            color = int(status[each]['color'],16)
            print('current color',hex(color))

        if not white:
            white = (color & _w_mask) >> 24

        if not red:
            red = (color & _r_mask)  >> 16

        if not green:
            green = (color & _g_mask) >> 8

        if not blue:
            blue = (color & _b_mask) >> 0

        print('color',hex(white),hex(red),hex(green),hex(blue))

        _new_c = (color & ~(_w_mask) |(white << 24))
        _new_c = (_new_c & ~(_r_mask) |(red << 16))
        _new_c = (_new_c & ~(_g_mask) |(green << 8))
        _new_c = (_new_c & ~(_b_mask) |(blue << 0))

      #  print('new color', '{:02x}'.format(_new_c))
        payload = {'color':  '{:02x}'.format(_new_c)}
        print(payload)
        self.post(payload)


    def status(self):
        r = requests.get(self._url)
        print(r.text)
        return r.json()

    def mode(self,mode):
        payload = {'mode': mode}
        self.post(payload)

    def on_status(self,mode):
        status = self.status()
        for each in status:
            on_status = bool(status[each]['on'])
            #print('current color',power)

        return on_status

    def power(self):
        status = self.status()
        for each in status:
            power = int(status[each]['power'])
            print('current color',power)

        return power


    def dimmer(self,value):
        payload = {'ramp': (value*1000)}
        print(payload)
        self.post(payload)

    def rampUp(self,timeout,start=0,end=100):

        step = end - start
        steps = timeout / step
        print(step,steps)

        count = 0
        while count < step:
            self.dimmer(count)
            count = count + 1
            time.sleep(steps)


class bulbwrapper(Thread):
    def __init__(self,config,broker):
        Thread.__init__(self)

        print('bulbwrappter',config)

        self._broker = broker
        self._config = config

        self._processId = {}

        self.start()

    def start(self):

        for key,item in self._config.items():
        #    print('print',key,item.get('IP', None),item.get('MAC',None))
            self._processId[key] = bulb(item.get('IP', None),item.get('MAC',None))

 #       print('processId',self._processId)
#        self._broker.publish('test','123')

    def update(self,channel,msg):

        return

    def run(self):

        while(True):
            print('test')
            for key,item in self._processId.items():
                # read power status
               # if item.on_status:
                #publish ligh status On/Off
                self._broker.publish(key,item.on_status)
                #publish power consumption
                self._broker.publish(key,item.power())



if __name__ == '__main__':
    print('main')
    b = bulb('192.168.2.112','5CCF7FA0B919')
    b.test_1(red=0xff, green=0xEE)
    b.switch('on')
    b.status()
    b.color(red = 255, white = 255)
    #b.switch('on')

    b.status()
    time.sleep(15)
    b.switch('off')


