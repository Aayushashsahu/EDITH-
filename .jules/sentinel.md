## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.

## 2024-05-28 - [Timing Attack Vulnerability in API Key Verification]
**Vulnerability:** API key verification used standard string equality operators (`==`, `!=`), which leak information about the correct API key through timing variations depending on where the character mismatch occurs.
**Learning:** Comparing user-supplied secrets against stored secrets using standard equality operators is vulnerable to timing attacks, allowing attackers to incrementally guess the secret.
**Prevention:** Always use `secrets.compare_digest` for comparing sensitive strings like API keys or tokens. Ensure that inputs to `secrets.compare_digest` are not `None` to prevent `TypeError`.
