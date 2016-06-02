import socket
import sys

port = 12345
data_payload = 2048

def sniff(local_ip):
    local_ip = str(local_ip).rpartition('.')[0]+'.'
    ip_add = ['%s%d' % (local_ip,x) for x in range(1,254)]
    
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    for each_ip in ip_add:
        ser_add = (each_ip, port)
        try:
            serversock.connect(ser_add)
            print('connect to %s' % each_ip)
            print('start receive file')
            file = serversock.recv(data_payload).decode()
            f = open('reveived_data_from_%s.txt' % each_ip, 'w')
            f.write(file)
            print('file is written')
            f.close()
        except:
           print('can\'t connect to %s' % each_ip)

if __name__ == '__main__':
    local_ip = input('please input local ip\n')
    sniff(local_ip)
