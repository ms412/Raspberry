import requests
import time
import json
from threading import Thread

class switch(object):
    def __init__(self,ip):

        self._url= 'http://'+ ip

    def ___status(self):
        call = self._url + '/report'
        print('print call',call)
        return call

    def _status(self):
        r = requests.get(self._url + '/report')
        print(r.text)
        return r.json()

    def on_status(self):
        status = self._status()
        return bool(status['relay'])


class switchwrapper(Thread):
    def __init__(self,config,broker):
        Thread.__init__(self)

        print('switchwrappter',config)

        self._broker = broker
        self._config = config

        self._processId = {}

        self.start()

    def start(self):

        for key,item in self._config.items():
        #    print('print',key,item.get('IP', None),item.get('MAC',None))
            self._processId[key] = switch(item.get('IP', None))
            print(self._processId[key].on_status())

 #       print('processId',self._processId)
#        self._broker.publish('test','123')
        return

    def update(self, mqttc, obj, msg):
        print('mesg',msg)

        return

    def run(self):
      #  self._broker.subscribe(self.update)
        self._broker.sub_callback(self.update)

        while(True):
            print('test')
            for key,item in self._processId.items():
                # read power status
               # if item.on_status:
                #publish ligh status On/Off
                self._broker.publish(key,item.on_status)
                #publish power consumption
                self._broker.publish(key,item.power())

        return

