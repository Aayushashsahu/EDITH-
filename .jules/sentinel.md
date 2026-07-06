## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.

## 2024-05-18 - Timing Attack Vulnerability in API Key Verification
**Vulnerability:** The API key validation used the standard equality operator (`==`) to compare user input with the expected API key, allowing for potential timing attacks to guess the API key.
**Learning:** Standard string comparisons stop at the first mismatching character. An attacker could measure the response time of API key verifications to determine how many initial characters were guessed correctly, slowly reconstructing the entire key.
**Prevention:** Use `secrets.compare_digest()` for validating sensitive tokens like API keys or passwords. It performs comparison in constant time, defeating timing attacks. Always ensure the inputs are not `None` before passing to `compare_digest` to avoid `TypeError`.
