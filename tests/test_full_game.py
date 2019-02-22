import json
import unittest
import subprocess

import os
import uuid

import xmlrunner

SCENARIO_ROOT = 'scenario/'
TEST_ROOT = "tests/"
OUTPUT_DIR='testout/'
REPLAY_FILENAME_ROOT = "test_output_"


class TestGame(unittest.TestCase):
    def setUp(self):
        self.replay_file_name =  TEST_ROOT + OUTPUT_DIR + REPLAY_FILENAME_ROOT + str(uuid.uuid4()) + ".json"

    def tearDown(self):
        os.remove(self.replay_file_name)

    def test_dumb_scenario(self):
        with open(TEST_ROOT + SCENARIO_ROOT + 'dumb1') as scenario:
            subprocess.run(
                ['python3', '__main__.py', '--no-gui', '-w', "." + "/"+ self.replay_file_name],
                cwd='.',
                stdin=scenario,
                stdout=subprocess.DEVNULL)

        with open(self.replay_file_name, "r") as file:
            replay = json.load(file)
            self.assertEqual(replay['winner'], 1)


if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False, buffer=False, catchbreak=False)
