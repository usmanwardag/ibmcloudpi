from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify, redirect
import atexit
import os
import json
import wiotp.sdk.application

app = Flask(__name__, static_url_path='')

options = wiotp.sdk.application.parseConfigFile("application.yaml")
client = wiotp.sdk.application.ApplicationClient(config=options)
client.connect()

port = int(os.getenv('PORT', 8000))

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/light/<command>', methods=['GET', 'POST'])
def light_route(command):
    print(command)
    eventData = {'command' : command}
    client.publishEvent(typeId="RaspberryPi", deviceId="1", eventId="light", msgFormat="json", data=eventData)
    return redirect("/", code=302)

@atexit.register
def shutdown():
    if client:
        client.disconnect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
