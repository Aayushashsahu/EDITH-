## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.

## 2024-06-03 - Timing attack vulnerability in API Key verification
**Vulnerability:** Fast fail string comparisons (`==` or `!=`) were used for validating `API_KEY` headers and query params across authentication endpoints.
**Learning:** Python's built-in string equality comparison checks character by character and exits early upon the first mismatch. This exposes the system to timing attacks, as attackers can discern the length and correct characters of the secret API key by measuring response times.
**Prevention:** Always use `secrets.compare_digest()` for cryptographic or secret comparisons, which performs a constant-time comparison. Additionally, guard against `None` values prior to comparing, as `secrets.compare_digest(None, 'string')` throws a `TypeError`.
