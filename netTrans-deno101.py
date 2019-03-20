import socket
import platform
import subprocess as sub
import threading as th
import colorama as colo

class Server:
    def __init__(self):
        pass

    def getlocalip(self):
        if platform.system() == 'Windows':
            command = 'ipconfig | findstr IPv4'
            x = self.fromsub(command, '\r\n')
            x.append('127.0.0.1')
            return x
        elif platform.system() == 'Linux':
            command = 'ifconfig | grep netmask'
            x = self.fromsub(command, '\n')
            return x

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

    def main(self):
        self.startServer()

    def bind(self, addr):
        sock = socket.socket()
        addresses = (addr, 40000)
        sock.bind(addresses)
        print('[' + colo.Fore.GREEN + " OK " + colo.Style.RESET_ALL + ']' + ('Success bind to {%s}' % addr))
        while True:
            sock.listen(10)
            c, addrinfo = sock.accept()
            print('[' + colo.Fore.GREEN + " CONNECT " + colo.Style.RESET_ALL + ']' + ('To {%s} ' % addrinfo[0]))
            self.serverProcessing(c, addrinfo)

    def startServer(self):
        bindaddrs = self.getlocalip()
        for x in bindaddrs:
            t = th.Thread(target=self.bind, args=(x,))
            t.start()

    def serverProcessing(self, c, addrinfo):
        pass


if __name__ == '__main__':
    Server().main()

