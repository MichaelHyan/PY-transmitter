from socket import *
import threading,os,json
print('system start')
class ser():
    def __init__(self,port = 1145):
        config = json.load(open('config.json'))
        self.info = []
        self.ip = config['ip']
        self.port = port
        self.buflen = 25600
        self.path = config['path']
        self.lsocket = socket(AF_INET,SOCK_STREAM)
        self.lsocket.bind((self.ip,port))
        self.lsocket.listen(8)
        self.code = 'utf-8'

    def dir(self):
        ls = os.listdir(self.path)
        l = ''
        for i in ls:
            l += i + '\n'
        return l[:-1]

    def upload(self,name,dsocket):
        try:
            f = open(f'{self.path}{name}','rb')
            dsocket.send(str(os.path.getsize(f'{self.path}{self.info[1]}')).encode())
            dsocket.recv(self.buflen)
            while True:
                data = f.read(self.buflen)
                if not data:
                    break
                dsocket.send(data)
        except:
            print('not found')
            dsocket.send('not found'.encode())

    def rec(self,name,dsocket):
        if "\\" in name:
            name = name.split('\\')[-1]
        if self.path[-1] == '\\':
            f = open(f'{self.path}{name}','wb')
        else:
            f = open(f'{self.path}\\{name}','wb')
        while True:
            data = dsocket.recv(self.buflen)
            if not data:
                break
            f.write(data)

    def buf(self,num):
        self.buflen = int(num)

    def remove(self,p):
        os.remove(f'{self.path}{p}')

    def main(self):
        while True:
            try:
                dsocket,addr = self.lsocket.accept()
                if dsocket:
                    print('C: connected')
                    self.info = dsocket.recv(self.buflen).decode(self.code)
                    self.info = self.info.split(' ')
                    if self.info[0] == 'dir':
                        print('cmd: dir')
                        dsocket.send(self.dir().encode(self.code))
                        print('complete')
                    elif self.info[0] == 'pull':
                        print(f'cmd: pull {self.info[1]}')
                        self.upload(self.info[1],dsocket)
                        print('complete')
                    elif self.info[0] == 'push':
                        print(f'cmd: push {self.info[1]}')
                        self.rec(self.info[1],dsocket)
                        print('complete')
                    elif self.info[0] == 'del':
                        print(f'cmd: del {self.info[1]}')
                        try:
                            self.remove(self.info[1])
                            print('complete')
                            dsocket.send('complete'.encode(self.code))
                        except:
                            print('not found')
                            dsocket.send('not found'.encode(self.code))
                    elif self.info[0] == 'buflen':
                        print(f'cmd: buflen {self.info[1]}')
                        if self.info[1] == 'reset':
                            buflen = 25600
                        else:
                            self.buf(self.info[1])
                        print(f'buflen set {buflen}')
                    elif self.info == 'exit':
                        print('cmd: exit')
                        dsocket.close()
                    elif self.info[0] == 'bar':
                        pass
                    elif self.info[0] == 'tick':
                        pass
                    else:
                        print('unknown cmd')
                    dsocket.close()
            except:
                pass
a = ser(1145)
a.main()