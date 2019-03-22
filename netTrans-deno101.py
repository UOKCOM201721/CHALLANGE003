import socket
import platform
import subprocess as sub
import threading as th
import colorama as colo
import struct
import sys
import os
import math
import time


def progressbar(count, total, suffix=''):
    barlen = 40
    if count >= total:
        total = count

    filledlen = int(round(barlen * count/float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = bytes((219,)).decode('cp437') * filledlen + '-' * (barlen - filledlen)
    sys.stdout.write("[%s] %s%s ...%s\r" % (bar, percents, "%", suffix))
    sys.stdout.flush()


class Client:
    def main(self):
        print(colo.Fore.GREEN + "Client" + colo.Style.RESET_ALL)
        ip = input("Enter destination ip:" )
        if ip in ('q', 'quit', 'exit'):
            sys.exit(0)
        sock = socket.socket()
        addrs = (ip, 40000)
        try:
            sock.connect(addrs)
        except socket.gaierror:
            print('[Errno -2] Name or service not known')
            self.main()
        except ConnectionRefusedError:
            print('[Errno 111] Connection refused')
            self.main()
        print('[' + colo.Fore.GREEN + "Connect" + colo.Style.RESET_ALL+ ']'+ ip)
        filetosend = input("Enter file to send: ")
        f = None
        try:
            f = open(filetosend, 'rb')
        except FileNotFoundError:
            print('[Errno 2] No such file or directory: ')
            self.main()

        leny = math.ceil(os.stat(filetosend).st_size)
        if leny <= 0:
            print("[Errono 5] Cannot send an empty file")
            self.main()
        filelen = struct.pack("<I", leny)
        filenamelen = struct.pack("<I", len(filetosend))
        sock.sendall(filelen + filenamelen)
        sock.sendall(bytes(filetosend, 'utf-8'))
        # print('debug', len(filetosend))
        # print('debug2', len(filetosend), type(filetosend))
        bufferx = 1024
        i = 0
        while True:
            data = f.read(bufferx)
            sock.send(data)
            progressbar(i, leny)
            if not data:
                break
            i += bufferx
        f.close()
        print()
        print('[' + colo.Fore.GREEN + " SUCCESS " + colo.Style.RESET_ALL + ']' + 'sent {%s}' % filetosend)
        self.main()


class Server:
    def __init__(self):
        self.enc = 'utf-8'

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
        try:
            sock.bind(addresses)
        except OSError:
            print('[Errno 98] (%s) Address already in use' % addr)
            return
        print('[' + colo.Fore.GREEN + " OK " + colo.Style.RESET_ALL + ']' + ('Success bind to {%s}' % addr))
        sock.listen(100)
        try:
            while True:
                c, addrinfo = sock.accept()
                #print('[' + colo.Fore.GREEN + " CONNECT " + colo.Style.RESET_ALL + ']' + ('To {%s} ' % addrinfo[0]))
                t = th.Thread(target=self.serverProcessing, args=(c, addrinfo,))
                t.start()
        except KeyboardInterrupt:
            sys.exit(1)


    def startServer(self):
        bindaddrs = self.getlocalip()
        for x in bindaddrs:
            t = th.Thread(target=self.bind, args=(x,))
            t.start()

    def serverProcessing(self, c, addrinfo):
        info = c.recv(8)
        # print(info)
        filelen = struct.unpack("<I", info[:4])[0]
        filenamelen = struct.unpack("<I", info[4:])[0]
        filename = c.recv(filenamelen)
        try:
            file = open(filename.decode('utf-8'), "wb")
        except FileNotFoundError:
            return
        alldata = bytes('', 'utf-8')
        i = 0
        while i < filelen:
            sys.stdout.flush()
            bufferx = 1024
            data = c.recv(bufferx)
            file.write(data)
            i += bufferx
        file.close()
        c.close()
        #print()
        #print('[' + colo.Fore.GREEN + " OK " + colo.Style.RESET_ALL + ']' + 'complete')
        #Client().main()


if __name__ == '__main__':

    t = th.Thread(target=Server().main)
    # t.daemon = True
    t.start()
    time.sleep(1)
    try:
        Client().main()
    except KeyboardInterrupt:
        print("\nExiting with exit code[0]")
        sys.exit()

