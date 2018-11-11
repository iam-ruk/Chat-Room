import socket
import select
import sys
import threading

HOST=''
PORT=9999
SOCKET_LIST=[]
d={}
lock=threading.Lock()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(10)

SOCKET_LIST.append(server_socket)
SOCKET_LIST.append(sys.stdin)
print("chat server started on port 9999")

def broadcast(server_socket, sock, message):
	for socket in SOCKET_LIST:
	
		if socket != server_socket and socket != sock and socket !=sys.stdin :
			try :
				socket.send(message.encode('utf-8'))
			except :
	
				socket.close()
	
				if socket in SOCKET_LIST:
					SOCKET_LIST.remove(socket)

def user_connection_request(sockfd):
	global d
	while True:
		username=sockfd.recv(1024).decode('utf-8')
		if username not in d:
			sockfd.send("Username accepted".encode('utf-8'))
			break
			

		else:
			sockfd.send("Username not accepted,Enter a different username".encode('utf-8'))
	
	lock.acquire()

	SOCKET_LIST.append(sockfd)
	d[username]=sockfd
	print("client connected ",username)
	broadcast(server_socket, sockfd, "%s entered our chatting room\n" % username)

	lock.release()



while True:
	ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST, [], [],0)
	for sock in ready_to_read:

		if sock == server_socket:
			sockfd, addr = server_socket.accept()
			t=threading.Thread(target=user_connection_request,args=(sockfd,))
			t.start()
		
		elif sock == sys.stdin:
				
			user_del=sys.stdin.readline().strip()
			print(user_del)
			print(d)
			if user_del in d:
				sock_del=d[user_del]
				
				SOCKET_LIST.remove(sock_del)
				sock_del.close()
				broadcast(server_socket, sock_del, "%s left our chatting room\n" % user_del)				


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

