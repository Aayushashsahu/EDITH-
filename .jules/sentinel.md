## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.
## 2024-06-12 - [API Key Timing Attack]
**Vulnerability:** Fast, early-exit string comparisons (`==`) were used to validate the API key, making the application vulnerable to timing attacks where an attacker could theoretically guess the key character-by-character based on the time taken to reject an incorrect key.
**Learning:** Basic string equality operations in Python are not constant time, which can leak information when handling secrets like API keys. Even in internal or lower-risk apps, using constant-time string comparison for secrets is standard practice.
**Prevention:** Always use `secrets.compare_digest` for validating API keys, tokens, or passwords instead of standard equality operators.
