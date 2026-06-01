from datetime import datetime

class Logger:
    def __init__(self, log_file="processing.log"):
        self.log_file = log_file

    def _time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _write(self, level, message):
        line = f"{self._time()} [{level}] {message}"

        print(line)

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def info(self, message):
        self._write("INFO", message)

    def error(self, message):
        self._write("ERROR", message)
