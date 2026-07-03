## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.
## 2024-05-18 - [API Key Timing Attack]
**Vulnerability:** Comparing API keys using standard equality (`==`) allows timing attacks, where an attacker can determine the correct key character by character based on how long the comparison takes.
**Learning:** Python`s standard equality operator short-circuits on the first mismatch, leaking timing information.
**Prevention:** Always use `secrets.compare_digest` (and check for `None` to prevent TypeErrors) when comparing security secrets.
