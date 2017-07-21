#!/usr/bin/env python3
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

__app__ = "mqttClient"
__VERSION__ = "0.85"
__DATE__ = "14.07.2017"
__author__ = "Markus Schiesser"
__contact__ = "M.Schiesser@gmail.com"
__copyright__ = "Copyright (C) 2017 Markus Schiesser"
__license__ = 'GPL v3'


import os
import time
from threading import Thread
import paho.mqtt.client as mqtt
#from library.loghandler import dummylog


class mqttclient(Thread):
    def __init__(self,config,loghandle):
        Thread.__init__(self)

        self._host = str(config.get('HOST', 'localhost'))
        self._port = int(config.get('PORT', 1883))
        self._subscribe = str(config.get('SUBSCRIBE','/MYTOPIC'))
        self._publish = str(config.get('PUBLISH','/OPENHAB'))
        #print('mqtt client',config)

        self._log = loghandle

        msg = 'Start ' + __app__ +' ' +  __VERSION__ + ' ' +  __DATE__
        self._log.info(msg)

        msg = 'Configuration' + str(config)
        self._log.debug(msg)

        self._mqttc = mqtt.Client(str(os.getpid()), clean_session=True)

        self._mqttc.on_message = self.on_message
        self._mqttc.on_connect = self.on_connect
        self._mqttc.on_publish = self.on_publish
        self._mqttc.on_subscribe = self.on_subscribe

        self.connect()
        self.subscribe(self._subscribe)

    def on_connect(self, mqttc, obj, flags, rc):
      #  print("connect rc: "+str(rc))
        if rc == 0:
            msg = __app__ + 'successfully connected'
            self._log.debug(msg)
        else:
            msg = __app__ + 'failed do connect'
            self._log.error(msg)


    def on_message(self, mqttc, obj, msg):
      #  print('message')
     #   print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
        msg = __app__ + 'message received' + str(msg.qos)+" "+str(msg.payload)
        self._log.debug(msg)

    def on_publish(self, mqttc, obj, mid):
       # print("mid: "+str(mid))
        msg = __app__ + 'message published msgid' + str(mid)
        self._log.debug(msg)

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
      #  print("Subscribed: "+str(mid)+" "+str(granted_qos))
        msg = __app__ + 'subscribed to channel' + str(mid)
        self._log.debug(msg)

    def on_log(self, mqttc, obj, level, string):
        print(string)

    def subscribe(self,topic):
        _topic = str(topic+'/#')
     #   print('tt',_topic)
        self._mqttc.subscribe(_topic,0)
        msg = __app__ + 'subscribe to channel' + _topic
        self._log.debug(msg)

    def callback(self,topic,method):
        _topic =str(self._subscribe + '/' + topic)
        self._mqttc.message_callback_add(_topic,method)
        #print('register callback',_topic,method)
        msg = __app__ + 'create callback for channel' + str(_topic) + str(method)
        self._log.debug(msg)

    def connect(self):
         self._mqttc.connect(self._host,self._port)

    def publish(self,topic,payload):
        _topic = str(self._publish + '/' + topic)
     #   print('Publish',_topic,payload)
        self._mqttc.publish(_topic,payload,0)
        msg = __app__ + 'publish message' + str(_topic) + str(payload)
        self._log.debug(msg)

    def run(self):
       # self._mqttc.connect("192.168.2.50", 1883, 60)
    #    self.subscribe("/MYSTROM/#")
  #      print('Start Broker')
        msg = __app__ + 'start broker as thread'
        self._log.debug(msg)

        rc = 0
        while rc == 0:
       #     print('x')
            rc = self._mqttc.loop_forever()
        return rc


class printer1(object):
    def output(self,mqttc, obj,msg):
        print('putput1', msg)


class printer2(object):
    def output(self, mqttc, obj, msg):
        print('putput2', msg)


if __name__ == '__main__':

    pp1 = printer1()
    pp2 = printer2()
    mqttc = mqttclient({'HOST':'192.168.2.50','PORT':1883,'SUBSCRIBE':'/MYSTROM'})
#    mqttc = mqttclient()
    mqttc.callback('/MYSTROM/myStrom1',pp1.output)
    mqttc.callback('/MYSTROM/myStrom2',pp2.output)

    mqttc.start()

    while(True):
        mqttc.publish('/TEST','1234567')
        time.sleep(10)
