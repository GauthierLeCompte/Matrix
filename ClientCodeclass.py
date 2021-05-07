import socket




class clientclass:
    def __init__(self, row_name, col_name):
        self.HEADER = 64
        PORT = 5050
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        SERVER = "127.0.1.1"
        ADDR = (SERVER, PORT)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)

        self.row_name = row_name
        self.col_name = col_name
        self.r = 0


    def update(self, result):
        if result > self.r:
            self.r = result
        msg = f"row {self.row_name} is evaluating {self.col_name} as result {result}"
        self.send(msg)

    def send(self, msg):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
        print(self.client.recv(2048).decode(self.FORMAT))

    def closee(self):
        self.send(self.DISCONNECT_MESSAGE)
        self.client.close()


