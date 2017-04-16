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


__app__ = "Modbus2mqtt Adapter"
__VERSION__ = "0.9"
__DATE__ = "04.04.2017"
__author__ = "Markus Schiesser"
__contact__ = "M.Schiesser@gmail.com"
__copyright__ = "Copyright (C) 2017 Markus Schiesser"
__license__ = 'GPL v3'

import os
import sys
from configobj import ConfigObj

#from library.ds18b20 import ds18b20
from library.devicereader import devicereader
from library.configfile import configfile
from library.mqttpush import mqttpush
#from library.logging import logger
from library.loghandler import loghandler
from library.mgr_modbus import mgr_modbus


class manager(object):
    def __init__(self,configfile):
       # self._log = loghandler('ONEWIRE')
        self._configfile = configfile

        self._logcfg = None
        self._mqttbroker = None
        self._modbus = None
        self._commands = None

    def readconfig(self):
        #_cfg = configfile(self._configfile)
        #_config = _cfg.openfile()
        _config = ConfigObj(self._configfile)
        print(_config)
        self._logcfg = _config.get('LOGGING',None)
        self._mqttbroker = _config.get('BROKER',None)
        self._modbus = _config.get('MODBUS',None)
        self._commands = _config.get('DEVICE',None)
        print(self._logcfg)
        return True

    def logger(self):
        self._log = loghandler('MODBUS')
        self._log.handle(self._logcfg.get('LOGMODE'),self._logcfg)
        return True

    def modbus(self):
      #  result = {}
        for devicename,item in self._commands.items():
           # print(key,item['CONFIG']['MODBUSID'])
            print(devicename,item)
            self._modbus['DEVICEID']=item['CONFIG']['MODBUSID']
            self._mgr = mgr_modbus(self._modbus,self._log)
            self._mgr.setup()
            _channel = item.get('PUBLISH','/OPENAHB/AC')
            print(item)
            _result = {}
            for key,item in item['CALLS'].items():
                print('data',key, item)
             #   value =0
                value = self._mgr.read(item)
               # value  = 0
                if value is not None:
                    _result[key]= value

            print('Result',_result,devicename)
            self.publishData(devicename,_result)
       # print(result)
        return True

    def publishData(self,channel,data):
        mqttc = mqttpush(self._mqttbroker)
        main_channel = self._mqttbroker.get('PUBLISH','/OPENHAB')

        for item, measurement in data.items():
            _channel = main_channel + '/' + channel + '/' + item
            self._log.debug('channel: %s, mesage %s'% (_channel,measurement))
            mqttc.publish(_channel,measurement)

        return True

    def run(self):
#        self.startSystem()
        self.readconfig()
        self.logger()

        self._log.info('Startup, %s %s %s'% ( __app__, __VERSION__, __DATE__) )
        self.modbus()
       # self.publishData(data)



if __name__ == '__main__':
    print('main')
    if len(sys.argv) == 2:
        configfile = sys.argv[1]
    else:
        configfile ='/opt/Modbus2mqtt/modbus2mqtt.cfg'
     #   configfile = 'modbus2mqtt.cfg'

    mgr_handle = manager(configfile)
    mgr_handle.run()

