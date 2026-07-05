## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.
## 2024-05-18 - Fix Timing Attack Vulnerability in API Key Verification
**Vulnerability:** The API key was being verified using standard equality (`==` and `!=`) in `backend/main.py`. This is susceptible to timing attacks, where an attacker could deduce the key based on how long the comparison takes.
**Learning:** Standard string comparisons stop at the first non-matching character, making the duration proportional to the number of correct characters. This pattern existed because standard equality is the default way to compare strings in non-security-critical paths.
**Prevention:** Always use `secrets.compare_digest` to compare sensitive strings like API keys or tokens in constant time. Additionally, ensure the input to `secrets.compare_digest` is explicitly guarded against `None`, as `secrets.compare_digest(None, 'string')` raises a `TypeError`.
