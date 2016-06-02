#实验室考核作业-客户端
#使用时输入本机IP
import socket
import os
port = 12345
data_payload = 2048

def client(local_ip):
    cli_add = (local_ip, port)
    clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsock.bind(cli_add)
    print('start')
    clientsock.listen(1)
    while True:
        client, add = clientsock.accept()
        print('server is up, start to send file')
        save_file()
        f = open('result.txt', 'r')
        file = f.read(data_payload)
        client.send(file.encode())
        print('send success')
        f.close()
        client.close()        

def disk_stat():  
    disk = {'/media':None,'/home':None,'/':None}
    for each in disk.keys():
        dir = os.statvfs(each)
        hd = {'available':None, 'capacity':None, 'used':None}
        hd['available'] = round(dir.f_bsize*dir.f_bavail/1073741824, 2)
        hd['capacity'] = round(dir.f_bsize*dir.f_blocks/1073741824, 2)
        hd['used'] = round(dir.f_bsize*dir.f_bfree/1073741824, 2)
        disk[each] = hd
    return disk

def mem_stat():
    mem = dict.fromkeys(['Mem', 'Swap'])
    for each in list(os.popen('free -h')):
        m = {'total':None, 'used':None,'free':None}
        m['total'] = each.split()[1]
        m['used'] = each.split()[2]
        m['free'] = each.split()[3]
        if each.split()[0] == 'Mem:':
            mem['Mem'] = m
        if each.split()[0] == 'Swap:':
            mem['Swap'] = m
    return mem

def cpu_stat():
    cpu = dict.fromkeys(['Tasks', 'Cpu'])
    c = list(os.popen('top -bi -n 1'))
    cpu['Tasks'] = c[1].partition(' ')[2]
    cpu['Cpu'] = c[2].partition(' ')[2]
    return cpu 

def save_file():
    dict_file = open('result.txt', 'w')
    
    disk = disk_stat()
    mem = mem_stat()
    cpu = cpu_stat()
    for keys in disk:
        print(keys, end = ':  ', file = dict_file)
        for inkeys in disk[keys]:
            print('{0}:{1}G'.format(inkeys, disk[keys][inkeys]), end='  ', file = dict_file)
        print('\n', file = dict_file)
    
    for keys in mem:
        print(keys, end = ':  ', file = dict_file)
        for inkeys in mem[keys]:
            print('{0}:{1}'.format(inkeys, mem[keys][inkeys]), end='  ', file = dict_file)
        print('\n', file = dict_file)

    for keys in cpu:
        print('{0}:{1}'.format(keys, cpu[keys]), file = dict_file)
    dict_file.close()
    
if __name__ == '__main__':
    local_ip = input('please input local ip\n')
    client(local_ip)
