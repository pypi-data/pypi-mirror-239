from pytest import mark

from classipypi import list_tags
from classipypi.interfaces import ListingConfig


@mark.parametrize(
    "exclude,expected",
    [
        (
            [],
            [
                "Development Status :: 1 - Planning",
                "Development Status :: 2 - Pre-Alpha",
                "Development Status :: 3 - Alpha",
                "Development Status :: 4 - Beta",
                "Development Status :: 5 - Production/Stable",
                "Development Status :: 6 - Mature",
                "Development Status :: 7 - Inactive",
            ],
        ),
        (
            ["Alpha"],
            [
                "Development Status :: 1 - Planning",
                "Development Status :: 4 - Beta",
                "Development Status :: 5 - Production/Stable",
                "Development Status :: 6 - Mature",
                "Development Status :: 7 - Inactive",
            ],
        ),
    ],
)
def test_list_dev_statuses(exclude, expected):
    config = ListingConfig(include=["Development Status"], exclude=exclude)
    tags = list_tags(config)
    assert tags == expected
