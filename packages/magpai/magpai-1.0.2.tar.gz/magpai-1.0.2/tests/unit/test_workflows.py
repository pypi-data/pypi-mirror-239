from magpai.workflows import RunWorkflow
from tests import *
from tests.helpers import *
import os

class TestVersion(unittest.TestCase):

    def test_workflow_run(self):
        job = RunWorkflow(os.environ["MAGPAI_API"], "yJXfa30diyekbQZdvmRQ", {"Name": "Elmo"})
        print(job)
        for output in job['outputs']:
            if output['name'] == 'out_1':
                self.assertEqual(output['value'], "My name is Elmo")
            if output['name'] == 'out_2':
                self.assertEqual(output['value'], "42")
            if output['name'] == 'out_3':
                self.assertEqual(output['value'], "#FE3E3EFF")
