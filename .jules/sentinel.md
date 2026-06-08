## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.

## 2024-06-08 - [Timing Attack via String Equality in API Key Verification]
**Vulnerability:** Timing attack vulnerability in `backend/main.py` due to standard string equality comparisons (`==` and `!=`) for `API_KEY` verification. This allows an attacker to deduce the correct API key by observing response times, as standard string equality returns early on the first mismatched character.
**Learning:** String equality comparisons in Python are not constant time. Using them for secrets (like passwords or API keys) can expose the application to timing attacks. Also, `secrets.compare_digest` will throw a TypeError if one of the inputs is None, so inputs must be guarded.
**Prevention:** Always use `secrets.compare_digest()` from the built-in `secrets` module for constant-time comparison of secrets. Ensure that inputs are not `None` before calling `compare_digest`.
