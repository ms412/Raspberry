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


__app__ = "myStrom2mqtt Adapter"
__VERSION__ = "0.8"
__DATE__ = "09.07.2017"
__author__ = "Markus Schiesser"
__contact__ = "M.Schiesser@gmail.com"
__copyright__ = "Copyright (C) 2017 Markus Schiesser"
__license__ = 'GPL v3'


import sys
import time
import json

from configobj import ConfigObj
from library.mqttclient import mqttclient
from library.loghandler import loghandler
from library.myStromSwitch import switchwrapper

from library.myStromBulb import bulbwrapper
from library.myStromBulb import bulb


class manager(object):

    def __init__(self,cfg_file='myStrom2mqtt.cfg'):

        self._cfg_file = cfg_file

        self._cfg_broker = None
        self._cfg_log = None
        self._cfg_device = None

        self._mqttc = None


    def read_config(self):

        _cfg = ConfigObj(self._cfg_file)

        if bool(_cfg) is False:
        #    print('ERROR config file not found',self._cfg_file)
            sys.exit()
            #exit

        self._cfg_broker = _cfg.get('BROKER',None)
        self._cfg_log = _cfg.get('LOGGING',None)
        self._cfg_device = _cfg.get('DEVICE',None)
       # self._cfg_switch = _cfg.get('SWITCH',None)
        return True

    def start_logger(self):
        self._log = loghandler('MYSTROM2MQTT')
        self._log.handle(self._cfg_log.get('LOGMODE'),self._cfg_log)
        self._log.level(self._cfg_log.get('LOGLEVEL','DEBUG'))
        return True

    def config_broker(self):
        self._mqttc = mqttclient(self._cfg_broker,self._log)
#        self._mqttc.subscribe(self._cfg_broker.get('SUBSCRIBE','/MYSTROM'))

        return True

    def start_broker(self):
        self._mqttc.start()


    def start_devices(self):
        #print('Device config',self._cfg_device)
        _switch_cfg = self._cfg_device.get('SWITCH',None)
        _bulb_cfg = self._cfg_device.get('BULB', None)

        if _switch_cfg:
            #for item in _switch_cfg:
             #   print('SWITCH',item)
            _switchwrapper = switchwrapper(self._cfg_device.get('SWITCH', None),self._mqttc,self._log)
            _switchwrapper.start()

        if _bulb_cfg:
            _bulbwrapper = bulbwrapper(self._cfg_device.get('BULB'),self._mqttc,self._log)
            _bulbwrapper.start()

        return True


    def run(self):
        """
        Entry point, initiates components and loops forever...
        """
        self.read_config()
        self.start_logger()
        # Log information
        msg = 'Start ' + __app__ +' ' +  __VERSION__ + ' ' +  __DATE__
        self._log.info(msg)


        self.config_broker()
    #    self.publish_test()
        self.start_devices()
        self.start_broker()
        test = 1
        while(True):
            test = test+1

       # self._log.info('Startup, %s %s %s'% ( __app__, __VERSION__, __DATE__) )
#        self.start_gpio()


if __name__ == "__main__":

    print ('main')
    if len(sys.argv) == 2:
        configfile = sys.argv[1]
    else:
    #    configfile = 'C:/Users/tgdscm41/PycharmProjects/Raspberry/S02mqtt1.cfg'
        configfile = 'C:/Users/tgdscm41/PycharmProjects/Raspberry/myStrom2mqtt/myStrom2mqtt.cfg'
        #configfile =  '/home/pi/m2m/S02mqtt.cfg'

  #  print('Configfile',configfile)
    mgr_handle = manager(configfile)
    mgr_handle.run()