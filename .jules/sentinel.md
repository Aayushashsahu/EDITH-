## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.

## 2024-05-18 - Fix API Key Timing Attacks in FastAPI endpoints
**Vulnerability:** Timing attack vulnerability in API key verification. The application was using the standard equality operator (`==` and `!=`) to compare incoming API keys against the expected key in both HTTP endpoints and WebSocket connections.
**Learning:** Standard string comparison operators exit early as soon as a mismatch is found. This leaks information about the length and content of the expected string through the time taken to respond, which could theoretically allow an attacker to guess the API key character by character.
**Prevention:** Always use a constant-time comparison function, such as `secrets.compare_digest` in Python, for verifying security tokens, API keys, passwords, or hashes. Additionally, ensure that inputs are not `None` before passing them to `compare_digest`, as it will raise a `TypeError`.
