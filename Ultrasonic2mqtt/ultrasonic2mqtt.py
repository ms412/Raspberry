#!/usr/bin/python3.4

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
        self._log.info('Start Reading Valuse')
        data = self.measure()
        print('DAten',data)
        self._log.info(data)
        self.publishData(data)



if __name__ == '__main__':
    mgr = manager('/home/pi/m2m/ultrasonic2mqtt.cfg')
    mgr.run()