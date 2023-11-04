import re
from typing import Literal

import pydantic


class Catalog(pydantic.BaseModel):
    """ML-STAC Catalog dataclass."""

    model_config = pydantic.ConfigDict(extra="forbid")

    name: Literal["train", "test", "val"]
    n_items: int

    @pydantic.field_validator("name")
    def name_must_be_valid(cls, value: str) -> str:
        """name must be only train, test, or val"""
        if not re.match(r"train|test|val", value):
            raise ValueError("name must be one of train, test, or val")
        return value

    @pydantic.field_validator("n_items")
    def n_items_must_be_valid(cls, value: int) -> int:
        """n_items must be positive"""
        # must be positive
        if value <= 0:
            raise ValueError("n_items must be positive")
        return value
