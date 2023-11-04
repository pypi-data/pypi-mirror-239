import json

import pytest

from gitmojis import defaults
from gitmojis.model import Gitmoji


def test_gitmoji_api_path_file_is_json_decodable():
    try:
        with defaults.GITMOJI_API_PATH.open(encoding="UTF-8") as f:
            json.load(f)
    except json.JSONDecodeError:
        pytest.fail()


def test_gitmoji_api_path_file_data_is_list_of_dicts():
    with defaults.GITMOJI_API_PATH.open(encoding="UTF-8") as f:
        gitmojis_json = json.load(f)

    assert isinstance(gitmojis_json, list)
    assert all(isinstance(gitmoji_json, dict) for gitmoji_json in gitmojis_json)


def test_gitmoji_api_path_file_data_can_create_gitmoji_objects():
    with defaults.GITMOJI_API_PATH.open(encoding="UTF-8") as f:
        gitmojis_json = json.load(f)

    for gitmoji_json in gitmojis_json:
        gitmoji = Gitmoji(**gitmoji_json)

        assert isinstance(gitmoji, Gitmoji)
