import requests
import time
import json
from threading import Thread

class switch_old(object):
    def __init__(self,ip):

        self._url= 'http://'+ ip
        self._switch = 'OFF'
        self._power = 0.0
        self._energy = 0.0
        self._t0 = time.time()

    def _status(self):
        info ="""{"power":0.0,"relay": false}"""
        result = json.loads(info)

        try:
            r = requests.get(self._url + '/report',timeout = 5)
#            print(r.text)
            return (True,r.json())
        except requests.Timeout:
            print('TIMEOUT')
        return (False,result)

    def update(self):
        _result = 0
        value, _status = self._status()
        print('status',_status)
        if value:

            if bool(_status['relay']):
                self._switch = 'ON'
                _result = 1
            else:
                self._switch = 'OFF'
                _result = 0

            self._power = float(_status['power'])
            _t1 = time.time() - self._t0
            self._t0 = time.time()
            print(_t1,self._power)
            self._energy = self._power * _t1 / 3600 / 1000

        return _result

    def power(self):
        return self._power

    def switch(self):
        return self._switch

    def energy(self):
        return self._energy

class switch(object):
    def __init__(self,ip,broker):

        self._url= 'http://'+ ip
        self._switch = 'OFF'
        self._power = 0.0
        self._broker = broker
   #     self._energy = 0.0
     #   self._t0 = time.time()

    def _status(self):
   #     info ="""{"power":0.0,"relay": false}"""
    #    result = json.loads(info)

        try:
            r = requests.get(self._url + '/report',timeout = 5)
#            print(r.text)
            return (True,r.json())
        except requests.Timeout:
            print('TIMEOUT')
        return (False,None)

    def update(self):
      #  _result = 0
        value, _status = self._status()
        print('status',_status)
        if value:
            if bool(_status['relay']):
                self._switch = 'ON'
                _result = 1
            else:
                self._switch = 'OFF'
                _result = 0

            self._power = float(_status['power'])
       #     _t1 = time.time() - self._t0
        #    self._t0 = time.time()
         #   print(_t1,self._power)
          #  self._energy = self._power * _t1 / 3600 / 1000

        #return _result
        return

    def power(self):
        return self._power

    def switch(self):
        return self._switch

    def callback(self):
        broker.callback()

 #   def energy(self):
  #      return self._energy

class switchwrapper(Thread):
    def __init__(self,config,broker):
        Thread.__init__(self)

        print('switchwrapper',config)

        self._broker = broker
        self._config = config

        self._processId = {}

        self.config()

    def config(self):

        for key,item in self._config.items():
        #    print('print',key,item.get('IP', None),item.get('MAC',None))
            self._processId[key] = switch(item.get('IP', None))
            print(self._processId[key].update())

 #       print('processId',self._processId)
#        self._broker.publish('test','123')
        return

    def update(self, mqttc, obj, msg):
        print('mesg',msg)

        return

    def run(self):
        print('START Thread Switch')
      #  self._broker.subscribe(self.update)
        self._broker.callback('/TEST/tt',self.update)

        while(True):
            print('test')
            for key,item in self._processId.items():
                # read power status
               # if item.on_status:
                #publish ligh status On/Off
                #print(item.on_st())
                item.update()
                _key = str(key + '/SWITCH')
                self._broker.publish(_key,item.switch())
                #publish power consumption
                _key = str(key + '/POWER')
                self._broker.publish(_key,item.power())
              #  _key = str(key + '/ENERGY')
               # self._broker.publish(_key,item.energy())
                time.sleep(10)

        return

