from pydantic import BaseModel

from .display import DisplayConfig

__all__ = ["FilterConfig", "ListingConfig"]


class FilterConfig(BaseModel):
    include: list[str] = []
    exclude: list[str] = []


class ListingConfig(DisplayConfig, FilterConfig):
    """
    Configure input filtering and output display.

      :param include: Strings to filter tags for.
      :param exclude: Strings to filter tags against.
      :param toml: Whether to display the tags as a TOML-compatible list.
      :param group: Whether to display tags grouped by section.
    """
