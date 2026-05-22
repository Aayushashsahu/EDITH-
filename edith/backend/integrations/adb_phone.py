"""
E.D.I.T.H. V8 — ADB Phone Integration
Samsung Galaxy wireless ADB — call detection, answer/end, SMS.
Enable ADB_ENABLED=True and set ADB_IP in config.
"""

import asyncio
import re
import subprocess
import os
import sys
import shlex
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../"))
from config.config import ADB_ENABLED, ADB_IP


def _adb(cmd: str) -> str:
    if not ADB_ENABLED:
        return "[ADB disabled]"
    try:
        if cmd.startswith("shell "):
            args = ["adb", "-s", str(ADB_IP), "shell", cmd[6:]]
        else:
            args = ["adb", "-s", str(ADB_IP)] + shlex.split(cmd)
        r = subprocess.run(args, capture_output=True, text=True, timeout=10)
        return (r.stdout or r.stderr or "").strip()
    except Exception as e:
        return f"ADB error: {e}"


class PhoneControl:
    def connect(self) -> str:
        r = subprocess.run(["adb", "connect", str(ADB_IP)],
                           capture_output=True, text=True, timeout=10)
        return r.stdout.strip()

    def call_state(self) -> str:
        out = _adb("shell dumpsys telephony.registry | grep mCallState")
        if "mCallState=1" in out: return "ringing"
        if "mCallState=2" in out: return "offhook"
        return "idle"

    def caller_info(self) -> str:
        out = _adb("shell dumpsys notification | grep -A5 'com.android.phone'")
        m = re.search(r"(\+?\d[\d\s\-]{7,})", out)
        return m.group(1).strip() if m else "Unknown"

    def answer(self) -> str:
        _adb("shell input keyevent KEYCODE_CALL"); return "Call answered."

    def end(self) -> str:
        _adb("shell input keyevent KEYCODE_ENDCALL"); return "Call ended."

    def sms(self, number: str, message: str) -> str:
        msg = message.replace("'", "\\'")
        _adb(f"shell am start -a android.intent.action.SENDTO "
             f"-d sms:{number} --es sms_body '{msg}' --ez exit_on_sent true")
        return f"SMS queued to {number}."

    def battery(self) -> str:
        out = _adb("shell dumpsys battery | grep level")
        m = re.search(r"level:\s*(\d+)", out)
        return f"Phone battery: {m.group(1)}%" if m else "Unknown"


async def call_monitor(phone: PhoneControl, tts, broadcast):
    if not ADB_ENABLED:
        return
    print("  [ADB]    Call monitor active.")
    last = "idle"
    while True:
        try:
            state = phone.call_state()
            if state == "ringing" and last != "ringing":
                caller = phone.caller_info()
                msg    = f"Incoming call from {caller}."
                await tts.speak_async(msg)
                await broadcast({"type": "notification", "title": "📞 Incoming Call", "message": caller})
            elif state == "idle" and last != "idle":
                await broadcast({"type": "notification", "title": "Call ended", "message": ""})
            last = state
        except Exception:
            pass
        await asyncio.sleep(2)
