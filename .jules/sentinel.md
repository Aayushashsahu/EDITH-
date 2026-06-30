## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.
## 2024-05-18 - [Preventing Timing Attacks in API Key Verification]
**Vulnerability:** API key verification was performed using standard equality operators (`==`, `!=`), which are susceptible to timing attacks.
**Learning:** Python's standard equality operators evaluate character by character and return early if a mismatch is found. This early return can be measured by an attacker to slowly brute force a secret by guessing one character at a time.
**Prevention:** Use `secrets.compare_digest(a, b)` for comparing sensitive strings like API keys or tokens. It performs the comparison in constant time, meaning it takes the same amount of time regardless of where the mismatch occurs, defeating timing attacks. Always ensure inputs are not `None` before passing them to `compare_digest` to avoid `TypeError`.
