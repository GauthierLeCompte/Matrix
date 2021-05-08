import socket
import threading
import json

HEADER = 64
PORT = 5050
SERVER = "192.168.0.240"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            try:
                z = json.loads(msg)
                with open(f'{z["row"]}{z["col"]}.json', 'w') as fp:
                    json.dump(z, fp)
                fp.close()
                conn.send("Msg received".encode(FORMAT))


            except ValueError:
                if msg[0] == "1":
                    try:
                        fi = open(f"{msg[1:]}.json")
                        dataname = json.load(fi)
                        fi.close()
                        tosend = json.dumps(dataname)
                        conn.send(f"{tosend}".encode(FORMAT))

                    except:
                        conn.send("no".encode(FORMAT))


                else:
                    conn.send("Msg1 received".encode(FORMAT))

                print(msg)

    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()