## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.
## 2024-06-02 - Fix Timing Attack in API Key Verification
**Vulnerability:** API keys were being verified using the standard equality operator (`==`), which evaluates character by character and returns early on a mismatch, allowing an attacker to theoretically determine the correct key via a timing attack.
**Learning:** In Python, standard string comparisons are not constant-time. Fast token or API key checks must use secure methods to prevent timing discrepancies.
**Prevention:** Always use `secrets.compare_digest(a, b)` for comparing cryptographic hashes, API keys, or security tokens to ensure constant-time comparison, even when one value may be None (ensure types and null checks are handled properly).
