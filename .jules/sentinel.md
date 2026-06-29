## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.
## 2026-06-29 - Prevent Command Injection via subprocess shell=True in ADB Phone Control
**Vulnerability:** Command Injection on host system due to `subprocess.run(..., shell=True)` combined with dynamically constructed strings.
**Learning:** Using `shell=True` with external binaries like `adb` exposes the host system to shell command injection if the dynamic parts (like config IPs or message strings) are compromised or maliciously manipulated. Piping operations (`| grep`) used in ADB shell commands should be passed as a single cohesive argument to the remote shell instead of being interpreted by the host shell.
**Prevention:** Avoid `shell=True` entirely. Pass the remote command containing pipes as a single cohesive string after the `shell` argument to `adb` (e.g., `["adb", "-s", IP, "shell", "dumpsys ... | grep ..."]`), and use `shlex.split()` for other standard ADB arguments.
