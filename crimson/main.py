# -*- coding: utf-8 -*-
"""
    crimson.main
    ~~~~~~~~~~~~

    Main entry point for command line invocation.

    :copyright: (c) 2015 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
import click

from . import __version__
from .fastqc import fastqc
from .flagstat import flagstat


@click.group()
@click.version_option(__version__)
@click.option("--compact", is_flag=True)
@click.pass_context
def cli(ctx, compact):
    """Converts various non-standard bioinformatics tools' output to JSON.

    :param compact: Whether to create a compact JSON output or not.
    :type compact: bool.

    """
    ctx.params["compact"] = compact

fastqc = cli.command()(fastqc)
flagstat = cli.command()(flagstat)
