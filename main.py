import socket
from GLM import glm
from random import randint
from multiprocessing import Process
from flask import Flask, render_template

app = Flask(__name__)

glm.PLUGIN_PACKAGE = "GLM.source.plugins"
PLUGIN_DIRECTORY = "./GLM/source/" + glm.PLUGIN_PREFIX + "/"
plugin_loader = None

server_addr = 'localhost'
server_port = 9998

@app.route('/')
def index():
    plugins = list(map(
        lambda x: x.replace('_', ' ').replace('.py', ''),
        glm.plugin_scan(PLUGIN_DIRECTORY)
    ))
    return render_template('main.html', plugins=enumerate(plugins))


@app.route('/plugin/<int:id>')
def select_plugin(id):
    global plugin_loader
    print(id)
    if plugin_loader is not None:
        plugin_loader.terminate()
    plugin_loader = Process(target=glm.plugin_loader, args=(glm.plugin_scan(PLUGIN_DIRECTORY)[int(id)],))
    plugin_loader.start()
    return ''

@app.route('/plugin/<int:id>/webview')
def webview(id):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_addr, server_port))

    # Web client response
    response = "web_client;" + "req_view"
    client.send(response.encode())

    response = client.recv(512)
    client.close()
    return render_template('webview.html', data=response.decode())

@app.route('/plugin/<int:id>/<str:event>')
def event(id, event):
    # Need to open a event client on each plugins
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_addr, server_port))

    response = "web_client" + event
    client.send(response.encode())

    response = client.recv(512) # Drop response
    client.close()

    return None
