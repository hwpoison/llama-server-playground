import subprocess
import time
from logger import log
from datetime import datetime


class InstanceManager:
    def __init__(self, config: dict):
        self.config = config
        self.base_port = 8084
        self.running_instances = {}
    def run_server(self, model_path: str, port: int):
        server_executable = self.config['server_exec']
        args = ['--port', str(port), '--model', model_path,
                '--ctx-size', str(self.config['max_ctx'])]
                
        process = subprocess.Popen(
            [server_executable] + args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        log.info(
            f"Instance of model '{model_path}' created on PORT({port}) with PID({process.pid}).")
        return process

    def recreate(self, instance_id: str) -> bool:
        if self.running_instances.get(instance_id):
            instance = self.running_instances[instance_id]
            instance['process'].kill()
            instance['process'] = self.run_server(
                instance['model'], instance['port'])
            log.info(
                f"[+] Instance recreated: :{instance['port']} PID:{instance['process'].pid}.")
            return True
        log.error(
            f"[x] Failed to recreate the instance {instance_id} does not exists!")
        return False

    def kill(self, instance_id: str):
        log.info("Killing instance ", instance_id)
        if self.running_instances.get(instance_id):
            instance = self.running_instances[instance_id]
            instance['process'].kill()
            del self.running_instances[instance_id]
            log.info(
                f"[+] Instance killed: :{instance['port']} PID:{instance['process'].pid}.")
            return True
        log.error(
            f"[x] Failed to kill the instance {instance_id} does not exists!")
        return False

    def kill_all(self):
        for instance_id in self.running_instances.keys():
            self.kill(instance_id)

    def create(self, instance_id: str, model_name: str):
        choiced_model = self.config['models'][model_name]
        self.base_port += 1
        process = self.run_server(choiced_model, self.base_port)

        self.running_instances[instance_id] = {
            'id': instance_id,
            'process': process,
            'port': self.base_port,
            'model': choiced_model,
            'current_prompt': '',
            'last_seen': datetime.now().timestamp()
        }

    def get_all_running(self):
        active_processes = []
        for process in self.running_instances.values():
            if not process['process'].poll():  # if still running
                active_processes.append({
                    process['id']: {
                        'pid': process['process'].pid,
                        'port': process['port'],
                        'last_seen': process['last_seen']
                    }
                })
        return active_processes

    def auto_purge(self):
        # Check every 10 secs and purge un used instances
        now = datetime.now().timestamp()
        for instance_id in list(self.running_instances):
            instance = self.running_instances[instance_id]
            if (now - instance['last_seen']) > 10:
                self.kill(instance['id'])
        time.sleep(10)
        self.auto_purge()
