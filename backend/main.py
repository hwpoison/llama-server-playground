from flask import Flask, request, jsonify, Response
from instance_manager import InstanceManager
from datetime import datetime
from logger import log
import threading
import requests
import atexit
import json
import yaml
import time

app = Flask(__name__)
instances = None

with open('config.yml', 'r') as file:
    server_config = yaml.safe_load(file)


@app.before_first_request
def initialize():
    global instances
    log.info("Initializing Instance manager.")
    instances = InstanceManager(server_config)
    threading.Thread(target=instances.auto_purge).start()
    atexit.register(instances.kill_all)


@app.route('/serverinfo')
def info():
    return jsonify({'running_instances': instances.get_all_running(),
                    'server_config': server_config})


@app.route('/imhere/<instance_id>')
def ping(instance_id):
    if instance := instances.running_instances.get(instance_id):
        instance['last_seen'] = datetime.now().timestamp()

    return jsonify({'ping': 'ok'}), 200


@app.route('/<endpoint>', methods=['GET', 'POST'])
def proxy(endpoint):
    incoming = json.loads(request.data)
    if (instance_id := incoming.get("sessionID")):
        process = instances.running_instances.get(instance_id)
        if not process:
            instances.create(instance_id, server_config["default_model"])
            process = instances.running_instances[instance_id]
            time.sleep(3)
            # return jsonify({"error": "This instance doest not exists or is not more available"})

    url = f'{server_config["server"]["ip"]}:{ process["port"] }/{endpoint}'

    if request.method == 'GET':
        try:
            response = requests.get(url)
            return response.content, response.status_code
        except requests.RequestException as e:
            status_code = getattr(e.response, 'status_code', 500)
            return jsonify({"error": str(e)}), status_code

    if request.method == 'POST':
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        try:
            response = requests.post(
                url, data=request.data, headers=headers, stream=True)
        except requests.RequestException as e:
            status_code = getattr(e.response, 'status_code', 500)
            print(url, status_code, str(e))
            return jsonify({"error": str(e)}), status_code

        return Response(response.iter_content(chunk_size=2048), content_type=response.headers['content-type'])

    return jsonify({"error": "problem solving the request"}), 500
