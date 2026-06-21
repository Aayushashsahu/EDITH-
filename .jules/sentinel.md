## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.

## 2024-05-24 - [Fixed Timing Attack in API Key Verification]
**Vulnerability:** Timing attack vulnerability in `verify_api_key` due to using standard string equality (`==`) to compare API keys.
**Learning:** Using `==` allows an attacker to deduce the correct API key by measuring the time it takes for the comparison to fail.
**Prevention:** Use `secrets.compare_digest` to perform constant-time string comparisons for security-sensitive checks like API keys or tokens. Ensure to guard against `None` values, as `compare_digest(None, ...)` raises a `TypeError`.
