import base64
from pathlib import Path

import pytest

from coding_agent.serialization.python_file import PythonFile, SerializedPythonFile
from coding_agent.utils.data import data_dir


@pytest.fixture
def example_file(tmp_path: Path):
    file_path = tmp_path / "example.py"
    file_path.write_text("print('Hello, World!')")
    return file_path


def test_init_valid():
    py_file = PythonFile("test.py", "print('Hello')")
    assert py_file.file_name == "test.py"
    assert py_file.text == "print('Hello')"


def test_init_invalid_path():
    with pytest.raises(ValueError, match="file_name should not contain a path"):
        PythonFile("path/to/test.py", "print('Hello')")


def test_init_invalid_extension():
    with pytest.raises(ValueError, match="file_name should end with '.py'"):
        PythonFile("test.txt", "print('Hello')")


def test_to_serialized_json():
    py_file = PythonFile("test.py", "print('Hello')")
    serialized = py_file.to_serialized_json()
    assert isinstance(serialized, SerializedPythonFile)
    assert serialized.file_name == "test.py"
    assert base64.b64decode(serialized.text_b64).decode("utf-8") == "print('Hello')"


def test_from_serialized_json():
    serialized = SerializedPythonFile(
        file_name="test.py",
        text_b64=base64.b64encode("print('Hello')".encode("utf-8")).decode("utf-8"),
    )
    py_file = PythonFile.from_serialized_json(serialized)
    assert py_file.file_name == "test.py"
    assert py_file.text == "print('Hello')"


def test_from_file():
    py_file = PythonFile.from_file("example.py", base_path=data_dir() / "python_scripts")
    assert py_file.file_name == "example.py"
    assert py_file.text == "print('Hello, Example World!')"


def test_save_to_file(tmp_path):
    py_file = PythonFile("test.py", "print('Hello')")
    py_file.save_to_file(base_path=tmp_path)
    saved_file = tmp_path / "test.py"
    assert saved_file.read_text() == "print('Hello')"


def test_roundtrip_serialization():
    original = PythonFile("test.py", "print('Hello, World!')")
    serialized = original.to_serialized_json()
    roundtrip = PythonFile.from_serialized_json(serialized)
    assert roundtrip.file_name == original.file_name
    assert roundtrip.text == original.text


def test_roundtrip_file_io(tmp_path: Path):
    original = PythonFile("test.py", "print('Hello, World!')")
    original.save_to_file(base_path=tmp_path)
    roundtrip = PythonFile.from_file("test.py", base_path=tmp_path)
    assert roundtrip.file_name == original.file_name
    assert roundtrip.text == original.text
