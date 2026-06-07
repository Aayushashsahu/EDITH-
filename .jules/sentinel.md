## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.

## 2026-06-07 - [Timing Attacks in API Key Validation]
**Vulnerability:** API keys were being verified using the standard equality operator (`==`) in both `backend/main.py` and `edith/backend/main.py`, making the system vulnerable to timing attacks.
**Learning:** Standard string comparisons stop at the first differing character, allowing an attacker to determine the correct API key character by character by measuring the response time.
**Prevention:** Use `secrets.compare_digest` for comparing sensitive strings like API keys, tokens, or passwords, as it performs a constant-time comparison. Ensure proper `None` checks before calling `compare_digest`.
