## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.
## 2026-06-23 - Prevent Timing Attacks on API Key Validation
**Vulnerability:** Fast API key validation endpoints were using standard equality operators (`==`, `!=`) and lacked `None` handling for API Keys, making them susceptible to timing attacks.
**Learning:** In a performance-optimized system like EDITH, slight variations in processing time from non-constant-time string comparisons can leak the expected API Key to an attacker. Additionally, failing to guard `secrets.compare_digest` with a `None` check causes a `TypeError` resulting in 500 crashes instead of secure 401s when query parameters or headers are absent.
**Prevention:** Always use `secrets.compare_digest` for security comparisons involving secrets or keys. Always guard `secrets.compare_digest` calls with a `None` check before executing the comparison.
