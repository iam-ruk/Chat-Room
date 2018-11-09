import socket
from time import sleep
import select
import sys
import re

s=socket.socket()
try:
    s.connect(('localhost', 9999))

except:
    print('Could not connect to the host')
    sys.exit()

print('you are connected to the host, you can send all your msgs')
username=input('Enter an username of your choice')
s.send(username.encode('utf-8'))
response=s.recv(1024).decode('utf-8')
while True:
	print(response)
	m=re.match('Username accepted',response,re.I)
	if m is not None:
		break
	else:
		username=input('Enter an username of your choice')
		s.send(username.encode('utf-8'))
		response=s.recv(1024).decode('utf-8')

while 1:
    socket_list=[sys.stdin, s]
    read_l, write_l, error_l = select.select(socket_list, [], [])

    for sock in read_l:
        if sock == s:
            data=s.recv(1024)
            if not data:
                print('Disconnected from the server')
                sys.exit()
            else:
                print(data.decode('utf-8'))
        else:
            input_text=sys.stdin.readline().strip()
            if input_text=='q':
                s.send('Client says bye'.encode('utf-8'))
                sys.exit()
            s.send((username +':' + input_text).encode('utf-8'))
