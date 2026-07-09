## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.

## 2024-05-28 - [Timing Attack Vulnerability in API Key Validation]
**Vulnerability:** API key validation in FastAPI endpoints (`verify_api_key` and `ws_endpoint`) used standard string equality operators (`==`, `!=`). This allows an attacker to deduce the valid API key character by character by measuring the response time (timing attack), as standard string comparison fails fast on the first mismatched character.
**Learning:** Security-sensitive string comparisons, such as checking passwords or API keys, must use constant-time operations to prevent timing side-channel attacks. Standard equality operators in Python are not constant-time. Additionally, `secrets.compare_digest` throws a `TypeError` if one of the arguments is `None`, so `None` checks are mandatory before calling it.
**Prevention:** Use `secrets.compare_digest(a, b)` for comparing API keys or other secrets. Always guard against `None` values (e.g., missing headers or query parameters) before calling `compare_digest`.
