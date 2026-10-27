"""Drain bounded subprocess diagnostics without blocking a streaming protocol."""
import os
import re
import threading


def redact(text, env=None):
    text = str(text)
    for name, value in (env or os.environ).items():
        if value and len(value) >= 6 and re.search(r'(?:KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL)', name, re.I):
            text = text.replace(value, '[secret hidden]')
    text = re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]', '', text)
    text = re.sub(r'(?i)(authorization["\s:]+(?:bearer\s+)?)[^\s",}]+', r'\1[secret hidden]', text)
    text = re.sub(r'(?i)((?:api[_-]?key|access[_-]?token|refresh[_-]?token|password|client_secret)["\s]*[:=]["\s]*)[^\s",}]+', r'\1[secret hidden]', text)
    return text


class ErrorTail:
    def __init__(self, process, env=None):
        self.text, self.env = '', env
        def read():
            try:
                while chunk := process.stderr.read(1024):
                    self.text = (self.text + chunk)[-8000:]
            except (OSError, ValueError):
                pass
        self.reader = threading.Thread(target=read, daemon=True)
        self.reader.start()

    def message(self, fallback):
        self.reader.join(timeout=.5)
        return redact(self.text.strip()[-4000:], self.env) or fallback

    def send(self, process, text):
        try:
            process.stdin.write(text)
            process.stdin.flush()
        except (BrokenPipeError, OSError):
            raise ValueError(self.message('The AI app closed before receiving your request. Check its connection and try again.')) from None

    @staticmethod
    def close_input(process):
        try:
            process.stdin.close()
        except OSError:
            pass
