import socket
import select
import sys
import threading

HOST=''
PORT=9999
SOCKET_LIST=[]
d={}
client_no=0
lock=threading.Lock()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(10)

SOCKET_LIST.append(server_socket)
print("chat server started on port 9999")

def broadcast(server_socket, sock, message):
	for socket in SOCKET_LIST:
	
		if socket != server_socket and socket != sock :
			try :
				socket.send(message.encode('utf-8'))
			except :
	
				print('df') 
				socket.close()
	
				if socket in SOCKET_LIST:
					SOCKET_LIST.remove(socket)

def user_connection_request(sockfd):
	global client_no,d
	while True:
		username=sockfd.recv(1024).decode('utf-8')
		if username not in d:
			sockfd.send("Username accepted".encode('utf-8'))
			break
			

		else:
			sockfd.send("Username not accepted,Enter a different username".encode('utf-8'))
	
	lock.acquire()

	client_no+=1
	d[username]=client_no
	SOCKET_LIST.append(sockfd)
	print("client connected ",username)
	broadcast(server_socket, sockfd, "%s entered our chatting room\n" % username)

	lock.release()



while True:
	ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST, [], [], 0)
	for sock in ready_to_read:

		if sock == server_socket:
			sockfd, addr = server_socket.accept()
			t=threading.Thread(target=user_connection_request,args=(sockfd,))
			t.start()		

		else:

			try:

				data = sock.recv(1024)
				if data:

					broadcast(server_socket, sock,data.decode('utf-8'))
				else:

					if sock in SOCKET_LIST:
						SOCKET_LIST.remove(sock)
						broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)

			except:
				broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
				continue

server_socket.close()

