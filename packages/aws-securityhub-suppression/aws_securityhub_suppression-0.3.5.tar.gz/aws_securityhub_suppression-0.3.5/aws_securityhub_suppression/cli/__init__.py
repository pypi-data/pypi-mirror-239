from typing import Optional

import click
import os

from aws_securityhub_suppression.cli.context import Context
from aws_securityhub_suppression.cli.handler import CliHandler


@click.command(cls=CliHandler)
@click.option("--debug/--no-debug")
@click.option("--profile", default=os.environ.get("AWS_PROFILE"))
@click.option("--region", default=os.environ.get("AWS_REGION"))
@click.pass_context
def cli(ctx: click.Context, debug: bool, profile: Optional[str], region: Optional[str]):
    """The root of cli."""
    ctx.obj = Context(debug=debug, profile=profile, region=region)


if __name__ == "__main__":
    cli()
