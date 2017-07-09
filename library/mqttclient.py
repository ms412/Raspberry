__author__ = 'oper'


import time
import os
#import library.libpaho as mqtt
import paho.mqtt.client as mqtt

from queue import Queue
#from library.msgbus import msgbus


class mqttbroker(object):

    def __init__(self,config):
        '''
        setup mqtt broker
        config = dictionary with configuration
        '''



        self._host = str(config.get('HOST','localhost'))
        self._port = int(config.get('PORT',1883))
        #temp = str(config.get('SUBSCRIBE','/SUBSCRIBE'))
        #self._subscribe = temp.split(",")

        self._subscribe = str(config.get('SUBSCRIBE',None))
        self._subscribe +='#'

        print('Subscribe Channel:', self._subscribe)

        self._publish = str(config.get('PUBLISH','/PUBLISH'))


        '''
        create mqtt session
        '''
        #self.create()
        self._mqttc = mqtt.Client(str(os.getpid()),clean_session=True)

        self.setup(self._config)
       # self.start()

    def __del__(self):
      #  print("Delete libmqttbroker")
        self._mqttc.disconnect()

    def start(self):
      #  print('MQTT::start')
        '''
        start broker
        '''
       # self._mqttc=self.create()
        msg = 'Start connection'
        self.msgbus_publish('LOG','%s Libmqtt: %s '%('INFO',msg))

        self.callback()
        self.connect(self._host,self._port)
        #for item in self._subscribe:
         #   print('subscribe:',item)
        self.subscribe(self._subscribe)

        self.msgbus_subscribe(self._msgSink,self.send)
        #self.subscribe('/TEST/#')
          #  time.sleep(5)
        return True

    def callback(self):
        '''
        setup callbacks
        '''
        self._mqttc.on_message = self.on_message
        self._mqttc.on_connect = self.on_connect
        self._mqttc.on_publish = self.on_publish
        self._mqttc.on_subscribe = self.on_subscribe
        self._mqttc.on_disconnect = self.on_disconnect
        self._mqttc.on_log = self.on_log
        return True


    def send(self,message):
        msg = 'Messages transmit'
        self.msgbus_publish('LOG','%s Libmqtt: %s '%('INFO',msg))
        #print('channel',channel)

        self.publish(message)
        return True

    def receive(self):
        if not self._rxQueue.empty():
            msg = self._rxQueue.get()
         #   message = msg.get('MESSAGE',None)
          #  channel = msg.get('CHANNEL',None)
        else:
            msg = None
           # channel = None

        return msg


    def on_connect(self, client, userdata, flags, rc):
       # print('MQTT:: connect to host:', self._host,client,userdata,flags,str(rc))
        msg = 'Connect to Mqtt broker'
        self.msgbus_publish('LOG','%s Libmqtt: %s '%('INFO',msg))
        self._connectState = True
    #    self.msgbus_publish('LOG','%s Broker: Connected %s'%('INFO', self._connectState))
        return True

    def on_disconnect(self, client, userdata, rc):
        msg = 'Disconnect from Mqtt broker'
        self.msgbus_publish('LOG','%s Libmqtt: %s '%('CRITICAL',msg))
      #  print('Mqtt:: Disconnect' +str(client)+' '+str(userdata)+' '+str(rc))
        return True

    def on_message(self, client, userdata, msg):
        message ={}
        message.update({'CHANNEL':msg.topic})
        message.update({'VALUE':msg.payload})
       # print('MQTT:: on_message:',userdata,msg,message)
        log_msg = 'Message received'
        self.msgbus_publish('LOG','%s Libmqtt: %s Channel: %s Message: %s'%('INFO',log_msg, msg.topic, msg.payload))
        self.msgbus_publish(self._msgSource,message)
      #  self.msgbus_publish('LOG','%s Broker: received Date Device: %s , Port: %s , Message: %s'%('INFO',message['CHANNEL'], message['PORT_NAME'], message['MESSAGE']))
       # self._rxQueue.put(message)
        return True

    def on_publish(self, client, userdata, mid):
        msg = 'Message published'
        self.msgbus_publish('LOG','%s Libmqtt: %s '%('INFO',msg))
   #     print('MQTT on_published '+str(client)+' '+str(userdata)+' '+str(mid))
        return True



    def on_subscribe(self, client, userdata, mid, granted_qos):
        msg = 'Subscribed to Channel'
        self.msgbus_publish('LOG','%s Libmqtt: %s '%('INFO',msg))
    #    print('MQTT: on_subscribe: '+str(client)+' '+str(userdata)+' '+str(mid)+' '+str(granted_qos))
        return True

    def on_unsubscribe(self, client, userdata, mid):
        msg = 'Unsubscribe from Channel'
        self.msgbus_publish('LOG','%s Libmqtt: %s '%('INFO',msg))
     #   print('MQTT:: unsubscribe',client, userdata,mid)
        return True

    def on_log(self, client, userdata, level, buf):
        '''
        Test
        :param client:
        :param userdata:
        :param level:
        :param buf:
        :return:
        '''
      #  print('MQTT: Log',client, userdata, level, buf)
        return True

   # def create(self):
    #    print('mqtt create mqtt object')
     #   return mqtt.Client(str(os.getpid()))

    def reinitialise(self):
        msg = 'Reinitialise'
        self.msgbus_publish('LOG','%s Libmqtt: %s '%('INFO',msg))
      #  print('mqtt reinitialise')
        self._mqttc.reinitialise(str(os.getpid()), clean_session=True)
        return True

    def connect(self,host,port):
        #print('COnnect')
        self._mqttc.connect(host, port,60)
        self._mqttc.loop_start()
        return True

    def disconnect(self):
       # print('dissconnect')
        self._mqttc.disconnect()
        #self._mqttc.loop_stop()
        #self._mqttc.loop_forever()
        return True

    def subscribe(self, channel, callback):
        self._callback[channel] = callback
        self._mqttc.subscribe(channel, 0)
        return True

    def unsubscribe(self,channel):
       # print('mqtt unsubscribe')
        self._mqttc.unsubscribe(self._subscribe)
        return True

    def publish(self,channel, message):
        self._mqttc.publish(channel, message, 0)
        return True

if __name__ == "__main__":

    config1 = {'HOST':'192.168.1.107','PUBLISH':'/TEST','SUBSCRIBE':'/TEST/','CONFIG':'/TEST2/'}
    config2 = {'HOST':'localhost','PUBLISH':'/TEST','SUBSCRIBE':['/TEST1/#','/TEST3','/TEST4']}
    msg = {'CHANNEL':'/TEST/CONFIG','MESSAGE':'{ioioookko}'}
    broker = mqttbroker(config1)
  #  broker = setup(config)
 #   broker.start()

#    broker.connect()
 #   broker.subscribe()
    time.sleep(10)
    broker.restart(config1)
 #   time.sleep(10)

    while True:
        time.sleep(1)
        #broker.publish(msg)
   # time.sleep(2)
