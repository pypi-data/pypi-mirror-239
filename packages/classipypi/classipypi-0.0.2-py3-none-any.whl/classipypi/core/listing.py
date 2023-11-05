from trove_classifiers import sorted_classifiers

from ..interfaces import ListingConfig

__all__ = ["list_tags"]


def list_tags(config: ListingConfig) -> list[str]:
    tags = sorted_classifiers
    if config.include:
        tags = [
            tag
            for tag in tags
            for query in config.include
            if (
                (query.lower() in tag.lower())
                if config.case_insensitive
                else (query in tag)
            )
        ]
    if config.exclude:
        tags = [
            tag
            for tag in tags
            for query in config.exclude
            if (
                (query.lower() not in tag.lower())
                if config.case_insensitive
                else (query not in tag)
            )
        ]
    return tags
