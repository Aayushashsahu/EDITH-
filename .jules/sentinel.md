## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.

## 2024-05-28 - [Command Injection via ADB phone integration]
**Vulnerability:** Command injection vulnerability in `backend/integrations/adb_phone.py` when executing `subprocess.run` with `shell=True`, as untrusted commands or SMS payloads are passed through directly.
**Learning:** `shell=True` exposes the host machine to command injection (e.g. `'; malicious_command'`) from inputs even if they seem constrained, especially via SMS content.
**Prevention:** Avoid `shell=True`. Always construct arguments as a list. When calling ADB shell, use a single cohesive string for the internal shell command (e.g., `["adb", "shell", "long command | pipe"]`), which safely prevents host-side injection while passing the intended payload to the device.
