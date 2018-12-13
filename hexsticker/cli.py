#!/bin/env python3
"""A command line interface for hexsticker."""

import logging

import click

from hexsticker import __name__ as hexsticker_name
from hexsticker import __version__ as hexsticker_version

from hexsticker.create import create_hexsticker
from hexsticker.create import DEFAULT_BACKGROUND_COLOR
from hexsticker.create import DEFAULT_BORDER_COLOR
from hexsticker.create import DEFAULT_PADDING_COLOR
from hexsticker.create import DEFAULT_SUPERSAMPLE

logging.basicConfig()
_LOGGER = logging.getLogger(hexsticker_name)


def _print_version(ctx, _, value):
    """Print version and exit."""
    if not value or ctx.resilient_parsing:
        return

    click.echo(hexsticker_version)
    ctx.exit()


@click.command()
@click.argument('image', type=click.Path(exists=True, dir_okay=False, readable=True))
@click.option('--output', '-o', type=click.Path(exists=False, dir_okay=False, writable=True), required=False,
              help="Output file to write to. If not provided, the output will be IMAGE-sticker.EXT.")
@click.option('--border-size', default=0, show_default=True, type=int,
              help="Size of border around hexagon content.")
@click.option('--border-color', default=None, show_default=True, type=str,
              help=f"A border color, defaults to {DEFAULT_BORDER_COLOR} if not provided.")
@click.option('--padding-size', default=0, show_default=True, type=int,
              help="Padding of the hexagon content.")
@click.option('--padding-color', default=None, show_default=True, type=str,
              help=f"A padding color for padded parts of the hexagon content. "
                   f"Defaults to {DEFAULT_PADDING_COLOR} if not provided.")
@click.option('--background-color', default=None, show_default=True, type=str,
              help=f"Background color for surrounding hexagon. "
                   f"Defaults to {DEFAULT_BACKGROUND_COLOR} if not provided.")
@click.option('--supersample', default=DEFAULT_SUPERSAMPLE, show_default=True, type=int,
              help=f"Scale factor to use for supersampling.")
@click.option('--version', is_flag=True, is_eager=True, callback=_print_version, expose_value=False,
              help=f"Print {hexsticker_name} version and exit.")
@click.option('--verbose', '-v', is_flag=True,
              help="Turn on verbose mode.")
def hexsticker(image, output,
               border_size=0, border_color=None, padding_size=0,
               padding_color=None, background_color=None,
               supersample=DEFAULT_SUPERSAMPLE,
               verbose=False):
    """Convert an image to hexagon sticker as defined by the Stickers Standard.


    Colors can be provided as hexadecimal color specifiers - #rrggbb (e.g. #ff0010),
    RGB function: (e.g. 'rgb(100, 200, 10)'), HSL function: hsl(hue, saturation, lightness) or as
    a common HTML names (e.g. 'white', 'yellow', ...).

    The Stickers Standard is available at https://sticker.how/
    """
    options = locals()
    verbose = options.pop('verbose', False)
    _LOGGER.setLevel(logging.DEBUG if verbose else logging.INFO)
    create_hexsticker(**options)


if __name__ == '__main__':
    hexsticker()
