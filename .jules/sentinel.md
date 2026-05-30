## 2026-05-19 - Command Injection in ADB Integration
**Vulnerability:** Use of `shell=True` with `subprocess.run` when executing adb commands in `adb_phone.py`, which is susceptible to host command injection.
**Learning:** Replacing `shell=True` for ADB commands requires passing the remote shell script as a single argument after `shell` to maintain pipeline functionality on the Android device without evaluating it on the host.
**Prevention:** Avoid `shell=True` and use a list of arguments, parsing the command into distinct parts using string operations or `shlex.split`.
