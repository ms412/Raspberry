import requests
import time
import json
from threading import Thread

class switch(object):
    def __init__(self,config):

        self._config = config
        self._url= 'http://'+ self._config.get('IP',None)
        self._switch = 'OFF'
        self._power = 0.0
     #   self._energy = 0.0
      #  self._t0 = time.time()

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

    def getStatus(self):
        _result = 0
        _value, _status = self._status()
        print('status',_status, _value)
        if _value:
            print('True')
            if bool(_status['relay']):
                self._switch = 'ON'
                _result = 1
            else:
                self._switch = 'OFF'
                _result = 0

            self._power = float(_status['power'])
         #   _t1 = time.time() - self._t0
          #  self._t0 = time.time()
          #  print(_t1,self._power)
          #  self._energy = self._power * _t1 / 3600 / 1000

        return _result

    def getPower(self):
        return self._power

    def getSwitch(self):
        print('switch', self._switch)
        return self._switch

    def setSwitch(self,state):
        if not 'LOCK' == self._config.get('SWITCH','UNLOCK').upper():
            print('switch is not in lock mode')
            if 'ON'in state:
                _url = self._url + '/relay?state=1'
            else:
                _url = self._url + '/relay?state=0'
            print('requests',_url)
            try:
                requests.get(_url,timeout=5)
            except requests.Timeout:
                print('TIMEOUT')
          #  r = requests.get(self._url + '/report', timeout=5)
        else:
            print('switch is in lock mode no change')
       # print('test0',r.json())
        return True



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
            self._processId[key] = switch(item)
            print(self._processId[key].getStatus())

            #subscribe callback of mqtt
            _key = str(key + '/SWITCH')
            self._broker.callback(_key,self.msg_snk)

 #       print('processId',self._processId)
#        self._broker.publish('test','123')
        return

    def msg_snk(self,mqttc, obj,msg):
        print('received from mqtt',obj,msg.topic,msg.payload)
        _topic_split = msg.topic.split('/')
        _key_topic = _topic_split[-1]
        if 'SWITCH' == _key_topic:
            self.cmd_switch(msg.topic,msg.payload)
        else:
            print('command not found:',_key_topic)

        return True

    def cmd_switch(self,topic,payload):
        _topic_split = topic.split('/')
        _key_topic = _topic_split[-2]
        print('_topic_key', _key_topic)
        for key,item in self._processId.items():
            if key in _key_topic:
                print(key,_key_topic,payload)
                self._processId[key].setSwitch(str(payload))
                self._processId[key].getStatus()
                self.update(key,self._processId[key])

    def update(self,topic,obj):
        obj.getStatus()
        _topic = str(topic + '/SWITCH')
        self._broker.publish(_topic, obj.getSwitch())

        _topic = str(topic + '/POWER')
        self._broker.publish(_topic, obj.getPower())

        return True

    def run(self):
        print('START Thread Switch')
      #  self._broker.subscribe(self.update)
 #       self._broker.callback('/TEST/tt',self.update)
#
        while(True):
          #  print('test')
            for key,item in self._processId.items():
                # read power status
               # if item.on_status:
                #publish ligh status On/Off
                #print(item.on_st())
             #   item.getStatus()
                self.update(key,item)
             #   _key = str(key + '/SWITCH')
              #  self._broker.publish(_key,item.getSwitch())
                #publish power consumption
              #  _key = str(key + '/POWER')
               # self._broker.publish(_key,item.getPower())
                #_key = str(key + '/ENERGY')
               # self._broker.publish(_key,item.energy())
                time.sleep(5)

        return

