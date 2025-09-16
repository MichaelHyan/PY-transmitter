from socket import *
import os,threading, math,json
config = json.load(open('config.json'))
ip = config['ip']
port = config['port']
buflen = 25600
tic = 100
path = config['path']
code = 'utf-8'
sb = 1#意思是show bar，或者是傻*


def bar(m,n):
    i = math.floor(10*n/m)
    n = n//10000
    m = m//10000
    a = [[0,f'[□□□□□□□□□□] {n}:{m}'],
         [1,f'[■□□□□□□□□□] {n}:{m}'],
         [2,f'[■■□□□□□□□□] {n}:{m}'],
         [3,f'[■■■□□□□□□□] {n}:{m}'],
         [4,f'[■■■■□□□□□□] {n}:{m}'],
         [5,f'[■■■■■□□□□□] {n}:{m}'],
         [6,f'[■■■■■■□□□□] {n}:{m}'],
         [7,f'[■■■■■■■□□□] {n}:{m}'],
         [8,f'[■■■■■■■■□□] {n}:{m}'],
         [9,f'[■■■■■■■■■□] {n}:{m}'],
         [10,f'[■■■■■■■■■■] {n}:{m}']]
    print(a[i][1])

def upload(name):
    try:
        if "\\" in name:
            f = open(f'{name}','rb')
            size = os.path.getsize(name)
        else:
            if path[-1] == '\\':
                f = open(f'{path}{name}','rb')
            else:
                f = open(f'{path}\\{name}','rb')
            size = os.path.getsize(f'{path}{name}')
        len = 0
        while True:
            data = f.read(buflen)
            if not data:
                break
            len += 1
            if len%tic == 0 and sb == 1:
                bar(size,len*buflen)
            dsocket.send(data)
    except:
        print('没找到文件(悲')

def rec(name):
    f = open(f'{path}{name}','wb')
    size = dsocket.recv(buflen)
    if size != b'not found':
        size = int(size)
    dsocket.send(b' ')
    len = 0
    while True:
        data = dsocket.recv(buflen)
        if data == b'not found':
            print('没找到文件(悲')
            break
        if not data:
            break
        len += 1
        if len%tic == 0 and sb == 1:
            bar(size,len*buflen)
        f.write(data)

def help():
    print('---------------------------')
    print('dir: 列出服务器文件')
    print('pull <name>: 下载文件')
    print('push <name>: 上传文件')
    print('buflen <size>: 修改缓存区大小')
    print('del <name>: 删除文件')
    print('bar <bool>: 显示/隐藏进度条')
    print('tick <int>: 修改进度条刷新间隔')
    print('exit: 退出')
    print('---------------------------')

while True:
    dsocket = socket(AF_INET,SOCK_STREAM)
    dsocket.connect((ip,port))
    if dsocket:
        print(f'连接至 {ip}:{port}')
        cmd = input('>>')
        if cmd == 'exit':
            dsocket.close()
            break
        dsocket.send(cmd.encode(code))
        if cmd[1] == ':':
            c = cmd
            cmd = ['','']
            cmd[0] = 'push'
            cmd[1] = c
        else:
            cmd = cmd.split()
        if cmd[0] == 'dir':
            print('---------------------------')
            print(dsocket.recv(buflen).decode(code))
            print('---------------------------')
        elif cmd[0] == 'pull':
            name = cmd[1]
            rec(name)
            print(f'下载 {name} 完成！')
        elif cmd[0] == 'push':
            name = cmd[1]
            upload(name)
            print(f'上传 {name} 完成！')
        elif cmd[0] == 'buflen':
            print(f'缓存区更改: {cmd[1]}')
            if cmd[1] == 'reset':
                buflen = 25600
            else:
                buflen = int(cmd[1])
        elif cmd[0] == 'del':
            info = dsocket.recv(buflen).decode(code)
            if info == 'complete':
                print('删除成功！')
            else:
                print('没找到文件(悲')
        elif cmd[0] == 'bar':
            try:
                sb = int(cmd[1])
                print(f'进度条显示:{bar}')
            except:
                bar = True
        elif cmd[0] == 'help':
            help()
        elif cmd[0] == 'tick':
            tic = int(cmd[1])
            print(f'进度条刷新间隔更改: {tic}')
        else:
            print('雜魚❤！服务器酱不知道你在说什么')
        dsocket.close()

