import socket
import time

from message import Message


def main():
	s, clients = make_connection()
	
	while True:
		try:
			msg, addr = get_info(s)
			send_info(s, clients, msg, addr)
			if addr not in clients:
				clients.append(addr)
				key_exchange(s, clients)
			elif msg.type == "quit":
				clients.remove(addr)
				key_exchange(s, clients)
		except KeyboardInterrupt:
			print("\n[ Server stopped ]")
			break
	
	s.close()


def make_connection(port=9090):
	host = socket.gethostbyname(socket.gethostname())
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((host, port))

	print(f"[ Server started on {host}:{port} ]")

	return s, []


def get_info(s):
	data, addr = s.recvfrom(1024)
	msg = Message().from_json(data)
	
	itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())

	print(f"[{addr[0]}]=[{addr[1]}]=[{itsatime}]/",end="")
	print(msg)

	return msg, addr


def send_info(s, clients, message, addr):
	for client in clients:
		if addr != client:
			message.send(s, client)


def key_exchange(s, clients, g=2):
	keys = {k:g for k in clients}
	n = len(clients)
	for i in range(n - 1):
		new_keys = {}
		for j in range(n):
			Message("get_key", keys[clients[(j + 1) % n]]) \
				.send(s, clients[j])
			while True:
				try:
					msg, addr = get_info(s)
					new_keys[addr] = msg.content
					break
				except KeyboardInterrupt:
					break
		
		keys = new_keys

	for i in range(n):
		Message("set_key", keys[clients[(i + 1) % n]]).send(s, clients[i])


if __name__ == "__main__":
	main()
