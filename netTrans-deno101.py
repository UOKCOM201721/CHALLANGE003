import socket
import platform
import subprocess as sub


class Server:
    def __init__(self):
        pass

    def getlocalip(self):
        if platform.system() == 'Windows':
            command = 'ipconfig | findstr IPv4'
            print(self.fromsub(command, '\r\n'))
        elif platform.system() == 'Linux':
            command = 'ifconfig | grep netmask'
            print(self.fromsub(command, '\n'))

    def fromsub(self, command, nxtline):
        run = sub.Popen(command, stdout=sub.PIPE, shell=True)
        output = run.communicate()
        allipinfo = output[0].strip().decode('utf-8').split(nxtline)
        finarray = []

        for x in allipinfo:
            nospace = x.split(' ')
            i = 0
            while i < len(nospace):
                if nospace[i] == '':
                    nospace.pop(i)
                    i -= 1
                i += 1
            if platform.system() == 'Linux':
            	finarray.append(nospace[1])
            elif platform.system() == 'Windows':
            	finarray.append(nospace[len(nospace)-1])

        return finarray


Server().getlocalip()

