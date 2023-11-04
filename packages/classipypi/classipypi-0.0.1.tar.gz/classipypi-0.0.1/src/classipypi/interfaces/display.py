from pydantic import BaseModel

__all__ = ["DisplayConfig"]


class DisplayConfig(BaseModel):
    toml: bool = False
    group: bool = False
