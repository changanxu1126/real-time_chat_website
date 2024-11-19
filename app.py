from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import os

app = Flask(__name__)
socketio = SocketIO(app)

MESSAGE_FILE = '1.txt'

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    if os.path.exists(MESSAGE_FILE):
        with open(MESSAGE_FILE, 'r') as f:
            messages = f.readlines()
        emit('load_messages', [msg.strip() for msg in messages])

@socketio.on('message')
def handle_message(msg):
    with open(MESSAGE_FILE, 'a') as f:
        f.write(msg + '\n')
    emit('message', msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app,allow_unsafe_werkzeug=True)

