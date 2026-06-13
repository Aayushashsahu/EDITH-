## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.

## 2026-06-13 - [Timing Attack in API Key Verification]
**Vulnerability:** Standard equality `==` was used to compare the API key, leading to a timing attack vulnerability.
**Learning:** Using `==` on strings returns as soon as a mismatch is found, leaking information about the expected string based on comparison time.
**Prevention:** Use `secrets.compare_digest` for comparing secrets, and always guard against `None` values since `secrets.compare_digest(None, 'str')` raises `TypeError`.
