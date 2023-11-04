import json
from dataclasses import asdict

import click

from gitmojis import defaults


@click.command()
@click.pass_context
def sync(context: click.Context) -> None:
    """Synchronize the backup file with the current state of the API."""
    # Get the `Guide` object from the command's context
    guide = context.obj["guide"]

    # Covert the `Guide` instance from context to a format defined by the API schema
    gitmojis_json = list(map(asdict, guide))

    with defaults.GITMOJI_API_PATH.open("w", encoding="UTF-8") as f:
        # Dump the Gitmoji data to the backup file
        json.dump(gitmojis_json, f, ensure_ascii=False, indent=2)

        # Append a newline to avoid the `end-of-file-fixer` Pre-commit hook error
        f.write("\n")
