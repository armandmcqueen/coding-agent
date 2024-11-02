from __future__ import annotations

import base64
from pathlib import Path

from pydantic import BaseModel


class SerializedPythonFile(BaseModel):
    file_name: str
    text_b64: str


class PythonFile:
    def __init__(self, file_name: str, text: str):
        if "/" in file_name:
            raise ValueError("file_name should not contain a path")

        if not file_name.endswith(".py"):
            raise ValueError("file_name should end with '.py'")

        self.file_name = file_name
        self.text = text

    def to_serialized_json(self) -> SerializedPythonFile:
        return SerializedPythonFile(
            file_name=self.file_name,
            text_b64=base64.b64encode(self.text.encode("utf-8")).decode("utf-8"),
        )

    @classmethod
    def from_serialized_json(cls, serialized: SerializedPythonFile) -> PythonFile:
        return cls(
            file_name=serialized.file_name,
            text=base64.b64decode(serialized.text_b64).decode("utf-8"),
        )

    @classmethod
    def from_file(cls, file_name: str, base_path: Path | None = None) -> PythonFile:
        path = base_path or Path(".")
        path = path / file_name
        with open(path, "r", encoding="utf-8") as f:
            return cls(file_name=file_name, text=f.read())

    def save_to_file(self, base_path: Path):
        with open(base_path / self.file_name, "w", encoding="utf-8") as f:
            f.write(self.text)
        return base_path / self.file_name
