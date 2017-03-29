import json
import time

from threading import Thread
from threading import Event
from queue import Queue
import time


'''
import device interface drivers
'''
from library.gpio import raspberry
#from library.dummy import dummy
#from module.devices.mcp23017 import MCP23017


from library.tempfile import tempfile


class S0(object):

    def __init__(self,hwHandle,cfg,logChannel):

        self._hwHandle = hwHandle
        self._cfg = cfg
        self._log = logChannel

        '''
        System parameter
        '''
        print('Startup',self._cfg)
        self._pin = int(self._cfg.get('GPIO',None))
        self._factor = int(self._cfg.get('FACTOR',1000))
        self._accuracyWatt = int(self._cfg.get('ACCURACY',360))
        self._attenuator = str(self._cfg.get('ATTENUATOR','UP'))
        self._trigger = str(self._cfg.get('TRIGGER','RISING'))
        self._debounce = int(self._cfg.get('DEBOUNCE',100))
        self._power = float(self._cfg.get('POWER',0))
        self._energy = float(self._cfg.get('ENERGY',0))

        '''
        Class variables
        '''
        self._powerData = []
        self._t_update = 0
        self._pulsCounter = 0

        self.setup()



    def setup(self):

        self._powerData.append(self._power)
        self._t_update = time.time()

        self._accuracySec = 3600 * 1000 / self._factor / self._accuracyWatt

        if not self._pin == None:
            self._hwHandle.ConfigIO(self._pin,'IN',self._attenuator)
            self._hwHandle.Edge(self._pin,self.callback,self._trigger,self._debounce)

        return True

    def callback(self,pin):

        if self._pulsCounter > 1:

          #  print('Test',self._t_update,self._powerData)

            _timeCurrent = time.time()

            self._powerData.append(self.power(self._t_update,_timeCurrent))
            self._t_update = _timeCurrent

        else:
            print('First Puls now Start')

        self._pulsCounter = self._pulsCounter + 1

      #  print('callback',self._powerData)
        return True

    def get(self):
        _msg = {}
        _msg['POWER'] = self.getPower()
        _msg['ENERGY'] = self.energy()

        return _msg

    def getPower(self):

        _result = 0
        #print('getPower',self._t_update,self._powerData)

        if self._t_update < time.time() - self._accuracySec:
            _result = 0
           # print('Nothing')
        else:
            _result = self.average(self._powerData)
          #  print('Result',_result)
        del self._powerData[:]
        self._powerData.append(_result)

        return _result

    def average(self,datalist):
        _result = 0

        for item in datalist:
            _result = _result + item

        #print('Reslut',_result,len(datalist))
        _result = _result / len(datalist)
        return _result

    def power(self,t0,t2):
        t1 = t2 - t0
#        print (t1, self._factor)
        _watt = 3600 * 1000 / self._factor / t1
      #  print('Watt',_watt)
  #      log_msg = 'Calculate power'
   #     self.msgbus_publish(self._log, '%s %s: %s %s Result %s' % ('DEBUG', self.whoami(), log_msg, self._pin, _watt))
        return _watt

    def energy(self):
        energySum = float(self._pulsCounter / self._factor)
        energySum = energySum + self._energy

    #    log_msg = 'Calculate energy'
    #    self.msgbus_publish(self._log, '%s %s: %s %s Result %s' % ('DEBUG', self.whoami(), log_msg, self._pin, energySum))
        return energySum





class S0manager(Thread):

    def __init__(self,config,sink,source,logChannel):
        Thread.__init__(self)


        self._cfg = config
        self._msgSink = sink
        self._msgSource = source
        self._log = logChannel
        self._tmpfilename = self._cfg.get('TEMPFILE','S02mqtt.temp')
        #del self._cfg['TEMPFILE']

        '''
        Hardware handel stores the handle to the hardware
        only once available per VDM instance
        '''
        self._hwHandle = None
        self._devHandle = {}

        self._counter = 0
        self._power = 0
        self._energy = 0
        self._result = {}

        self._threadRun = True

        self.msg = {}

        log_msg = 'Startup GPIO Adapter with config'
        self.msgbus_publish(self._log,'%s %s: %s %s' % ('INFO', self.whoami(), log_msg, self._cfg))

        self.setup()

    def __del__(self):
        '''
        stop all concerning VPM objects before destroying myself
        '''

        for key, value in self._VPMobj:
            del value

        self.msgbus_publish(self._log,'%s GPIO Module Destroying myself: %s '%('DEBUG', self._DevName))

    def whoami(self):
        return type(self).__name__

    def setup(self):
        self._tempFile = tempfile(self._tmpfilename, self._log)
        tmpdata = self._tempFile.openfile()

        if tmpdata == None:
          #  print('file does not exist')
            log_msg = 'Tempfile does not exist'
            self.msgbus_publish(self._log,'%s %s: %s %s' % ('DEBUG', self.whoami(), log_msg, self._tmpfilename))
        else:
            #print('Data',tmpdata)
            log_msg = 'Tempfile exit read old values'
            self.msgbus_publish(self._log, '%s %s: %s %s' % ('INFO', self.whoami(), log_msg, tmpdata))


     #   print('Config',self._cfg)
        #self._hwHandle = dummy()
        self._hwHandle = raspberry(self._log)

        for _pin, _cfg in self._cfg.items():
            print(_pin, _cfg)
            if isinstance(_cfg, dict):
                if tmpdata != None:
                    _tmp = tmpdata.get(_pin,None)
                    #print('Temp',_tmp,_pin,tmpdata.get('ENERGY',0))
                    if None == _tmp:
                        _cfg['ENERGY'] = 0
                        _cfg['POWER'] = 0
                    else:
                        _cfg['ENERGY'] = _tmp.get('ENERGY',0)
                        _cfg['POWER'] = _tmp.get('POWER',0)
           #        _cfg['TIME'] = _tmp.get('TIME',0)

                #self._devHandle[_pin] = S0(self._hwHandle, _pin, _cfg, self._log)
                self._devHandle[_pin] = S0(self._hwHandle, _cfg, self._log)

    def run(self):

      #  self.msgbus_publish(self._log,'%s VDM Virtual Device Manager %s Startup'%('INFO', self._DevName))
       # threadRun = True


        _timeT0 = time.time()
        _timeDelta = 60
        _timeT1 = _timeT0 + _timeDelta


        while self._threadRun:
            time.sleep(0.3)
           # for key,value in self._devHandle.items():
          #      print('.',key,value)
                #value.run()

          #  print('Test',_timeT1,time.time())
            if time.time() > _timeT1:
              #  print('Send update')
                log_msg = 'Timer expired get update'
                self.msgbus_publish(self._log, '%s %s: %s ' % ('DEBUG', self.whoami(), log_msg))

                for key,value in self._devHandle.items():
          #         print('.',key,value)
                    self.msg[key]=value.get()
                    self._tempFile.writefile(self.msg)

              #  print('power',self.msg)
                log_msg = 'Send Update'
                self.msgbus_publish(self._log, '%s %s: %s %s' % ('DEBUG', self.whoami(), log_msg, self.msg))
                self.msgbus_publish(self._msgSource,self.msg)

                _timeT1 = time.time() + _timeDelta