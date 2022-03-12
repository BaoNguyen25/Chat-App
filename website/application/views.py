from flask import Flask, render_template, url_for, session, redirect, request, jsonify, flash, Blueprint
from client import Client
from .database import DataBase
import time

view = Blueprint("views", __name__)

NAME_KEY = "name"
MSG_LIMIT = 20


def disconnect():
    """
    disconnect client from server
    :return:
    """
    global client
    if client:
        client.disconnect()


@view.route("/login", methods=["POST", "GET"])
def login():
    """
    display login page and get the name of user
    :return: None
    """
    if request.method == "POST":
        name = request.form["inputName"]
        if len(name) >= 2:
            session[NAME_KEY] = name
            flash(f'You were successfully logged in as {name}.')
            return redirect(url_for("views.home"))
        else:
            flash('Name must be longer than 1 character')

    return render_template("login.html", **{"session": session})


@view.route("/logout")
def logout():
    """
    logging the user out by popping name from session
    :return: None
    """
    session.pop(NAME_KEY, None)
    flash("You were logged out.")
    return redirect(url_for("views.login"))


@view.route("/history")
def history():
    if NAME_KEY not in session:
        flash("Please login before viewing message history")
        return redirect(url_for("views.login"))

    json_messages = get_history(session[NAME_KEY])
    return render_template("history.html", **{"history": json_messages})



@view.route("/")
@view.route("/home")
def home():
    """
    Main home page where users can chat together
    :return: None
    """

    if NAME_KEY not in session:
        return redirect(url_for("views.login"))

    return render_template("index.html", **{"session": session})


@view.route("/get_name")
def get_name():
    """
    :return: convert a json object storing name of user into response object
    """
    data = {"name": ""}
    if NAME_KEY in session:
        data = {"name": session[NAME_KEY]}
    return jsonify(data)


@view.route("/get_messages")
def get_messages():
    """
    :return: all messages stored in database
    """
    db = DataBase()
    msgs = db.get_all_messages(MSG_LIMIT)
    messages = remove_seconds_from_messages(msgs)

    return jsonify(messages)


@view.route("/get_history")
def get_history(name):
    """
    return all messages by name of user
    :param name: str
    """
    db = DataBase()
    msgs = db.get_message_by_name(name)
    messages = remove_seconds_from_messages(msgs)

    return messages


def remove_seconds_from_messages(msgs):
    """
    remove the seconds from all messages
    :param msgs: list
    :return: list
    """
    messages = []
    for msg in msgs:
        message = msg
        message["time"] = remove_seconds(message["time"])
        messages.append(message)
    return messages


def remove_seconds(msg):
    """
    remove the seconds off of a date time string
    :param msg:
    :return:
    """
    return msg.split(".")[0][:-3]
