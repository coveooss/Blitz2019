import os
import subprocess
import unittest
import uuid
import xmlrunner
from pathlib import Path

from framework.framework import main
from . import SCENARIO_ROOT, get_open_port


class TestChallengeFrameworkTests(unittest.TestCase):
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

    def test_output_score(self):
        score = main(self.challenge_name,
                     self.replayfile,
                     self.resultfile,
                     self.service_url,
                     'yoloswagteamyo',
                     3, 1, 3)
        self.assertGreaterEqual(score, 2)  # Perfect score would be 3


class TestWrongChallengeFrameworkTests(unittest.TestCase):
    def setUp(self):
        self.port = get_open_port()
        self.service_url = f'http://localhost:{self.port}'
        self.wrongest_pong_process = subprocess.Popen(
            [f'python3 {SCENARIO_ROOT}wrongest_pong.py {self.port}'], shell=True)
        self.challenge_name = 'pingpong'
        self.replayfile = f'replay_{uuid.uuid4()}'
        self.resultfile = f'result_{uuid.uuid4()}'

    def tearDown(self):
        self.wrongest_pong_process.kill()
        self.wrongest_pong_process.wait()
        if Path(self.replayfile).exists():
            os.remove(self.replayfile)
        if Path(self.resultfile).exists():
            os.remove(self.resultfile)

    def test_output_score_should_not_count_wrong_answers(self):
        score = main(self.challenge_name,
                     self.replayfile,
                     self.resultfile,
                     self.service_url,
                     'yoloswagteamyo',
                     3, 1, 3)
        self.assertEqual(score, 0)  # :sowrong:


class TestAverageChallengeFrameworkTests(unittest.TestCase):
    def setUp(self):
        self.port = get_open_port()
        self.service_url = f'http://localhost:{self.port}'
        self.flipping_pong_process = subprocess.Popen(
            [f'python3 {SCENARIO_ROOT}flipping_pong.py {self.port}'], shell=True)
        self.challenge_name = 'pingpong'
        self.replayfile = f'replay_{uuid.uuid4()}'
        self.resultfile = f'result_{uuid.uuid4()}'

    def tearDown(self):
        self.flipping_pong_process.kill()
        self.flipping_pong_process.wait()
        if Path(self.replayfile).exists():
            os.remove(self.replayfile)
        if Path(self.resultfile).exists():
            os.remove(self.resultfile)

    def test_output_score_should_not_count_wrong_answers(self):
        score = main(self.challenge_name,
                     self.replayfile,
                     self.resultfile,
                     self.service_url,
                     'yoloswagteamyo',
                     10, 1, 10, 1)
        self.assertGreaterEqual(score, 4.5)
        self.assertLessEqual(score, 6.5)


if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False, buffer=False, catchbreak=False)
