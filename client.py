import socket, threading, time

SHUTDOWN = False


def main():
	global SHUTDOWN
	key = 8194

	s, server = make_connection()
	rT = make_receiving_pool(s, key)
	username = None

	while not SHUTDOWN:
		if username is None:
			username = join_user(s, server)
		else:
			try:
				send_message(s, server, username, key)
			except:
				SHUTDOWN = quit_user(s, server, username)

	rT.join()
	s.close()


def make_connection(server_url="127.0.1.1", server_port=9090, client_port=0):
	host = socket.gethostbyname(socket.gethostname())
	server = (server_url, server_port)

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((host, client_port))
	s.setblocking(0)

	return s, server


def make_receiving_pool(s, key):
	rT = threading.Thread(target=receving, args=("RecvThread", s, key))
	rT.start()

	return rT


def receving(name, sock, key):
	global SHUTDOWN
	while not SHUTDOWN:
		try:
			while True:
				data, _ = sock.recvfrom(1024)
				#print(data.decode("utf-8")
				decrypted = decrypt(data, key)
				print(decrypted)
				time.sleep(0.2)
		except:
			pass


def encrypt(message, key):
	encrypted = ""
	for i in message:
		encrypted += chr(ord(i)^key)
	
	return encrypted


def decrypt(data, key):
	decrypted = ""; k = False
	for i in data.decode("utf-8"):
		if i == ":":
			k = True
			decrypted += i
		elif k == False or i == " ":
			decrypted += i
		else:
			decrypted += chr(ord(i)^key)
	
	return decrypted


def join_user(s, server):
	username = input("Name: ")
	s.sendto((f"[{username}] => join chat ").encode("utf-8"), server)z

	return username


def send_message(s, server, username, key):
	message = input()
	message = encrypt(message, key)

	if message != "":
		s.sendto(("["+username + "] :: "+message).encode("utf-8"), server)
	
	time.sleep(0.2)


def quit_user(s, server, username):
	s.sendto(("["+username + "] <= left chat ").encode("utf-8"), server)
	return True


if __name__ == "__main__":
	main()
