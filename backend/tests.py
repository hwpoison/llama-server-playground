import unittest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from instance_manager import InstanceManager
import subprocess
import yaml


class TestInstanceManager(unittest.TestCase):
    def setUp(self):
        self.config = None
        self.load_settings()
        self.manager = InstanceManager(self.config)

    def load_settings(self):
        with open('config.yml', 'r') as file:
            self.config = yaml.safe_load(file)

    def test_run_server(self):
        mock_process = MagicMock()
        mock_subprocess = MagicMock()
        mock_subprocess.return_value = mock_process
        with unittest.mock.patch('subprocess.Popen', mock_subprocess):
            process = self.manager.run_server('model_path', 8085)
            mock_subprocess.assert_called_once_with(
                ['server.exe', '--port', '8085', '--model',
                    'model/model_path', '--ctx-size', '1024', '--mlock'],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            self.assertEqual(process, mock_process)

    def test_recreate_existing_instance(self):
        instance_id = 'instance1'
        self.manager.running_instances = {
            instance_id: {
                'id': instance_id,
                'process': MagicMock(),
                'port': 8085,
                'model': 'model_path',
                'current_prompt': '',
                'last_seen': datetime.now().timestamp()
            }
        }
        self.manager.run_server = MagicMock()

        result = self.manager.recreate(instance_id)

        self.assertTrue(result)
        self.manager.run_server.assert_called_once_with('model_path', 8085)

    def test_recreate_non_existing_instance(self):
        instance_id = 'instance1'
        self.manager.running_instances = {}
        self.manager.run_server = MagicMock()

        result = self.manager.recreate(instance_id)

        self.assertFalse(result)
        self.manager.run_server.assert_not_called()


if __name__ == '__main__':
    unittest.main()
