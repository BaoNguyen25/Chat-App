from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


class Client:
    """
    Communication with server
    """
    HOST = "localhost"
    PORT = 5500
    ADDR = (HOST, PORT)
    BUFSIZ = 512

    def __init__(self, name):
        """
        Initialize client object
        :param name: str
        """
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages = []
        receive_thread = Thread(target=self.receive_message)
        receive_thread.start()
        self.send_message(name)

    def receive_message(self):
        """
        Handles receiving of messages from server
        :return: None
        """
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode()
                self.messages.append(msg)
                print(msg)
            except Exception as e:
                print("[EXCEPTION", e)
                break

    def send_message(self, msg):
        """
        Handles sending of messages to server
        :param msg: str
        :return: None
        """
        self.client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            self.client_socket.close()

