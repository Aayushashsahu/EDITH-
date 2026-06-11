## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.

## $(date +%Y-%m-%d) - Fix Timing Attack in API Key Verification
**Vulnerability:** API keys were being validated using simple string equality (`==` and `!=`). This is susceptible to timing attacks, as string comparisons often exit early upon finding the first differing character, leaking information about the valid key based on response times.
**Learning:** This existed due to using basic Python string comparisons (`==`) directly on security-sensitive values instead of utilizing constant-time comparison methods. Additionally, handling `None` checks was required since the safe comparison method throws an error on `None` input.
**Prevention:** Always use `secrets.compare_digest` for validating authentication tokens, API keys, or passwords. Ensure robust guardrails like `is not None` exist around these calls to prevent application errors on missing tokens.
