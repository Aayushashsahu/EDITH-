## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.
## 2024-05-18 - [API Key Verification Timing Attack]
**Vulnerability:** API key verification in both `backend/main.py` and `edith/backend/main.py` used standard string equality operators (`==` and `!=`) to compare the provided API key with the stored API key.
**Learning:** Using standard string equality operators for comparing sensitive data like API keys, passwords, or tokens introduces a timing attack vulnerability. Standard string comparison returns `False` as soon as it finds a mismatching character. An attacker can use the timing differences to guess the secret character by character.
**Prevention:** Use `secrets.compare_digest` for comparing sensitive data to ensure constant-time comparison, mitigating timing attacks. Always ensure the arguments to `secrets.compare_digest` are not `None` since `secrets.compare_digest(None, 'string')` raises a `TypeError`.
