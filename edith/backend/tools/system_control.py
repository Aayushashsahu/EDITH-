"""
E.D.I.T.H. V8 — System Control
Full Windows control from WSL via cmd.exe / PowerShell bridge.
Also handles WSL-side file ops, shell commands, processes.
"""

import os
import re
import subprocess
import datetime
import socket
import psutil
from pathlib import Path
from config.config import WIN_CMD, WIN_PS, WIN_USER, NOTES_FILE


# ── Windows bridge helpers ────────────────────────────────────────────────────
def _cmd(command: str) -> str:
    try:
        r = subprocess.run([WIN_CMD, "/c", command],
                           capture_output=True, text=True, timeout=15)
        return (r.stdout or r.stderr or "").strip()[:2000]
    except FileNotFoundError:
        return "[Bridge unavailable — check WIN_CMD path in config.py]"
    except subprocess.TimeoutExpired:
        return "Command timed out."
    except (subprocess.SubprocessError, OSError) as e:
        return f"Error: {e}"

def _ps(script: str) -> str:
    try:
        r = subprocess.run([WIN_PS, "-NoProfile", "-Command", script],
                           capture_output=True, text=True, timeout=20)
        return (r.stdout or r.stderr or "").strip()[:2000]
    except FileNotFoundError:
        return "[PowerShell bridge unavailable]"
    except (subprocess.SubprocessError, OSError) as e:
        return f"PowerShell error: {e}"


