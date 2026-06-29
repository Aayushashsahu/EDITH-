import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Adjust path to import adb_phone
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import edith.backend.integrations.adb_phone as adb_phone

class TestADBPhoneSecurity(unittest.TestCase):
    def setUp(self):
        # Enable ADB for testing
        adb_phone.ADB_ENABLED = True
        adb_phone.ADB_IP = "192.168.1.1:5555"

    @patch('subprocess.run')
    def test_adb_shell_command(self, mock_run):
        # Setup mock return value
        mock_run.return_value = MagicMock(stdout="ringing\n", stderr="")

        # Call with a shell command
        cmd = "shell dumpsys telephony.registry | grep mCallState"
        res = adb_phone._adb(cmd)

        # Verify shell=True is NOT passed (it's False by default)
        # Verify the arguments are a list
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args

        # args[0] should be a list
        self.assertIsInstance(args[0], list)
        self.assertEqual(args[0], ["adb", "-s", "192.168.1.1:5555", "shell", "dumpsys telephony.registry | grep mCallState"])
        self.assertNotIn('shell', kwargs)

    @patch('subprocess.run')
    def test_adb_non_shell_command(self, mock_run):
        mock_run.return_value = MagicMock(stdout="", stderr="")

        # Call with a non-shell command
        cmd = "devices -l"
        res = adb_phone._adb(cmd)

        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args

        self.assertIsInstance(args[0], list)
        self.assertEqual(args[0], ["adb", "-s", "192.168.1.1:5555", "devices", "-l"])
        self.assertNotIn('shell', kwargs)

    @patch('subprocess.run')
    def test_phone_control_connect(self, mock_run):
        mock_run.return_value = MagicMock(stdout="connected\n", stderr="")

        phone = adb_phone.PhoneControl()
        phone.connect()

        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args

        self.assertIsInstance(args[0], list)
        self.assertEqual(args[0], ["adb", "connect", "192.168.1.1:5555"])
        self.assertNotIn('shell', kwargs)

    @patch('subprocess.run')
    def test_sms_command_injection_prevented(self, mock_run):
        mock_run.return_value = MagicMock(stdout="", stderr="")

        phone = adb_phone.PhoneControl()

        # Suppose a malicious message is sent
        message = "hello'; delete_things /; echo '"
        phone.sms("1234567890", message)

        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args

        self.assertIsInstance(args[0], list)
        self.assertEqual(args[0][0], "adb")
        self.assertEqual(args[0][3], "shell")

        # The entire rest of the command is passed as a SINGLE argument to `adb shell`.
        # This prevents host command injection, although device shell injection might still
        # be possible since `adb shell` passes it to the Android shell. However, the host
        # machine running the script is protected because `subprocess.run` receives a list
        # and doesn't invoke the host shell.
        expected_cmd = "am start -a android.intent.action.SENDTO -d sms:1234567890 --es sms_body 'hello\\'; delete_things /; echo \\'' --ez exit_on_sent true"
        self.assertEqual(args[0][4], expected_cmd)
        self.assertNotIn('shell', kwargs)

if __name__ == '__main__':
    unittest.main()
