## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.
## 2026-06-27 - Secure API Key Validation
**Vulnerability:** Timing attacks due to insecure string comparison of API keys using '=='.
**Learning:** The '==' operator exits early on the first mismatch, exposing the system to timing side channels.
**Prevention:** Use 'secrets.compare_digest' to perform constant-time comparisons, ensuring to guard against None values first.
