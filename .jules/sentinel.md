## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.

## 2024-05-18 - [API Key Timing Attack]
**Vulnerability:** API key validation was using standard string equality (`==` and `!=`), which stops comparison at the first mismatched character, enabling timing attacks to guess the key.
**Learning:** In FastAPI routes and WebSockets, standard string comparison for secrets is insecure. `secrets.compare_digest` must be used to perform constant-time comparison, but it requires both operands to be strings.
**Prevention:** Always use `secrets.compare_digest` for validating authentication tokens, API keys, or passwords. Ensure explicit `None` checks are in place before calling `compare_digest` to prevent `TypeError`.
