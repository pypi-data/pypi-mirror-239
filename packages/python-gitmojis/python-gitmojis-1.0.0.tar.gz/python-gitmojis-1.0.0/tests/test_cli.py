import subprocess
import sys

import click
import requests

from gitmojis.cli import commands as commands_module
from gitmojis.cli import get_commands, gitmojis_cli
from gitmojis.model import Guide


def test_gitmojis_cli_runs_as_entry_point():
    result = subprocess.run(["gitmojis"])

    assert result.returncode == 0


def test_gitmojis_cli_runs_as_python_script():
    result = subprocess.run([sys.executable, "-m", "gitmojis"])

    assert result.returncode == 0


def test_get_commands_registers_command_from_commands_module(mocker):
    @click.command()
    def command():
        pass

    mocker.patch.dict(commands_module.__dict__, {"command": command})

    commands = get_commands()

    assert command in commands


def test_gitmojis_cli_passes_guide_to_context(mocker, cli_runner):
    mocker.patch("gitmojis.core.fetch_guide", return_value=Guide(gitmojis=[]))

    @click.command()
    @click.pass_context
    def command(context):
        assert "guide" in context.obj

    gitmojis_cli.add_command(command)

    result = cli_runner.invoke(gitmojis_cli, "command")

    assert result.exit_code == 0


def test_gitmojis_cli_passes_use_backup_option_to_fetch_guide(mocker, cli_runner):
    fetch_guide = mocker.patch("gitmojis.cli.fetch_guide", return_value=Guide())

    @click.command()
    @click.pass_context
    def command(context):
        pass

    gitmojis_cli.add_command(command)

    cli_runner.invoke(gitmojis_cli, ["--use-backup", "command"])

    assert fetch_guide.call_args.kwargs == {"use_backup": True}


def test_sync_command_dumps_api_data_to_backup_file(tmp_path, mocker, cli_runner):
    # Mock the backup file as empty file
    gitmoji_api_path = tmp_path / "gitmojis.json"
    mocker.patch("gitmojis.defaults.GITMOJI_API_PATH", gitmoji_api_path)

    # Mock response
    response = mocker.Mock(spec_set=requests.Response)
    response.json.return_value = {"gitmojis": []}
    mocker.patch("requests.get", return_value=response)

    # Run command
    cli_runner.invoke(gitmojis_cli, ["sync"])

    assert gitmoji_api_path.read_text(encoding="UTF-8") == "[]\n"
