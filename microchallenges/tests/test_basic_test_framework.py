import os
import subprocess
import unittest
import uuid
import xmlrunner
from pathlib import Path

from framework.framework import main
from . import SCENARIO_ROOT, get_open_port


class TestBasicTestFrameworkTests(unittest.TestCase):
    def setUp(self):
        self.port = get_open_port()
        self.service_url = f'http://localhost:{self.port}'
        self.perfect_pong_process = subprocess.Popen(
            [f'python3 {SCENARIO_ROOT}perfect_pong.py {self.port}'], shell=True)
        self.challenge_name = 'pingpong'
        self.replayfile = f'replay_{uuid.uuid4()}'
        self.resultfile = f'result_{uuid.uuid4()}'

    def tearDown(self):
        self.perfect_pong_process.kill()
        self.perfect_pong_process.wait()
        if Path(self.replayfile).exists():
            os.remove(self.replayfile)
        if Path(self.resultfile).exists():
            os.remove(self.resultfile)

    def test_does_not_crash(self):
        main(self.challenge_name,
             self.replayfile,
             self.resultfile,
             self.service_url,
             'yoloswagteamyo',
             1, 1, 1)

    def test_does_produce_replay(self):
        main(self.challenge_name,
             self.replayfile,
             self.resultfile,
             self.service_url,
             'yoloswagteamyo',
             1, 1, 1)
        self.assertTrue(Path(self.replayfile).exists())

    def test_does_produce_score_file(self):
        main(self.challenge_name,
             self.replayfile,
             self.resultfile,
             self.service_url,
             'yoloswagteamyo',
             1, 1, 1)
        self.assertTrue(Path(self.resultfile).exists())


if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False, buffer=False, catchbreak=False)
