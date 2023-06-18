from flask import Flask, request, jsonify, Response
from instance_manager import InstanceManager
from datetime import datetime
import requests
import json
import atexit
import threading
from logger import log


server_config = {
    'server_exec': 'server.exe',
    'default_ip': 'http://127.0.0.1',
    'models': {
        'openllama3b': 'model/open-llama-3b-q4_0.bin',
    },
    'default_model': 'openllama3b',
    'max_ctx': 1024,
}

app = Flask(__name__)
instances = None


@app.before_first_request
def initialize():
    global instances
    log.info("Initializing instances...")
    instances = InstanceManager(server_config)
    threading.Thread(target=instances.auto_purge).start()

    atexit.register(instances.kill_all)


@app.route('/serverinfo')
def info():
    return jsonify({'availables_instances': instances.get_all_running(), 'server_config': server_config})


@app.route('/imhere/<instance_id>')
def ping(instance_id):
    instance = instances.running_instances.get(instance_id)
    if instance:
        instance['last_seen'] = datetime.now().timestamp()

    return jsonify({'ping': 'ok'}), 200


@app.route('/<instance_id>/<endpoint>', methods=['GET', 'POST'])
def proxy(instance_id, endpoint):
    process = instances.running_instances.get(instance_id)
    if not process:
        instances.create(instance_id, server_config["default_model"])
        process = instances.running_instances[instance_id]

    url = f'{server_config["default_ip"]}:{ process["port"] }/{endpoint}'
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

    if request.method == 'GET':
        try:
            response = requests.get(url)
            res_data = json.loads(response.content)
            return response.content, response.status_code
        except:
            return jsonify({"error": "problem"}), 500

    if request.method == 'POST':
        req_data = json.loads(request.data)
        response = requests.post(
            url, data=request.data, headers=headers, stream=True)

        # Stream resonse
        def generate():
            for chunk in response.iter_content(chunk_size=2048):
                yield chunk

        if response.status_code != 200:
            instances.recreate(instance_id)

        return Response(generate(), content_type=response.headers['content-type'])
