import socket
import platform
import subprocess as sub


class Server:
    def __init__(self):
        pass

    def getlocalip(self):
        if platform.system() == 'Windows':
            pass
        elif platform.system() == 'Linux':
            command = 'ifconfig | grep netmask'
            print(self.fromsub(command))

    def fromsub(self, command):
        run = sub.Popen(command, stdout=sub.PIPE, shell=True)
        output = run.communicate()
        allipinfo = output[0].strip().decode('utf-8').split('\n')
        finarray = []

        for x in allipinfo:
            nospace = x.split(' ')
            i = 0
            while i < len(nospace):
                if nospace[i] == '':
                    nospace.pop(i)
                    i -= 1
                i += 1
            finarray.append(nospace[1])

        return finarray


Server().getlocalip()

