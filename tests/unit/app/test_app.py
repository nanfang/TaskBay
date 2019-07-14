import unittest
from taskbay.app.base import TaskBay


class TestTaskBayApp(unittest.TestCase):

    def test_app_config(self):
        """hello world"""
        app = TaskBay(config_source='tests.unit.app.taskbay_config')
        self.assertEqual(app.task_cls, 'taskbay.task.base:_Task')



if __name__ == '__main__':
    unittest.main()