## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.

## 2024-06-05 - [Timing Attack on API Key Verification]
**Vulnerability:** Fast fail short-circuiting on string comparisons (`==`, `!=`) allows attackers to guess valid API keys character-by-character by observing server response times (Timing Attack). This occurred in `verify_api_key` and `ws_endpoint` for the `API_KEY` checking in `backend/main.py`.
**Learning:** Standard equality operators in Python fail immediately at the first non-matching character, introducing measurable latency differences based on how many initial characters match. Additionally, `secrets.compare_digest` raises `TypeError` if passed `None`, requiring an explicit null-guard.
**Prevention:** Always use `secrets.compare_digest(a, b)` for cryptographic/security token comparisons to ensure constant-time checking, and always explicitly verify inputs are `not None` beforehand.
