
import minimalmodbus

class mgr_modbus(object):
    def __init__(self,config,logHandle):

        self._log = logHandle

        self._interface = str(config.get('INTERFACE','/dev/ttyUSB0'))
        self._baudrate = int(config.get('BAUDRATE',9800))

        self._if = None


    def setup(self):
        self._if = minimalmodbus.Instrument(self._interface,3)
        self._if.serial.baudrate = self._baudrate
        self._if.timeout = 0.8
        self._if.debug = False

    def read(self,data):
        print('test',self._if)
        typ,value,size = data
        if 'int' in typ:
           # print('type int',value)
            print('read int',value,int(size))
            value = self._if.read_register(int(value,16),int(size))
         #   value = '8'
        elif 'str' in typ:
            print('type string',value,size)
          #  value ='TEST'
            value = self._if.read_string(int(value,16),int(size))
        else:
            value = None

        return value


       # print(typ,value,size)


