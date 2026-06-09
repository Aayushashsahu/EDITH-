## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.

## 2024-05-28 - [Timing Attack via String Equality on API Keys]
**Vulnerability:** Timing attack vulnerability due to using standard string equality (`==`) when validating API keys (e.g., `api_key_header == API_KEY`).
**Learning:** Standard string comparisons short-circuit as soon as they find a mismatch, leaking information about the valid API key character by character through the response time difference.
**Prevention:** Use `secrets.compare_digest()` for constant-time comparison of sensitive strings like API keys or tokens. Ensure you handle `None` values properly before comparison to avoid `TypeError`.
