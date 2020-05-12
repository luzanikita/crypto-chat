import socket, time


def main():
	s, clients = make_connection()
	
	while True:
		try:
			data, addr = get_info(s)
			send_info(s, clients, data, addr)
		except:
			print("\n[ Server stopped ]")
			break
	
	s.close()


def make_connection(port=9090):
	host = socket.gethostbyname(socket.gethostname())
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((host, port))

	print(f"[ Server started on {host}:{port} ]")

	return s, {}


def get_info(s):
	data, addr = s.recvfrom(1024)
	itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())

	print("["+addr[0]+"]=["+str(addr[1])+"]=["+itsatime+"]/",end="")
	print(data.decode("utf-8"))

	return data, addr


def send_info(s, clients, data, addr):
	if addr not in clients:
		clients[addr] = data.decode("utf-8").split(":")[-1]
	
	for client in clients:
		if addr != client:
			s.sendto(data, client)


if __name__ == "__main__":
	main()
