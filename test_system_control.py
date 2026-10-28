import unittest
import sys
from unittest.mock import patch, MagicMock

# Mock psutil before importing
sys.modules['psutil'] = MagicMock()

import edith.backend.tools.system_control as sc

class TestSystemControl(unittest.TestCase):
    def setUp(self):
        self.control = sc.SystemControl()

    @patch('edith.backend.tools.system_control.datetime')
    def test_get_time(self, mock_datetime):
        mock_now = MagicMock()
        mock_now.strftime.return_value = "It is 03:15 PM on Monday, 01 January 2024."
        mock_datetime.datetime.now.return_value = mock_now

        res = self.control.get_time()

        self.assertEqual(res, "It is 03:15 PM on Monday, 01 January 2024.")
        mock_datetime.datetime.now.assert_called_once()
        mock_now.strftime.assert_called_once_with("It is %I:%M %p on %A, %d %B %Y.")

    @patch('edith.backend.tools.system_control._ps')
    def test_open_url_valid_http(self, mock_ps):
        res = self.control.open_url("http://example.com")
        self.assertEqual(res, "Opened http://example.com.")
        mock_ps.assert_called_once_with("Start-Process 'http://example.com'")

    @patch('edith.backend.tools.system_control._ps')
    def test_open_url_valid_https(self, mock_ps):
        res = self.control.open_url("https://example.com")
        self.assertEqual(res, "Opened https://example.com.")
        mock_ps.assert_called_once_with("Start-Process 'https://example.com'")

    @patch('edith.backend.tools.system_control._ps')
    def test_open_url_missing_scheme(self, mock_ps):
        res = self.control.open_url("example.com")
        self.assertEqual(res, "Opened https://example.com.")
        mock_ps.assert_called_once_with("Start-Process 'https://example.com'")

    @patch('edith.backend.tools.system_control._ps')
    def test_open_url_injection_attempt(self, mock_ps):
        # Single quotes should be escaped
        url_with_injection = "example.com&calc.exe'test"
        res = self.control.open_url(url_with_injection)
        self.assertEqual(res, "Opened https://example.com&calc.exe'test.")
        mock_ps.assert_called_once_with("Start-Process 'https://example.com&calc.exe''test'")

    @patch('edith.backend.tools.system_control._ps')
    def test_open_url_invalid_scheme(self, mock_ps):
        res1 = self.control.open_url("file:///C:/Windows/System32/cmd.exe")
        self.assertTrue(res1.startswith("Opened https://file:///"))

        res2 = self.control.open_url("javascript:alert(1)")
        self.assertTrue(res2.startswith("Opened https://javascript:alert(1)"))

if __name__ == '__main__':
    unittest.main()
