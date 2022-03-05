from flask import Flask, render_template, url_for, session, redirect, request, jsonify
from client import Client
from threading import Thread
import time

NAME_KEY = "name"
messages = []

client = None
app = Flask(__name__, template_folder='templates')
app.secret_key = "hellomynameisbaonguyen"


def disconnect():
    """
    disconnect client from server
    :return:
    """
    global client
    if client:
        client.disconnect()


@app.route("/login", methods=["POST", "GET"])
def login():
    """
    display login page and get the name of user
    :return: None
    """
    if request.method == "POST":
        session[NAME_KEY] = request.form["inputName"]
        return redirect(url_for("home"))
    else:
        return render_template("login.html", **{"session": session})


@app.route("/logout")
def logout():
    """
    logging the user out by popping name from session
    :return: None
    """
    session.pop(NAME_KEY, None)
    return redirect(url_for("login"))


@app.route("/")
@app.route("/home")
def home():
    """
    Main home page where users can chat together
    :return: None
    """
    global client

    if NAME_KEY not in session:
        return redirect(url_for("login"))

    client = Client(session[NAME_KEY])

    return render_template("index.html", **{"login": True, "session": session})


@app.route("/send_messages")
def send_messages():
    """
    called from JQuery to send messages
    :return: None
    """
    global client

    msg = request.args.get("txt")
    print(msg)
    if client:
        client.send_message(msg)

    return "none"


@app.route("/get_messages")
def get_messages():
    return jsonify({"messages": messages})


def update_messages():
    """
    updates the list of messages
    :return: None
    """

    global messages

    run = True
    while run:
        time.sleep(0.1)
        if not client: continue
        new_messages = client.get_messages()  # get any new messages from client
        messages.extend(new_messages)  # add to the list of messages

        for msg in new_messages:
            if msg == "{quit}":
                run = False
                break


if __name__ == "__main__":
    Thread(target=update_messages).start()
    app.run(debug=True)
