import socket
import json



class clientclass:
    def __init__(self, row_name, col_name):
        self.HEADER = 64
        PORT = 5050
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        SERVER = "192.168.0.240"
        ADDR = (SERVER, PORT)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)

        self.row_name = row_name
        self.col_name = col_name
        self.best_result = 0

    def ask(self):
        msg = f"1{self.row_name}{self.col_name}"
        answer = self.send(msg)
        if answer != "no":
            z = json.loads(answer)
            with open(f'{z["row"]}{z["col"]}.json', 'w') as fp:
                json.dump(z, fp)
            fp.close()

    def update(self, result, i, final):
        if result > self.best_result:
            self.best_result = result
        progress = {"row": self.row_name, "col":self.col_name, "result":result, "i":i, "final": final}
        msg = json.dumps(progress)
        # msg = f"row {self.row_name} is evaluating {self.col_name} as result {result}"
        self.send(msg)

    def send(self, msg):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
        x = self.client.recv(2048).decode(self.FORMAT)
        print(x)
        return x

    def closee(self):
        self.send(self.DISCONNECT_MESSAGE)
        self.client.close()


