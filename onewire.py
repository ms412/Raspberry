#!/usr/bin/python3.4

import os
from configobj import ConfigObj

from library.ds18b20 import ds18b20
from library.devicereader import devicereader
from library.configfile import configfile
from library.mqttpush import mqttpush
#from library.logging import logger
from library.loghandler import loghandler


class manager(object):
    def __init__(self,configfile):
       # self._log = loghandler('ONEWIRE')
        self._configfile = configfile

        self._logcfg = None
        self._mqttbroker = None
        self._onewire = None

    def startSystem(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        return True

    def readconfig(self):
        #_cfg = configfile(self._configfile)
        #_config = _cfg.openfile()
        _config = ConfigObj(self._configfile)
        self._logcfg = _config.get('LOGGING',None)
        self._mqttbroker = _config.get('BROKER',None)
        self._onewire = _config.get('ONEWIRE',None)
        print(self._onewire)
        return True

    def logger(self):
        self._log = loghandler('ONEWIRE')
        self._log.handle(self._logcfg.get('LOGMODE'),self._logcfg)
        return True

    def getData(self):
        result={}
        basedir = self._onewire.get('BASEDIR','/temp')
        devicefile = self._onewire.get('DEVICEFILE','w1_slave')
        deviceId = self._onewire.get('DEVICEID','28')
      #  print(basedir,devicefile,deviceId)

        ds = ds18b20()
        dr = devicereader(basedir,deviceId,devicefile)
        devices = dr.readdevice()
     #   print('devices found:', devices)
        for deviceId, deviceFile in devices.items():
         #   print(dr.readfile(deviceFile))
            data = dr.readfile(deviceFile)
            if data is not None:
                ds.readValue(data)
                result[deviceId]=ds.getCelsius()

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
        self.startSystem()
        self.readconfig()
        self.logger()
        self._log.info('Start Reading Valuse')

        data = self.getData()
       # print('DAten',data)
        self._log.info(data)

        self.publishData(data)



if __name__ == '__main__':
    mgr = manager('/home/pi/m2m/onewire.cfg')
    mgr.run()
