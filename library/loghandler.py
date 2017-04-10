import logging
import logging.handlers
import socket


class loghandler(object):

    def __init__(self,name):

        self._loghandle = ''

        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)

   #     hostname = socket.gethostname()
    #    formatter = logging.Formatter('%(asctime)s %(name)s: %(levelname)s %(message)s'.format(hostname),'%b %e %H:%M:%S')

     #   handler = logging.handlers.SysLogHandler(address=(syslogHost, 514), facility=19)
      #  handler.setFormatter(formatter)

       # self._logger.addHandler(handler)

    def level(self,level):
        if level in 'INFO':
            self._logger.setLevel(logging.INFO)
        elif level in 'DEBUG':
            self._logger.setLevel(logging.DEBUG)
        return True

    def handle(self,methode,config):
        print (methode)
        if 'SYSLOG' in methode:
          #  print('Ssyslog',config )
            host = config.get('LOGSERVER','localhost')
           # print('Syslog',host)
            handler = logging.handlers.SysLogHandler(address=(host, 514), facility=19)

            hostname = socket.gethostname()
            formatter = logging.Formatter('%(asctime)s %(name)s: %(levelname)s %(message)s'.format(hostname),'%b %e %H:%M:%S')
            handler.setFormatter(formatter)

        self._logger.addHandler(handler)

        return True



    def debug(self,msg):
    #    print('debug',msg)
        self._logger.debug(msg)

    def info(self,msg):
     #   print('info',msg)
        self._logger.info(msg)

    def warning(self,msg):
      #  print('critical',msg)
        self._logger.warning(msg)

    def error(self,msg):
       # print('critical',msg)
        self._logger.error(msg)

    def critical(self,msg):
#        print('critical',msg)
        self._logger.critical(msg)

class app(object):

    def __init__(self,log):
        self._log = log
        self._log.info('start')

    def methode(self, x):
        msg = 'test' + x
        self._log.debug(msg)


if __name__ == '__main__':
    log = logger('TEST')
    log.handle('SYSLOG',{'HOST':'172.17.115.121'})
    log.info('TEST')
    appX = app(log)
    appX.methode('iii')