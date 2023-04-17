from flask import Flask
from flask_socketio import SocketIO

app = Flask ( __name__ )
socketio = SocketIO ( app )


@socketio.on ( 'message' )
def handle_message(message):
    print ( f'received message: {message}' )


if __name__ == '__main__':
    socketio.run ( app )
