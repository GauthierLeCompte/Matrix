import socket
import json


#TODO: Uitleg class
class clientclass:
    """
    classe voor de clientside
    """
    # TODO: Uitleg functie
    def __init__(self, row_name, col_name):
        """
        initializeerd de classe met de rij en kollom naam
        """
        self.HEADER = 64
        #moet dezelfde port zijn als de server
        PORT = 5050
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        #change to own IP4v address
        SERVER = "192.168.0.241"
        ADDR = (SERVER, PORT)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)

        self.row_name = row_name
        self.col_name = col_name

    def ask(self):
        """
        vraag de server voor een json, alse deze bestaat return deze en anders return je None
        """
        msg = f"1{self.row_name}{self.col_name}"
        answer = self.send(msg)
        print(answer)
        if answer != "no":
            z = json.loads(answer)
            return z
        return None

    def update(self, result, i, final):
        """
        schrijf progress en results uit naar de server
        :param result: het beste resultaat tot nu toe (float)
        :param i: de hoeveelste itteratie is gebeurd (int)
        :param final: is dit het finale resultaat (bool)
        """
        progress = {"row": self.row_name, "col":self.col_name, "result":result, "i":i, "final": final}
        msg = json.dumps(progress)
        self.send(msg)

    def send(self, msg):
        """
        stuur een msg naar de server 
        eerst wordt dit ge-encode en dan verstuurd
        return wat de server antwoord
        """
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
        x = self.client.recv(2048).decode(self.FORMAT)
        return x

    def closee(self):
        """
        sluit de client
        """
        self.send(self.DISCONNECT_MESSAGE)
        self.client.close()


