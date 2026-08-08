## 2024-05-28 - [Command Injection via Windows CMD Bridge]
**Vulnerability:** Command injection vulnerability in WSL-to-Windows `_cmd` execution bridge when untrusted input (e.g., URLs) is passed to `WIN_CMD /c start {url}` without sanitization.
**Learning:** `cmd.exe` easily executes injected commands (via `&` or `&&`), making naive string interpolation extremely dangerous when crossing the OS boundary from WSL to Windows.
**Prevention:** Avoid `_cmd` for untrusted input. Instead, use the PowerShell bridge (`_ps`), enclose inputs strictly in single quotes, and escape any internal single quotes (`replace("'", "''")`) to ensure literal string evaluation.

## 2025-02-12 - Prevent Host Command Injection in Remote Execution with Pipes
**Vulnerability:** The ADB integration used `shell=True` to execute `adb` commands to allow piping logic on the Android device (e.g., `dumpsys | grep`), which introduced a critical command injection vulnerability on the host machine.
**Learning:** We need to support shell-like pipelines on remote systems while keeping execution completely secure and avoiding injection attacks on the host. Standard `shlex.split` cannot parse pipeline operators correctly without stripping them or breaking execution locally.
**Prevention:** Remove `shell=True` completely. For executing complex commands with pipes on remote environments like `adb shell`, construct the arguments list by prefixing the remote command string as a single, cohesive argument to `shell` (e.g., `["adb", "-s", IP, "shell", "dumpsys | grep"]`). This avoids host shell parsing while correctly passing the piped command strictly to the remote shell.
## 2026-07-28 - [Timing Attack Risk in API Key Verification]
**Vulnerability:** Standard equality operators (== and !=) were used to verify API keys in HTTP and WebSocket endpoints, making them susceptible to timing attacks.
**Learning:** Using == to compare secrets leaks information about the secret's length and content, as it short-circuits upon the first mismatch.
**Prevention:** Always use secrets.compare_digest (and ensure both inputs are strings, not None) when comparing secrets like API keys, tokens, or passwords.

## 2024-08-02 - [XSS via Attribute Injection in Frontend]
**Vulnerability:** The custom `esc()` function in the frontend only escaped `<`, `>`, and `&`. It was used to sanitize data placed inside HTML attributes via `innerHTML` (e.g., `aria-label="Complete task: ${esc(t.title)}"`). This allowed attribute-based Cross-Site Scripting (XSS) because unescaped single or double quotes could break out of the attribute and inject malicious event handlers.
**Learning:** Escaping HTML tags is insufficient when rendering data into HTML properties/attributes inside quotes using `innerHTML` or template literals.
**Prevention:** The `esc()` function must explicitly escape single (`'`) and double (`"`) quotes as `&#39;` and `&quot;` to ensure full XSS protection.

## 2024-05-15 - [Authorization Bypass in Telegram Bot via Permissive Defaults]
**Vulnerability:** The Telegram Bot integration (`backend/integrations/telegram_bot.py`) contained a critical authorization bypass vulnerability. The `_guard` function checked `not TELEGRAM_CHAT_ID or str(update.effective_chat.id) == str(TELEGRAM_CHAT_ID)`. If `TELEGRAM_CHAT_ID` was left unconfigured (empty string), `not TELEGRAM_CHAT_ID` evaluated to True, bypassing authorization and allowing ANY Telegram user to control the system.
**Learning:** Security controls that rely on user configuration (like a specific chat ID for remote access) must use a 'deny-by-default' (fail-closed) approach. The system should not fall back to an open, permissive state when the configuration is missing.
**Prevention:** Implement strict fail-closed checks at the entry point of the integration (refusing to start the bot if `TELEGRAM_CHAT_ID` is missing) and ensure authorization guards require the configuration to be explicitly present and truthy before evaluating equality.
