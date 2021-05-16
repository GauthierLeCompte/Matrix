import socket
import threading
import json

HEADER = 64
# zeker zijn dat de port vrij is
PORT = 5050
# change to own IP4v address
SERVER = "192.168.0.241"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    """
    handled een client
    """
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    # blijf connected met de clients
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            # als de client disconnect -> disconnect
            if msg == DISCONNECT_MESSAGE:
                connected = False

            # print de message
            print(f"[{addr}] {msg}")
            try:
                # als de msg een json is open deze en schrijf deze uit
                resultdict = json.loads(msg)
                with open(f'{resultdict["row"]}{resultdict["col"]}.json', 'w') as fp:
                    json.dump(resultdict, fp)
                fp.close()
                conn.send("Msg received".encode(FORMAT))

            except ValueError:
                # als het geen json is kijk of het begint met een 1
                if msg[0] == "1":
                    #dit is een aanvraag voor een file -> als deze bestaat geef deze terug
                    try:
                        fi = open(f"{msg[1:]}.json")
                        dataname = json.load(fi)
                        fi.close()
                        tosend = json.dumps(dataname)
                        conn.send(f"{tosend}".encode(FORMAT))

                    except:
                        conn.send("no".encode(FORMAT))

                # als het iets anders is print error
                else:
                    conn.send("error".encode(FORMAT))

                print(msg)

    conn.close()

def start():
    """
    start de server en luister naar nieuwe clients
    """
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")

    # maak een nieuwe thread aan als er ene nieuwe client is en handle dit
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

#start de server
print("[STARTING] server is starting...")
start()
