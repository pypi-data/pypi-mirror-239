import click

from gitmojis.core import fetch_guide


def get_commands() -> list[click.Command]:
    """Return a list of `@click` commands defined in `gitmojis.cli.commands`."""
    from gitmojis.cli import commands as commands_module

    return [
        command
        for command in commands_module.__dict__.values()
        if isinstance(command, click.Command)
    ]


@click.group(
    name="gitmojis",
    commands=get_commands(),
)
@click.option(
    "--use-backup",
    is_flag=True,
    help="Use the backup to fetch data if the API request fails.",
)
@click.version_option(
    package_name="python-gitmojis",
    prog_name="gitmojis",
)
@click.pass_context
def gitmojis_cli(context: click.Context, use_backup: bool) -> None:
    """Command-line interface for managing the official Gitmoji guide."""
    # Initialize the context object
    context.ensure_object(dict)

    # Pass the current state of the Gitmoji guide to the group context
    context.obj["guide"] = fetch_guide(use_backup=use_backup)
