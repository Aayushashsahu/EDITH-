## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.

## 2024-06-04 - [Prevent timing attacks on API key verification]
**Vulnerability:** The application compared API keys using standard equality (`==`), which allows timing attacks because standard string comparison fails quickly on the first mismatched character.
**Learning:** Python's standard `==` string comparison is not constant-time. In security contexts like authentication, it opens an application to side-channel timing attacks to brute-force secrets. Also, `secrets.compare_digest` must be guarded against `None` values to avoid throwing a `TypeError`.
**Prevention:** Always use `secrets.compare_digest` from the built-in `secrets` library to compare API keys, tokens, or passwords to ensure a constant-time comparison, making sure to explicitly check for `None` beforehand.
