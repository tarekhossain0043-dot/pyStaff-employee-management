import json
import os


class FileManager:
    """Handles JSON file read/write operations."""

    def __init__(self, file_path):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        directory = os.path.dirname(self.file_path)

        if directory:
            os.makedirs(directory, exist_ok=True)

        if not os.path.exists(self.file_path):
            self.write([])

    def read(self):
        try:
            with open(
                self.file_path,
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

                return data if isinstance(data, list) else []

        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def write(self, data):
        with open(
            self.file_path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False,
            )
