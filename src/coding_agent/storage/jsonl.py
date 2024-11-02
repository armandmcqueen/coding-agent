import json
from pathlib import Path
from typing import Generic, List, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)
U = TypeVar("U", bound=BaseModel)


class JsonlDatabase(Generic[T]):
    def __init__(self, model: type[T], path: Path):
        self.path = path
        self.model = model
        self._items = []

        if path.exists():
            self._items = self._load()

    def __getitem__(self, item: int) -> T:
        return self._items[item]

    def __setitem__(self, key: int, value: T):
        raise NotImplementedError(
            "Cannot set items in JsonlDatabase. The database is append-only."
        )

    def get_all(self) -> List[T]:
        return self._items

    def get_latest(self) -> T | None:
        if not self._items:
            return None
        return self._items[-1]

    def append(self, item: T):
        self._items.append(item)
        self._save(self._items)

    def _save(self, items: List[T]):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(json.dumps({"model": self.model.__name__}) + "\n")
            for item in items:
                f.write(item.model_dump_json() + "\n")

    def _load(self) -> List[T]:
        items = []
        with open(self.path, "r", encoding="utf-8") as f:
            metadata = json.loads(f.readline())
            stored_model_name = metadata.get("model")
            if stored_model_name != self.model.__name__:
                raise ValueError(
                    f"Stored model '{stored_model_name}' does not match expected "
                    f"model '{self.model.__name__}'"
                )
            for line in f:
                items.append(self.model.model_validate_json(line))
        return items
