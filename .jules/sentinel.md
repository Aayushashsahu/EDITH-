## 2026-05-18 - Command Injection in ADB shell
**Vulnerability:** Command injection on the host machine.
**Learning:** Calling `subprocess.run(f"adb -s {ADB_IP} {cmd}", shell=True)` allowed untrusted data in `cmd` to escape into the host's shell. It's a common pattern when calling adb commands dynamically.
**Prevention:** Remove `shell=True` and pass arguments as a list. For `adb shell` commands, pass the entire remote command string as a single cohesive argument after the 'shell' keyword (e.g., `['adb', 'shell', 'dumpsys | grep']`) to ensure pipes run on the android device instead of the host.
