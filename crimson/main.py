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
from . import fusioncatcher as m_fusioncatcher
from . import picard as m_picard
from . import star as m_star
from . import star_fusion as m_star_fusion
from . import vep as m_vep
from .utils import write_output

__all__ = []


@click.group()
@click.version_option(__version__)
@click.option("--fmt", default="json", type=click.Choice(["json", "yaml"]),
              help="Output file format. Default: json.")
@click.option("--indent", default=2,
              help="Indentation level. Ignored if the --compact flag is set. "
              "Default: 2.")
@click.option("--compact", is_flag=True,
              help="Whether to create a compact JSON or not. "
              "Ignored if output format is YAML.")
@click.pass_context
def cli(ctx, fmt, indent, compact):
    """Converts bioinformatics tools' output to a standard format."""
    ctx.params["fmt"] = fmt
    ctx.params["indent"] = indent
    ctx.params["compact"] = compact


@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.File("w"), default="-")
@click.pass_context
def fastqc(ctx, input, output):
    """Converts FastQC output.

    Use "-" for stdin and/or stdout.

    """
    payload = m_fastqc.parse(input)
    write_output(payload, output, **ctx.parent.params)


@cli.command()
@click.argument("input", type=click.File("r"))
@click.argument("output", type=click.File("w"), default="-")
@click.pass_context
def flagstat(ctx, input, output):
    """Converts samtools flagstat output.

    Use "-" for stdin and/or stdout.

    """
    payload = m_flagstat.parse(input)
    write_output(payload, output, **ctx.parent.params)


@cli.command()
@click.argument("input", type=click.File("r"))
@click.argument("output", type=click.File("w"), default="-")
@click.pass_context
def fusioncatcher(ctx, input, output):
    """Converts FusionCatcher output.

    Use "-" for stdin and/or stdout.

    """
    payload = m_fusioncatcher.parse(input)
    write_output(payload, output, **ctx.parent.params)


@cli.command()
@click.argument("input", type=click.File("r"))
@click.argument("output", type=click.File("w"), default="-")
@click.pass_context
def picard(ctx, input, output):
    """Converts Picard metrics output.

    Use "-" for stdin and/or stdout.

    """
    payload = m_picard.parse(input)
    write_output(payload, output, **ctx.parent.params)


@cli.command()
@click.argument("input", type=click.File("r"))
@click.argument("output", type=click.File("w"), default="-")
@click.pass_context
def star(ctx, input, output):
    """Converts STAR Log.final.out file.

    Use "-" for stdin and/or stdout.

    """
    payload = m_star.parse(input)
    write_output(payload, output, **ctx.parent.params)


@cli.command(name="star-fusion")
@click.argument("input", type=click.File("r"))
@click.argument("output", type=click.File("w"), default="-")
@click.pass_context
def star_fusion(ctx, input, output):
    """Converts output of STAR-Fusion.

    Use "-" for stdin and/or stdout.

    """
    payload = m_star_fusion.parse(input)
    write_output(payload, output, **ctx.parent.params)


@cli.command(name="vep")
@click.argument("input", type=click.File("r"))
@click.argument("output", type=click.File("w"), default="-")
@click.pass_context
def vep(ctx, input, output):
    """Converts plain text output of Variant Effect Predictor.

    Use "-" for stdin and/or stdout.

    """
    payload = m_vep.parse(input)
    write_output(payload, output, **ctx.parent.params)
