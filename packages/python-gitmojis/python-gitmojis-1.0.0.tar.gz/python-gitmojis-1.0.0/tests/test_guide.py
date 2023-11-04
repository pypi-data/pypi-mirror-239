import pytest

from gitmojis.model import Gitmoji, Guide


@pytest.fixture()
def gitmojis_json():
    return [
        {
            "emoji": "💥",
            "entity": "&#x1f4a5;",
            "code": ":boom:",
            "description": "Introduce breaking changes.",
            "name": "boom",
            "semver": "major",
        },
        {
            "emoji": "✨",
            "entity": "&#x2728;",
            "code": ":sparkles:",
            "description": "Introduce new features.",
            "name": "sparkles",
            "semver": "minor",
        },
        {
            "emoji": "🐛",
            "entity": "&#x1f41b;",
            "code": ":bug:",
            "description": "Fix a bug.",
            "name": "bug",
            "semver": "patch",
        },
        {
            "emoji": "📝",
            "entity": "&#x1f4dd;",
            "code": ":memo:",
            "description": "Add or update documentation.",
            "name": "memo",
            "semver": None,
        },
    ]


@pytest.fixture()
def guide(gitmojis_json):
    return Guide(gitmojis=[Gitmoji(**gitmoji_json) for gitmoji_json in gitmojis_json])


def test_guide_init_raises_if_called_with_positional_argument():
    with pytest.raises(TypeError):
        Guide([])


def test_guide_init_succeeds_if_called_with_keyword_argument():
    try:
        Guide(gitmojis=[])
    except TypeError:
        pytest.fail()


def test_guide_gitmojis_returns_data(guide):
    assert guide.gitmojis == guide.data
