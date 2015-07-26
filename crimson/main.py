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
from . import fastqc as m_fastqc
from . import flagstat as m_flagstat
from . import picard as m_picard
from .utils import write_json

__all__ = []


@click.group()
@click.version_option(__version__)
@click.option("--compact", is_flag=True,
              help="Whether to create a compact JSON or not. "
              "Ignored if output format is YAML.")
@click.pass_context
def cli(ctx, compact):
    """Converts bioinformatics tools' output to a standard format."""
    ctx.params["compact"] = compact


@cli.command()
@click.argument("input", type=click.File("r"))
@click.argument("output", type=click.File("w"))
@click.pass_context
def fastqc(ctx, input, output):
    """Converts FastQC output.

    Use "-" for stdin and/or stdout.

    """
    payload = m_fastqc.parse(input)
    write_json(payload, output, ctx.parent.params["compact"])


@cli.command()
@click.argument("input", type=click.File("r"))
@click.argument("output", type=click.File("w"))
@click.pass_context
def flagstat(ctx, input, output):
    """Converts samtools flagstat output.

    Use "-" for stdin and/or stdout.

    """
    payload = m_flagstat.parse(input)
    write_json(payload, output, ctx.parent.params["compact"])


@cli.command()
@click.argument("input", type=click.File("r"))
@click.argument("output", type=click.File("w"))
@click.pass_context
def picard(ctx, input, output):
    """Converts Picard metrics output.

    Use "-" for stdin and/or stdout.

    """
    payload = m_picard.parse(input)
    write_json(payload, output, ctx.parent.params["compact"])
