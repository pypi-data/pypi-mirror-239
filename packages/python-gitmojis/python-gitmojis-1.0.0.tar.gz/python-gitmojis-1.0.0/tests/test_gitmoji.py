from dataclasses import FrozenInstanceError, fields

import pytest

from gitmojis.model import Gitmoji


@pytest.fixture()
def gitmoji_json():
    return {
        "emoji": "🐛",
        "entity": "&#x1f41b;",
        "code": ":bug:",
        "description": "Fix a bug.",
        "name": "bug",
        "semver": "patch",
    }


@pytest.fixture()
def gitmoji(gitmoji_json):
    return Gitmoji(**gitmoji_json)


def test_gitmoji_init_populates_fields_from_kwargs(gitmoji_json, gitmoji):
    for key, value in gitmoji_json.items():
        assert getattr(gitmoji, key) == value


@pytest.mark.parametrize(
    "field_name",
    [field.name for field in fields(Gitmoji)],
)
def test_gitmoji_is_immutable(gitmoji, field_name):
    with pytest.raises(FrozenInstanceError):
        setattr(gitmoji, field_name, getattr(gitmoji, field_name))