class SystemControl:

    # ── Time / date ───────────────────────────────────────────────────────────
    def get_time(self) -> str:
        now = datetime.datetime.now()
        return now.strftime("It is %I:%M %p on %A, %d %B %Y.")

    # ── System stats ──────────────────────────────────────────────────────────
    def system_info(self) -> str:
        cpu  = psutil.cpu_percent(interval=0.5)
        ram  = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        bat  = psutil.sensors_battery()
        bat_s = f"{bat.percent:.0f}% ({'charging' if bat.power_plugged else 'on battery'})" if bat else "N/A"
        return (f"CPU {cpu}%  ·  RAM {ram.percent}% "
                f"({ram.used>>20}MB/{ram.total>>20}MB)  ·  "
                f"Disk {disk.percent}%  ·  Battery {bat_s}")

    def stats_dict(self) -> dict:
        cpu  = psutil.cpu_percent(interval=0.3)
        ram  = psutil.virtual_memory()
        bat  = psutil.sensors_battery()
        return {
            "cpu":     round(cpu, 1),
            "ram":     round(ram.percent, 1),
            "ram_mb":  ram.used >> 20,
            "ram_total": ram.total >> 20,
            "battery": f"{bat.percent:.0f}%" if bat else "N/A",
            "charging": bat.power_plugged if bat else False,
        }

    # ── Apps (Windows) ────────────────────────────────────────────────────────
    _APPS = {
        "edge":        "start msedge",
        "chrome":      "start chrome",
        "firefox":     "start firefox",
        "vscode":      "code .",
        "code":        "code .",
        "spotify":     "start spotify",
        "discord":     "start discord",
        "telegram":    "start telegram",
        "notepad":     "notepad",
        "explorer":    "explorer",
        "calculator":  "calc",
        "taskmanager": "taskmgr",
        "cmd":         "start cmd",
        "powershell":  "start powershell",
        "settings":    "start ms-settings:",
        "vlc":         "start vlc",
        "obs":         "start obs64",
        "steam":       "start steam",
        "whatsapp":    "start whatsapp",
        "paint":       "mspaint",
        "word":        "start winword",
        "excel":       "start excel",
    }

    def open_app(self, app: str) -> str:
        key = re.sub(r"\s+", "", app.lower())
        cmd = self._APPS.get(key, f"start {app}")
        _cmd(cmd)
        return f"Opening {app}."

    def close_app(self, app: str) -> str:
        out = _cmd(f"taskkill /F /IM {app}.exe 2>&1")
        if "SUCCESS" in out or "terminated" in out.lower():
            return f"Closed {app}."
        # fallback to psutil
        killed = sum(1 for p in psutil.process_iter(["name"])
                     if app.lower() in p.info["name"].lower() and not p.kill())
        return f"Closed {killed} instance(s) of {app}." if killed else f"{app} not found."

    def open_url(self, url: str) -> str:
        import urllib.parse
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        try:
            parsed = urllib.parse.urlparse(url)
            if parsed.scheme not in ("http", "https"):
                return "Invalid URL scheme. Only http and https are allowed."

            safe_url = urllib.parse.urlunparse((
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                parsed.query,
                parsed.fragment
            ))

            # Using _ps() safely opens URLs on Windows bypassing cmd.exe shell interpolation.
            # We must ensure powershell doesn't evaluate the string either.
            # Let's escape single quotes since we pass it to powershell in single quotes.
            safe_url_ps = safe_url.replace("'", "''")

            _ps(f"Start-Process '{safe_url_ps}'")
            return f"Opened {safe_url}."
        except Exception as e:
            return f"Error opening URL: {e}"

    # ── Power ─────────────────────────────────────────────────────────────────
    def lock(self)     -> str: _cmd("rundll32.exe user32.dll,LockWorkStation"); return "Screen locked."
    def sleep(self)    -> str: _cmd("rundll32.exe powrprof.dll,SetSuspendState 0,1,0"); return "Sleeping. Goodnight."
    def shutdown(self) -> str: _cmd("shutdown /s /t 15"); return "Shutting down in 15 seconds."
    def restart(self)  -> str: _cmd("shutdown /r /t 15"); return "Restarting in 15 seconds."

    # ── Volume ────────────────────────────────────────────────────────────────
    def set_volume(self, pct: int) -> str:
        pct = max(0, min(100, pct))
        out = _cmd(f"nircmd setsysvolume {int(pct*655.35)}")
        if "not recognized" in out.lower():
            return "Install nircmd for volume control. (https://www.nirsoft.net/utils/nircmd.html)"
        return f"Volume set to {pct}%."

    def mute(self) -> str:
        _ps("(New-Object -ComObject WScript.Shell).SendKeys([char]173)")
        return "Toggled mute."

    def volume_up(self)   -> str:
        _ps("(New-Object -ComObject WScript.Shell).SendKeys([char]175)")
        return "Volume up."

    def volume_down(self) -> str:
        _ps("(New-Object -ComObject WScript.Shell).SendKeys([char]174)")
        return "Volume down."

    # ── Screenshot ────────────────────────────────────────────────────────────
    def screenshot(self) -> str:
        ts  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        win = f"C:\\Users\\{WIN_USER}\\Pictures\\edith_{ts}.png"
        ps  = (
            "Add-Type -AssemblyName System.Windows.Forms,System.Drawing;"
            "$b=[System.Drawing.Rectangle]::FromLTRB(0,0,"
            "[System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width,"
            "[System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height);"
            "$bmp=New-Object System.Drawing.Bitmap($b.Width,$b.Height);"
            "$g=[System.Drawing.Graphics]::FromImage($bmp);"
            "$g.CopyFromScreen($b.Location,[System.Drawing.Point]::Empty,$b.Size);"
            f"$bmp.Save('{win}');"
        )
        _ps(ps)
        return f"Screenshot saved to {win}"

    # ── Keyboard / input ──────────────────────────────────────────────────────
    def type_text(self, text: str) -> str:
        safe = text.replace("'", "''")
        _ps(f"(New-Object -ComObject WScript.Shell).SendKeys('{safe}')")
        return f"Typed: {text}"

    def hotkey(self, keys: str) -> str:
        _ps(f"(New-Object -ComObject WScript.Shell).SendKeys('{keys}')")
        return f"Sent keys: {keys}"

    # ── Windows toast notification ────────────────────────────────────────────
    def notify(self, title: str, body: str) -> str:
        ps = (
            "Add-Type -AssemblyName System.Windows.Forms;"
            "$n=New-Object System.Windows.Forms.NotifyIcon;"
            "$n.Icon=[System.Drawing.SystemIcons]::Information;"
            "$n.Visible=$true;"
            f"$n.ShowBalloonTip(5000,'{title}','{body}',[System.Windows.Forms.ToolTipIcon]::None);"
        )
        _ps(ps)
        return f"Notification: {title}"

    # ── Shell (WSL/Linux side) ────────────────────────────────────────────────
    def shell(self, cmd: str) -> str:
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=20)
            return (r.stdout or r.stderr or "No output.").strip()[:2000]
        except subprocess.TimeoutExpired:
            return "Command timed out."
        except (subprocess.SubprocessError, OSError) as e:
            return f"Shell error: {e}"

    # ── Files ─────────────────────────────────────────────────────────────────
    def ls(self, path: str = "~") -> str:
        p = Path(os.path.expanduser(path.strip()))
        if not p.exists():
            return f"Path not found: {p}"
        items = sorted(p.iterdir(), key=lambda x: (x.is_file(), x.name))
        return f"{p}:\n" + "\n".join(
            ("📁 " if i.is_dir() else "📄 ") + i.name for i in items[:40])

    def read_file(self, path: str) -> str:
        p = Path(os.path.expanduser(path.strip()))
        if not p.exists():
            return f"File not found: {p}"
        return p.read_text(errors="ignore")[:3000]

    def create_file(self, path: str, content: str = "") -> str:
        p = Path(os.path.expanduser(path.strip()))
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        return f"Created: {p}"

    # ── Notes ─────────────────────────────────────────────────────────────────
    def save_note(self, text: str) -> str:
        ts = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M]")
        with open(NOTES_FILE, "a") as f:
            f.write(f"{ts} {text}\n")
        return "Note saved."

    def read_notes(self) -> str:
        if not NOTES_FILE.exists():
            return "No notes yet."
        lines = NOTES_FILE.read_text().splitlines()
        return "\n".join(lines[-25:]) or "Empty."

    # ── Processes ─────────────────────────────────────────────────────────────
    def list_processes(self) -> str:
        skip = {"kworker","systemd","bash","python3","sh","grep","ps","cat"}
        names = sorted({p.name() for p in psutil.process_iter(["name"])
                        if p.name() not in skip})[:24]
        return "Running: " + "  ·  ".join(names)

    # ── Network ───────────────────────────────────────────────────────────────
    def net_info(self) -> str:
        h = socket.gethostname()
        try:
            ip = socket.gethostbyname(h)
        except OSError:
            ip = "unknown"
        return f"Host: {h}  ·  IP: {ip}"
