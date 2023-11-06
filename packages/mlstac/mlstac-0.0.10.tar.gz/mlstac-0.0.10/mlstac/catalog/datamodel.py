import re
from typing import Literal

import pydantic


class Catalog(pydantic.BaseModel):
    """ML-STAC Catalog dataclass."""
    n_items: int
    url: str

    @pydantic.field_validator("n_items")
    def n_items_must_be_valid(cls, value: int) -> int:
        """n_items must be positive"""
        # must be positive
        if value <= 0:
            raise ValueError("n_items must be positive")
        return value