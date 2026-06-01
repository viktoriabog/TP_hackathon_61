from datetime import datetime

class Logger:

    def _time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def info(self, message):
        print(f"{self._time()} [INFO] {message}")

    def error(self, message):
        print(f"{self._time()} [ERROR] {message}")
