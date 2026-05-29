from app.parsers.txt_parser import TxtParser
from app.parsers.json_parser import JsonParser


class EmailParser:

    def __init__(self):

        self.txt_parser = TxtParser()
        self.json_parser = JsonParser()

    def parse(self, filepath):

        if filepath.endswith(".txt"):
            return self.txt_parser.parse(filepath)

        elif filepath.endswith(".json"):
            return self.json_parser.parse(filepath)

        else:
            raise ValueError("Unsupported file format")