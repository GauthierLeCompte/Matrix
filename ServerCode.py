import socket
import threading
import json

#TODO: Uitleg variabelen
HEADER = 64
PORT = 5050
SERVER = "192.168.0.241"
# SERVER = "192.168.0.104"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

#TODO: Uitleg functie
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    # TODO: Uitleg
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        # TODO: Uitleg
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            # TODO: Uitleg
            if msg == DISCONNECT_MESSAGE:
                connected = False

            # TODO: Uitleg
            print(f"[{addr}] {msg}")
            try:
                resultdict = json.loads(msg)
                with open(f'{resultdict["row"]}{resultdict["col"]}.json', 'w') as fp:
                    json.dump(resultdict, fp)
                fp.close()
                conn.send("Msg received".encode(FORMAT))

            # TODO: Uitleg
            except ValueError:
                # TODO: Uitleg
                if msg[0] == "1":
                    try:
                        fi = open(f"{msg[1:]}.json")
                        dataname = json.load(fi)
                        fi.close()
                        tosend = json.dumps(dataname)
                        conn.send(f"{tosend}".encode(FORMAT))

                    except:
                        conn.send("no".encode(FORMAT))

                # TODO: Uitleg
                else:
                    conn.send("Msg1 received".encode(FORMAT))

                print(msg)

    conn.close()

#TODO: Uitleg functie
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")

    # TODO: Uitleg
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()