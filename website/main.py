from flask import session
from flask_socketio import SocketIO
import time
from application import create_app
from application.database import DataBase
import config

# setup flask application

app = create_app()
socketio = SocketIO(app)  # user communication

# User communication functions


@socketio.on('event')
def handle_my_custom_event(json, methods=['POST', 'GET']):
    """
    saving messages from web server and sending to other clients
    :param json: json
    :param methods: POST GET
    :return: None
    """
    data = dict(json)
    if "name" in data:
        db = DataBase()
        db.save_message(data["name"], data["message"])

    socketio.emit('message response', json)


if __name__ == "__main__": # start the web server
    socketio.run(app, debug=True, host=str(config.Config.SERVER))