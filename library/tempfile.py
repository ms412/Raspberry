import json

class tempfile(object):

    def __init__(self,filename,logChannel):

        self._filename = filename
        self._log = logChannel

    def openfile(self):

        try:
            with open(self._filename)as fh:
                data = json.load(fh)
            #    print('test',data)
                fh.close()

        except IOError:
            data = None

        return data


    def writefile(self,data):

            with open(self._filename,'w')as fh:
                json.dump(data,fh,indent =4)

