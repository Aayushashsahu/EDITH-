## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.

## 2024-06-10 - [API Key Verification Timing Attack Vulnerability]
**Vulnerability:** The API key validation logic in both REST and WebSocket endpoints (`backend/main.py` and `edith/backend/main.py`) used standard string equality operators (`==`, `!=`). This allowed potential timing attacks since the comparison exits early upon finding the first mismatched character, thereby leaking the length and characters of the correct key through response timing discrepancies.
**Learning:** Even simple authentication mechanisms require constant-time string comparison to prevent leaking secrets. Standard operators short-circuit, which makes them insecure for comparing secrets like passwords or API keys. Guard clauses against `None` are also required since `secrets.compare_digest` throws a TypeError on `None`.
**Prevention:** Always use `secrets.compare_digest(a, b)` for comparing secret values. Additionally, always guard against `None` values prior to running the comparison (e.g., `if val is not None and secrets.compare_digest(val, SECRET):`).
