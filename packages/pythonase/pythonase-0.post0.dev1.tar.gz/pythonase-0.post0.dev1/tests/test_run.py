import unittest
from pythonase.run import run_command


class RunTestCase(unittest.TestCase):
    def test_run_command_ok(self):
        cmd = "echo abc"
        std, _, rc = run_command(cmd)
        self.assertEqual(rc, 0)
        self.assertEqual(std.strip(), "abc")

    def test_run_command_wrong(self):
        cmd = "not_available_command abc"
        _, err, rc = run_command(cmd)
        self.assertNotEqual(rc, 0)
        self.assertTrue(err.find("not found") != -1)


if __name__ == '__main__':
    unittest.main()
