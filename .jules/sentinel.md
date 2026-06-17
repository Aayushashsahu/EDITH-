## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.

## 2025-02-28 - [Timing Attack via String Equality in API Key Verification]
**Vulnerability:** Timing attack vulnerability in API key verification using standard equality (`==`) which compares character-by-character and stops at the first mismatch, potentially leaking key information via response time differences.
**Learning:** `secrets.compare_digest` must be used for securely comparing sensitive values like API keys to ensure constant time execution regardless of matching characters. It requires guards against `None` values since `secrets.compare_digest(None, 'string')` raises a `TypeError`.
**Prevention:** Always use `secrets.compare_digest` for secret comparisons and validate inputs against `None` before comparison.
