from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from Person import Person

# GLOBAL CONSTANTS
HOST = "localhost"
PORT = 5500
BUFSIZ = 512
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10

#  GLOBAL VARIABLES
persons = []
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)  # set up server


def broadcast(msg, name):
    """
    Send new messages to all clients
    :param msg: byte["utf8"]
    :param name: str
    :return:
    """
    for person in persons:
        try:
            client = person.client
            client.send(bytes(name, "utf8") + msg)
        except Exception as e:
            print("[EXCEPTION", e)


def client_communication(person):
    """
    Thread to handle all messages from client
    :param person: Person
    :return: None
    """
    client = person.client

    # received the person name
    name = client.recv(BUFSIZ).decode("utf8")
    person.set_name(name)
    msg = bytes(f"{name} has joined the chat!", "utf8")
    broadcast(msg, "")  # broadcast welcome message

    while True:  # wait for messages from clients
        try:
            msg = client.recv(BUFSIZ)

            if msg == bytes("{quit}", "utf8"):  # disconnect client if message is quit
                client.close()
                persons.remove(person)
                broadcast(f"{name} has left the chat...", "")
                print(f"[DISCONNECTED] {name} disconnected")
                break
            else:  # send messages to all others clients
                broadcast(msg, name + ": ")
                print(f"{name}: ", msg.decode("utf8"))

        except Exception as e:
            print("[EXCEPTION]", e)
            break


def wait_for_connection():
    """
    Wait for connection from new clients, start new thread once connected
    :return: None
    """
    while True:
        try:
            client, addr = SERVER.accept()  # wait for connections
            person = Person(addr, client)  # create new person for connection
            persons.append(person)

            print(f"[CONNECTION] {addr} connected to the server at {time.time()}")
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print("[EXCEPTION]", e)
            break

    print("SERVER CRASHED")


if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS)  # Listen for connections
    print("[STARTED] Waiting for connections...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
