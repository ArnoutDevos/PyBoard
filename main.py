#! /usr/bin/python
# -*- encoding: utf-8 -*-

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import time

class MyServer(Flask):

    def __init__(self, *args, **kwargs):
            super(MyServer, self).__init__(*args, **kwargs)

            #instanciate your variables here
            self.newest_data = {}

app = MyServer(__name__, template_folder='templates', static_url_path='/static/', static_folder='static')
app.config['SECRET_KEY'] = 'ines'
socketio = SocketIO(app)

app.newest_data = {'values':[], 'labels':[]}

@app.route('/')
def index():
	return render_template('./index.html', newest_content=app.newest_data)

@app.route('/chart')
def chart():
	return render_template('./chart.html')

@socketio.on('connected')
def conn(msg):
	return {'data':'Ok'}

@socketio.on('client_message')
def receive_message(data):
	print('Sending data: ', data)
	emit('server_message', data, broadcast=True)

@app.route('/send', methods=['POST'])
def some_function():
	#data.append(float(request.form['number']))
	content = request.json

	app.newest_data = content

	print('POST data: ', content['values'])
	print('##############################')
	msg = {'nickname': 'Guest', 'message': content}
	print('Sending data from server: ', msg)
	emit('server_message', msg, broadcast=True, namespace='/')
	return str(msg)

if __name__ == '__main__':
	socketio.run(app, debug=True)