import socket
import threading
import time

from message import Message
from encryptor import Encryptor


USER = None
SHUTDOWN = False


def main():
    global SHUTDOWN
    key = 8194

    s, server = make_connection()
    join_user(s, server)
    rT = make_receiving_pool(s, server, key)

    while not SHUTDOWN:
        try:
            send_message(s, server)
        except KeyboardInterrupt:
            SHUTDOWN = quit_user(s, server)

    rT.join()
    s.close()


def make_connection(server_url="127.0.1.1", server_port=9090, client_port=0):
    host = socket.gethostbyname(socket.gethostname())
    server = (server_url, server_port)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, client_port))
    s.setblocking(0)

    return s, server


def make_receiving_pool(s, server, key):
    rT = threading.Thread(target=receving, args=("RecvThread", s, server))
    rT.start()

    return rT


def receving(name, sock, server):
    global SHUTDOWN
    global USER
    while not SHUTDOWN:
        try:
            while True:
                data, _ = sock.recvfrom(1024)
                msg = Message().from_json(data)
                if msg.type == "crypto":
                    decrypted = USER.decrypt_message(msg.content)
                    print(decrypted)
                elif msg.type == "get_key":
                    key = USER.generate_key(msg.content)
                    Message("get_key", key).send(sock, server)
                elif msg.type == "set_key":
                    USER.key = USER.generate_key(msg.content)
                else:
                    print(msg.content)
                time.sleep(0.2)
        except BlockingIOError:
            pass
        except Exception as e:
            print(e)


def join_user(s, server):
    global USER
    username = input("Name: ")
    USER = Encryptor(username)
    Message("info", f"[{username}] => join chat ").send(s, server)

    return username


def send_message(s, server):
    global USER
    data = input()
    data = f"[{USER.name}] :: {data}"
    data = USER.encrypt_message(data)

    if data != "":
        Message("crypto", data).send(s, server)
    
    time.sleep(0.2)


def quit_user(s, server):
    global USER
    Message("quit", f"[{USER.name}] <= left chat ").send(s, server)

    return True


if __name__ == "__main__":
    main()
