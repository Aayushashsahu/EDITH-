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

## 2024-08-10 - [Command Injection via PowerShell Bridge Interpolation]
**Vulnerability:** Methods in `system_control.py` (like `open_app`, `close_app`, `notify`, and `hotkey`) passed unsanitized string arguments directly into PowerShell strings (e.g. `Start-Process '{app}'`), allowing an attacker to break out of the string context and execute arbitrary PowerShell code if they included a single quote in their payload.
**Learning:** Passing user-supplied strings directly into PowerShell commands enclosed in single quotes is dangerous if the input itself contains single quotes. It breaks the string literal context and evaluates subsequent text as code.
**Prevention:** Always escape single quotes in variables before passing them into the `_ps` PowerShell bridge by replacing them with two single quotes (`replace("'", "''")`).
## 2024-05-18 - Fix authorization bypass in Telegram bot
**Vulnerability:** The Telegram integration used a fail-open authorization check `not TELEGRAM_CHAT_ID or str(update.effective_chat.id) == str(TELEGRAM_CHAT_ID)`, meaning if a user neglected to configure `TELEGRAM_CHAT_ID`, the bot would accept commands from any Telegram user on the internet. It also lacked authorization checks on the `/start` command.
**Learning:** Security controls that rely on user configuration (such as a remote bot token or `TELEGRAM_CHAT_ID`) must use a "deny-by-default" (fail-closed) approach. If the required configuration is missing, the service should actively refuse to start or explicitly deny access rather than falling back to an open, permissive state.
**Prevention:** Ensure all authorization logic follows a fail-closed pattern (`bool(CONFIG_VAR) and user == CONFIG_VAR`). Ensure critical services refuse to initialize if required security configuration is absent.

## 2024-08-26 - [FastAPI WebSocket Cross-Site WebSocket Hijacking (CSWSH)]
**Vulnerability:** FastAPIs/Starlettes CORSMiddleware does not automatically apply to WebSocket endpoints. The codebase accepted WebSocket connections unconditionally without manually checking the `Origin` header.
**Learning:** `CORSMiddleware` in FastAPI only applies to HTTP REST routes. This is a common pitfall where WebSocket endpoints remain completely unprotected from cross-origin requests.
**Prevention:** Always manually retrieve and validate the `Origin` header (`ws.headers.get("origin")`) against an allowed origin list (and handle wildcards appropriately) in all WebSocket endpoint handlers before calling `await ws.accept()`.
