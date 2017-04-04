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


__app__ = "ultrasonic2mqtt Adapter"
__VERSION__ = "0.9"
__DATE__ = "04.04.2017"
__author__ = "Markus Schiesser"
__contact__ = "M.Schiesser@gmail.com"
__copyright__ = "Copyright (C) 2017 Markus Schiesser"
__license__ = 'GPL v3'

from configobj import ConfigObj
from library.sr04 import sr04
from library.configfile import configfile
from library.mqttpush import mqttpush
from library.loghandler import loghandler


class manager(object):

    def __init__(self,configfile):
        self._configfile = configfile

        self._general = None
        self._mqttbroker = None
        self._ultrasonic = None

    def readconfig(self):
     #   _cfg = configfile(self._configfile)
      #  _config = _cfg.openfile()
        _config = ConfigObj(self._configfile)
        self._logcfg = _config.get('LOGGING',None)
        self._mqttbroker = _config.get('BROKER',None)
        self._ultrasonic = _config.get('ULTRASONIC',None)
        return True

    def logger(self):
        print(self._logcfg)
        self._log = loghandler('ULTRASONIC')
        self._log.handle(self._logcfg.get('LOGMODE'),self._logcfg)
        return True

    def measure(self):
        result = {}
        for item, value in self._ultrasonic.items():
            _trigger = value.get('TRIGGER',24)
            _echo = value.get('ECHO',23)
            us = sr04(_trigger,_echo)

            result[item] = us.measure_average()
            del us
           # result[item] = 5

        return result

    def publishData(self,data):
        mqttc = mqttpush(self._mqttbroker)
        main_channel = self._mqttbroker.get('PUBLISH','/OPENHAB')

        for deviceId, measurement in data.items():
            channel = main_channel + '/' + deviceId
          #  print('channel',channel,deviceId)
            mqttc.publish(channel,measurement)

        return True

    def run(self):
        self.readconfig()
        self.logger()
        self._log.info('Startup, %s %s %s' % (__app__, __VERSION__, __DATE__))
      #  self._log.info('Start Reading Valuse')
        data = self.measure()
        print('DAten',data)
        self._log.info(data)
        self.publishData(data)



if __name__ == '__main__':
    mgr = manager('/home/pi/m2m/ultrasonic2mqtt.cfg')
    mgr.run()