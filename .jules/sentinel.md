## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.

## 2024-05-24 - API Key Validation Timing Attack
**Vulnerability:** API key validation endpoints were comparing the user-provided API key directly with `API_KEY` using the equality `==` operator.
**Learning:** This introduces a timing attack vulnerability where an attacker can figure out the API key character-by-character by measuring the time it takes the server to reject the key.
**Prevention:** Always use a constant-time string comparison function, such as `secrets.compare_digest`, when comparing sensitive data like API keys. Ensure that inputs to `secrets.compare_digest` are not `None` since it raises a `TypeError` when given `None`.
