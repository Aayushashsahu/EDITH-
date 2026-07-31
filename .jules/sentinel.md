## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.

## 2025-02-12 - Prevent Host Command Injection in Remote Execution with Pipes
**Vulnerability:** The ADB integration used `shell=True` to execute `adb` commands to allow piping logic on the Android device (e.g., `dumpsys | grep`), which introduced a critical command injection vulnerability on the host machine.
**Learning:** We need to support shell-like pipelines on remote systems while keeping execution completely secure and avoiding injection attacks on the host. Standard `shlex.split` cannot parse pipeline operators correctly without stripping them or breaking execution locally.
**Prevention:** Remove `shell=True` completely. For executing complex commands with pipes on remote environments like `adb shell`, construct the arguments list by prefixing the remote command string as a single, cohesive argument to `shell` (e.g., `["adb", "-s", IP, "shell", "dumpsys | grep"]`). This avoids host shell parsing while correctly passing the piped command strictly to the remote shell.
## 2026-07-28 - [Timing Attack Risk in API Key Verification]
**Vulnerability:** Standard equality operators (== and !=) were used to verify API keys in HTTP and WebSocket endpoints, making them susceptible to timing attacks.
**Learning:** Using == to compare secrets leaks information about the secret's length and content, as it short-circuits upon the first mismatch.
**Prevention:** Always use secrets.compare_digest (and ensure both inputs are strings, not None) when comparing secrets like API keys, tokens, or passwords.

## 2024-05-24 - [Prevent Attribute-Based XSS in innerHTML Templates]
**Vulnerability:** The custom `esc()` function used for escaping text before injecting it via `innerHTML` only escaped HTML tags (`<`, `>`, `&`), failing to escape quotes (`"`, `'`). This allowed attribute-based XSS when user input was embedded within HTML attributes using template literals.
**Learning:** Escaping only tags is insufficient when rendering dynamic HTML. If an attacker inputs a string with a quote followed by a payload (e.g., `" onmouseover="alert(1)`), it can break out of an attribute and execute arbitrary JavaScript.
**Prevention:** Ensure any escaping utility also handles double quotes (`"`) and single quotes (`'`), converting them to their HTML entity equivalents (`&quot;`, `&#39;`) before insertion into the DOM.
