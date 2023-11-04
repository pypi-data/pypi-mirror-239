import pytest
import requests

from gitmojis import defaults
from gitmojis.core import fetch_guide
from gitmojis.exceptions import ApiRequestError, ResponseJsonError
from gitmojis.model import Guide


@pytest.fixture()
def response(mocker):
    return mocker.Mock(spec_set=requests.Response)


def test_fetch_guide_creates_guide_from_api_response_json(mocker, response):
    response.json.return_value = {defaults.GITMOJI_API_KEY: []}

    mocker.patch("requests.get", return_value=response)

    guide = fetch_guide()

    assert isinstance(guide, Guide)


def test_fetch_guide_raises_error_if_gitmoji_api_key_not_in_response_json(mocker, response):  # fmt: skip
    response.json.return_value = {}  # `GITMOJI_API_KEY` not in the response's JSON

    mocker.patch("requests.get", return_value=response)

    with pytest.raises(ResponseJsonError):
        fetch_guide()


def test_fetch_guide_falls_back_to_backup_data_if_request_error_and_using_backup(mocker):  # fmt: skip
    mocker.patch("pathlib.Path.open", mocker.mock_open(read_data="[]"))
    mocker.patch("requests.get", side_effect=requests.RequestException)

    json_load = mocker.patch("json.load")

    guide = fetch_guide(use_backup=True)

    assert json_load.called
    assert guide == Guide(gitmojis=[])


def test_fetch_guide_raises_error_if_request_error_and_not_using_backup(mocker):
    mocker.patch("requests.get", side_effect=requests.RequestException)

    with pytest.raises(ApiRequestError) as exc_info:
        fetch_guide(use_backup=False)
    assert isinstance(exc_info.value.__cause__, requests.RequestException)
