"""Main entry point for command line invocation"""
# Copyright (c) 2015-2022 Wibowo Arindrarto <contact@arindrarto.dev>
# SPDX-License-Identifier: BSD-3-Clause

from pathlib import Path
from typing import Optional, TextIO, cast

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


@click.group()
@click.version_option(__version__, message="%(version)s")
@click.option(
    "--fmt",
    default="json",
    type=click.Choice(["json", "yaml"]),
    help="Output file format. Default: json.",
)
@click.option(
    "--indent",
    default=2,
    help="Indentation level. Ignored if the --compact flag is set. Default: 2.",
)
@click.option(
    "--compact",
    is_flag=True,
    help="Whether to create a compact JSON or not. Ignored if output format is"
    " YAML.",
)
@click.pass_context
def main(ctx: click.Context, fmt: str, indent: int, compact: bool) -> None:
    """Converts bioinformatics tools' output to a standard format."""
    ctx.params["fmt"] = fmt
    ctx.params["indent"] = indent
    ctx.params["compact"] = compact


@main.command()
@click.argument("input", type=click.Path(exists=True, path_type=str))
@click.argument("output", type=click.File("w"), default="-")
@click.pass_context
def fastqc(ctx: click.Context, input: str, output: TextIO) -> None:
    """Converts FastQC output.

    Use "-" for stdin and/or stdout.

    """
    payload = m_fastqc.parse(Path(input))
    parent = cast(click.Context, ctx.parent)
    write_output(payload, output, **parent.params)


@main.command()
@click.argument("input", type=click.File("r"))
@click.argument("output", type=click.File("w"), default="-")
@click.pass_context
def flagstat(ctx: click.Context, input: TextIO, output: TextIO) -> None:
    """Converts samtools flagstat output.

    Use "-" for stdin and/or stdout.

    """
    payload = m_flagstat.parse(input)
    parent = cast(click.Context, ctx.parent)
    write_output(payload, output, **parent.params)


@main.command()
@click.argument("input", type=click.File("r"))
@click.argument("output", type=click.File("w"), default="-")
@click.pass_context
def fusioncatcher(ctx: click.Context, input: TextIO, output: TextIO) -> None:
    """Converts FusionCatcher output.

    Use "-" for stdin and/or stdout.

    """
    payload = m_fusioncatcher.parse(input)
    parent = cast(click.Context, ctx.parent)
    write_output(payload, output, **parent.params)


@main.command()
@click.argument("input", type=click.File("r"))
@click.argument("output", type=click.File("w"), default="-")
@click.option(
    "--input-linesep",
    default=None,
    type=click.Choice(["posix", "windows"]),
    help=(
        "Line separator for input files; used when parsing. Default: native"
        " value for current operating system."
    ),
)
@click.pass_context
def picard(
    ctx: click.Context,
    input: TextIO,
    output: TextIO,
    input_linesep: Optional[str],
) -> None:
    """Converts Picard metrics output.

    Use "-" for stdin and/or stdout.

    """
    payload = m_picard.parse(input, input_linesep)
    parent = cast(click.Context, ctx.parent)
    write_output(payload, output, **parent.params)


@main.command()
@click.argument("input", type=click.File("r"))
@click.argument("output", type=click.File("w"), default="-")
@click.option(
    "--input-linesep",
    default=None,
    type=click.Choice(["nt", "posix"]),
    help=(
        "Line separator for input files; used when parsing. Default: native"
        " value for current operating system."
    ),
)
@click.pass_context
def star(
    ctx: click.Context,
    input: TextIO,
    output: TextIO,
    input_linesep: Optional[str],
) -> None:
    """Converts STAR Log.final.out file.

    Use "-" for stdin and/or stdout.

    """
    payload = m_star.parse(input, input_linesep)
    parent = cast(click.Context, ctx.parent)
    write_output(payload, output, **parent.params)


@main.command(name="star-fusion")
@click.argument("input", type=click.File("r"))
@click.argument("output", type=click.File("w"), default="-")
@click.pass_context
def star_fusion(ctx: click.Context, input: TextIO, output: TextIO) -> None:
    """Converts output of STAR-Fusion.

    Use "-" for stdin and/or stdout.

    """
    payload = m_star_fusion.parse(input)
    parent = cast(click.Context, ctx.parent)
    write_output(payload, output, **parent.params)


@main.command(name="vep")
@click.argument("input", type=click.File("r"))
@click.argument("output", type=click.File("w"), default="-")
@click.option(
    "--input-linesep",
    default=None,
    type=click.Choice(["nt", "posix"]),
    help=(
        "Line separator for input files; used when parsing. Default: native"
        " value for current operating system."
    ),
)
@click.pass_context
def vep(
    ctx: click.Context,
    input: TextIO,
    output: TextIO,
    input_linesep: Optional[str],
) -> None:
    """Converts plain text output of Variant Effect Predictor.

    Use "-" for stdin and/or stdout.

    """
    payload = m_vep.parse(input)
    parent = cast(click.Context, ctx.parent)
    write_output(payload, output, **parent.params)
