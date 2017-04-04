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
        self._commands = _config.get('COMMANDS',None)
        print(self._logcfg)
        return True

    def logger(self):
        self._log = loghandler('MODBUS')
        self._log.handle(self._logcfg.get('LOGMODE'),self._logcfg)
        return True

    def modbus(self):
        result = {}
        self._mgr = mgr_modbus(self._modbus,self._log)
        self._mgr.setup()
        print(self._commands)
        for key,item in self._commands.items():
            print('data',key, item)
            value = self._mgr.read(item)
            if value is not None:
                result[key]= value

        print(result)
        return result

    def publishData(self,data):
        mqttc = mqttpush(self._mqttbroker)
        main_channel = self._mqttbroker.get('PUBLISH','/OPENHAB')

        for deviceId, measurement in data.items():
            channel = main_channel + '/' + deviceId
            print('channel',channel,measurement)
            mqttc.publish(channel,measurement)

        return True

    def run(self):
#        self.startSystem()
        self.readconfig()
        self.logger()
        self._log.info('Start Reading Valuse')
        data = self.modbus()

   #     data = self.getData()
       # print('DAten',data)
      #  self._log.info(data)

        self.publishData(data)



if __name__ == '__main__':
    print('main')
    if len(sys.argv) == 2:
        configfile = sys.argv[1]
    else:
        #    configfile = 'C:/Users/tgdscm41/PycharmProjects/Raspberry/S02mqtt1.cfg'
       # configfile = 'C:/Users/tgdscm41/PycharmProjects/Raspberry/Modbus2mqtt/modbus2mqtt.cfg'
        configfile ='/opt/Modbus2mqtt/modbus2mqtt.cfg'
        # configfile =  '/home/pi/m2m/S02mqtt.cfg'

        # print('Configfile',configfile)
    mgr_handle = manager(configfile)
    mgr_handle.run()

