## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.

## 2024-06-15 - [API Key Timing Attack in FastAPI]
**Vulnerability:** Timing attack vulnerability when comparing API keys using standard equality operator (`==`) in FastAPI endpoints.
**Learning:** Standard string comparison stops at the first mismatched character, allowing an attacker to deduce the expected key by measuring the response time. Additionally, `secrets.compare_digest` raises a TypeError if passed a `None` value, which must be handled before the comparison.
**Prevention:** Use `secrets.compare_digest` instead of `==` to compare sensitive tokens like API keys, ensuring constant time execution regardless of mismatches. Always ensure `None` values are handled safely before passing them to the digest function.
