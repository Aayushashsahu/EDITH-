import unittest
import sys
from unittest.mock import patch, MagicMock

# Mock psutil before importing
sys.modules['psutil'] = MagicMock()

import backend.tools.system_control as sc

class TestSystemControl(unittest.TestCase):
    def setUp(self):
        self.control = sc.SystemControl()

    @patch('backend.tools.system_control._ps')
    def test_open_url_valid_http(self, mock_ps):
        res = self.control.open_url("http://example.com")
        self.assertEqual(res, "Opened http://example.com.")
        mock_ps.assert_called_once_with("Start-Process 'http://example.com'")

    @patch('backend.tools.system_control._ps')
    def test_open_url_valid_https(self, mock_ps):
        res = self.control.open_url("https://example.com")
        self.assertEqual(res, "Opened https://example.com.")
        mock_ps.assert_called_once_with("Start-Process 'https://example.com'")

    @patch('backend.tools.system_control._ps')
    def test_open_url_missing_scheme(self, mock_ps):
        res = self.control.open_url("example.com")
        self.assertEqual(res, "Opened https://example.com.")
        mock_ps.assert_called_once_with("Start-Process 'https://example.com'")

    @patch('backend.tools.system_control._ps')
    def test_open_url_injection_attempt(self, mock_ps):
        # Single quotes should be escaped
        url_with_injection = "example.com&calc.exe'test"
        res = self.control.open_url(url_with_injection)
        self.assertEqual(res, "Opened https://example.com&calc.exe'test.")
        mock_ps.assert_called_once_with("Start-Process 'https://example.com&calc.exe''test'")

    @patch('backend.tools.system_control._ps')
    def test_open_url_invalid_scheme(self, mock_ps):
        res1 = self.control.open_url("file:///C:/Windows/System32/cmd.exe")
        self.assertTrue(res1.startswith("Opened https://file:///"))

        res2 = self.control.open_url("javascript:alert(1)")
        self.assertTrue(res2.startswith("Opened https://javascript:alert(1)"))

    @patch('backend.tools.system_control._cmd')
    def test_open_app_known(self, mock_cmd):
        res = self.control.open_app("chrome")
        self.assertEqual(res, "Opening chrome.")
        mock_cmd.assert_called_once_with("start chrome")

    @patch('backend.tools.system_control._ps')
    def test_open_app_unknown_injection_attempt(self, mock_ps):
        res = self.control.open_app("calc.exe&echo 'hacked'")
        self.assertEqual(res, "Opening calc.exe&echo 'hacked'.")
        mock_ps.assert_called_once_with("Start-Process 'calc.exe&echo ''hacked'''")

    @patch('backend.tools.system_control._ps')
    def test_close_app_injection_attempt(self, mock_ps):
        mock_ps.return_value = "SUCCESS"
        res = self.control.close_app("calc.exe&echo 'hacked'")
        self.assertEqual(res, "Closed calc.exe&echo 'hacked'.")
        mock_ps.assert_called_once_with("taskkill /F /IM 'calc.exe&echo ''hacked''.exe' 2>&1")

if __name__ == '__main__':
    unittest.main()
