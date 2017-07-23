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


__app__ = "vcontrold2mqtt Adapter"
__VERSION__ = "0.1"
__DATE__ = "23.07.2017"
__author__ = "Markus Schiesser"
__contact__ = "M.Schiesser@gmail.com"
__copyright__ = "Copyright (C) 2017 Markus Schiesser"
__license__ = 'GPL v3'


import sys
import time
import json

from configobj import ConfigObj
from library.mqttpush import mqttpush
from library.loghandler import loghandler
from library.vcontrold import vcontrold


class manager(object):

    def __init__(self,cfg_file='vcontrold2mqtt.cfg'):

        self._cfg_file = cfg_file

        self._cfg_broker = None
        self._cfg_log = None
        self._cfg_vclient = None
        self._cfg_commands = None

        self._mqttc = None
        self._vclient = None

        self._state = 'NOTCONNECTED'

        print('x')

    def read_config(self):
        print(self._cfg_file)
        _cfg = ConfigObj(self._cfg_file)
        print('tes123t',_cfg)

        if bool(_cfg) is False:
            _msg = 'Configuration File not found' + str(self._cfg_file)
            print('ERROR: ',_msg)
        #    print('ERROR config file not found',self._cfg_file)
        #    print('error')
            sys.exit()
            #exit
        print('0')
        self._cfg_broker = _cfg.get('BROKER',None)
        self._cfg_log = _cfg.get('LOGGING',None)
        self._cfg_vcontrold = _cfg.get('VCONTROLD',None)
        self._cfg_commands = _cfg.get('COMMANDS',None)
       # print(self._cfg_commands)
        return True

    def start_logger(self):
        self._log = loghandler('VCONTROLD2MQTT')
        self._log.handle(self._cfg_log.get('LOGMODE'),self._cfg_log)
        self._log.level(self._cfg_log.get('LOGLEVEL','DEBUG'))
        return True

    def config_broker(self):
        self._mqttc = mqttpush(self._cfg_broker)
#        self._mqttc.subscribe(self._cfg_broker.get('SUBSCRIBE','/MYSTROM'))
        return True

    def connect_vcontrold(self):
        self._vcontrold = vcontrold(self._cfg_vcontrold, self._log)
        result = self._vcontrold.connect()
        return result

    def read_vcontrold(self):
       # for item in self._cfg_commands:
        _commandlist = self._cfg_commands.get('COMMANDLIST',None)
        result = self._vcontrold.readValues(_commandlist)
        return result

    def publish(self,data):

        for key, value in data.items():
            self._mqttc.publish(key,json.dumps(value))
            print('mqtt',key,value )



    def run(self):
        """
        Entry point, initiates components and loops forever...
        """
        print('test')
        self.read_config()
        print('ooo')
        self.start_logger()
        print('loger')
        # Log information
        msg = 'Start ' + __app__ +' ' +  __VERSION__ + ' ' +  __DATE__
        self._log.info(msg)


        self.config_broker()
        print('config broker')
    #    self.publish_test()
     #   print('connected',self.connect_vcontrold())
        i = 0
        while not self.connect_vcontrold():
            i = i+1
           # print('faild to connect')
            _msg = 'Connection to vcontrold failed try ' + str(i)
            self._log.error(_msg)
            time.sleep(10)
            if i > 3:
                _msg = ('connection failed stop process')
                self._log.error(_msg)
                sys.exit(_msg)
               # break
        #self.start_broker()
#        self._connect_vclient()
        data = self.read_vcontrold()

        self.publish(data)



if __name__ == "__main__":

    print ('main')
    if len(sys.argv) == 2:
        configfile = sys.argv[1]
    else:
    #    configfile = 'C:/Users/tgdscm41/PycharmProjects/Raspberry/S02mqtt1.cfg'
        configfile = 'C:/Users/tgdscm41/PycharmProjects/Raspberry/vcontrold2mqtt/vcontrold2mqtt.cfg'
        #configfile =  '/home/pi/m2m/S02mqtt.cfg'

  #  print('Configfile',configfile)
    mgr_handle = manager(configfile)
    mgr_handle.run()