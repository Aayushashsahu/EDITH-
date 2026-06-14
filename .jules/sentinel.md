## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.

## 2024-06-14 - [Timing Attack via API Key Comparison]
**Vulnerability:** API key verification in the FastAPI backend (`backend/main.py` and `edith/backend/main.py`) used standard string equality operators (`==` and `!=`). This is vulnerable to timing attacks, as the standard comparison operation returns early upon the first mismatched character, allowing an attacker to deduce the key character by character by measuring response times.
**Learning:** Security-sensitive string comparisons like API keys, passwords, or tokens should always use constant-time comparisons.
**Prevention:** Use `secrets.compare_digest` from the Python standard library `secrets` module for all sensitive token comparisons. Ensure that `None` values (like missing headers or query parameters) are handled properly before comparison, as `secrets.compare_digest(None, 'string')` raises a `TypeError`.
