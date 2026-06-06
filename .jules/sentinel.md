## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.

## 2025-02-14 - Fix Timing Attack Vulnerability in API Key Validation
**Vulnerability:** The application used simple string equality (`==` and `!=`) to verify API keys in REST API headers and WebSocket query parameters.
**Learning:** Standard string comparison operators return `False` as soon as a character mismatch is found. An attacker can exploit this early exit by measuring the time it takes for the server to reject incorrect keys, allowing them to guess the correct API key character by character (a timing attack).
**Prevention:** Always use constant-time comparison functions like `secrets.compare_digest` when verifying sensitive strings such as API keys, tokens, or passwords. Additionally, always guard against `None` values (e.g., missing headers or query params), as `secrets.compare_digest(None, 'string')` throws a `TypeError`.
