from pathlib import Path

from pydantic import BaseModel, model_validator

from .display import DisplayConfig

__all__ = ["SourceConfig", "SelectorConfig"]


class SourceConfig(BaseModel):
    query: str | None = None
    source: Path | None = None

    @model_validator(mode="after")
    @classmethod
    def mutually_exclusive_and_required(cls, self):
        if self.query and self.source:
            raise ValueError("Cannot provide both 'query' and 'source'.")
        if not (self.query or self.source):
            raise ValueError("Must provide one of 'query' and 'source'.")
        return self


class SelectorConfig(DisplayConfig, SourceConfig):
    """
    Configure input source and output display.

      :param query: The query string.
      :param source: The source code.
      :param toml: Whether to display the tags as a TOML-compatible list.
      :param group: Whether to display tags grouped by section.
    """
