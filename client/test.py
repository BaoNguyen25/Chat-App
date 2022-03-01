from client import Client
from threading import Thread
import time

c1 = Client("Vin")
c2 = Client("Bao")

def update_messages():
    """
    updates the list of messages
    :return: None
    """
    msgs = []
    run = True
    while run:
        time.sleep(0.1)
        new_messages = c1.get_messages()  # get any new messages from client
        msgs.extend(new_messages)  # add to the list of messages

        for msg in new_messages:
            print(msg)

            if msg == "{quit}":
                run = False
                break


Thread(target=update_messages).start()

c1.send_message("Hello")
time.sleep(5)
c2.send_message("Hi")
time.sleep(5)

c1.disconnect()
time.sleep(2)
c2.disconnect()