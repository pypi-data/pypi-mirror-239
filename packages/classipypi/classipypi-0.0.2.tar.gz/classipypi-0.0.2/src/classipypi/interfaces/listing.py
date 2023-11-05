from pydantic import BaseModel

from .display import DisplayConfig

__all__ = ["FilterConfig", "ListingConfig"]


class FilterConfig(BaseModel):
    include: list[str] = []
    exclude: list[str] = []
    case_insensitive: bool = False


class ListingConfig(DisplayConfig, FilterConfig):
    """
    Configure input filtering and output display.

      :param include: Strings to filter tags for.
      :param exclude: Strings to filter tags against.
      :param case_insensitive: Whether to match case-insensitively.
      :param toml: Whether to display the tags as a TOML-compatible list.
      :param group: Whether to display tags grouped by section.
    """
