## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.

## 2024-05-28 - [Timing Attack in API Key Verification]
**Vulnerability:** API key verification used standard equality operators (`==` and `!=`), making it susceptible to timing attacks. An attacker could potentially guess the API key character by character by measuring the time taken for the server to reject incorrect keys.
**Learning:** Standard string equality checks in Python short-circuit when they find a mismatch, leaking information about the length and content of the expected string.
**Prevention:** Use `secrets.compare_digest(a, b)` for constant-time string comparison when validating secrets like API keys or tokens. Remember to guard against `None` values, as `secrets.compare_digest` raises a `TypeError` if either argument is `None`.
