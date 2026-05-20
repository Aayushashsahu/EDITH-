## 2024-05-18 - PowerShell bridge command injection
**Vulnerability:** Command injection via unescaped string interpolation when passing user arguments to the PowerShell bridge script (`_ps()`). This was found in the `SystemControl.hotkey` and `SystemControl.notify` methods in `backend/tools/system_control.py`.
**Learning:** Even if `subprocess.run` receives a list of strings, executing powershell scripts built with string interpolation allows attackers to break out using single quotes (`'`) and execute arbitrary PowerShell scripts, because the `script` parameter itself acts as an eval.
**Prevention:** Always escape single quotes (`.replace("'", "''")`) for any untrusted user input that gets interpolated into a single-quoted string block passed to PowerShell.
