"""Create a hexagon sticker - main logic."""

import logging

from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageOps

import hexsticker.exception as exceptions

DEFAULT_BACKGROUND_COLOR = '#ff000000'
DEFAULT_BORDER_COLOR = 'black'
DEFAULT_PADDING_COLOR = 'white'
DEFAULT_SUPERSAMPLE = 1
HEIGHT_TO_WIDTH_RATIO = 2 / 1.73
SUPPORTED_FILE_TYPES = frozenset(('jpg', 'png', 'jpeg', 'tiff', 'gif', 'bmp', 'eps'))

_LOGGER = logging.getLogger(__name__)


def _get_file_type(file_name: str) -> str:
    """Get file type based on file name extension."""
    extension = file_name.rsplit('.', maxsplit=1)

    if len(extension) != 2:
        raise exceptions.UnknownFileType(f"Unable to determine file type from file {file_name!r}")

    extension = extension[1].lower()

    # Pillow does not know jpg, use jpeg correctly.
    if extension == 'jpg':
        extension = 'jpeg'

    if extension not in SUPPORTED_FILE_TYPES:
        raise exceptions.UnknownFileType(f"Unknown file type {extension!r}, "
                                         f"supported are: {tuple(SUPPORTED_FILE_TYPES)}")

    return extension


def _get_output_file_name(input_file_name: str) -> str:
    """Construct output file name based on input file name."""
    parts = input_file_name.split('.', maxsplit=1)

    # This should be handled before calling this function.
    if len(parts) != 2:
        raise exceptions.SaveError("The input file name has no extension - unable to construct output file name.")

    return f"{parts[0]}-sticker.{parts[1]}"


def _draw_hexagon(img: Image, color: str=None) -> None:
    """Draw surrounding hexagon for the output image."""
    width, height = img.size
    draw = ImageDraw.Draw(img)

    # left up
    draw.polygon(
        ((0, 0), (0, height * 0.25), (0 + width * 0.5, 0)),
        fill=color or 'white'
    )
    # left down
    draw.polygon(
        ((0, height), (0, height - height * 0.25), (0 + width * 0.5, height)),
        fill=color or 'white'
    )
    # right down
    draw.polygon(
        ((width, height), (width, height - height * 0.25), (0 + width * 0.5, height)),
        fill=color or 'white'
    )
    # right up
    draw.polygon(
        ((width, 0), (width, height * 0.25), (width * 0.5, 0)),
        fill=color or 'white'
    )


def _crop_image(img: Image) -> Image:
    """Crop the given image, return a copy of the original image."""
    width, height = img.size

    # Simply fit to a rectangle - we could find the largest area that fits into
    # the original image, but let's keep this simple.
    aspect = min(width, height)
    new_width, new_height = int(aspect / HEIGHT_TO_WIDTH_RATIO), aspect

    width_offset = (width - new_width) // 2
    height_offset = (height - new_height) // 2

    return img.crop((width_offset, height_offset, new_width + width_offset, new_height + height_offset))


def _check_options(border_size: int=0, border_color: str=None,
                   padding_size: int=0, padding_color: str=None,
                   background_color=None,
                   supersample: int=DEFAULT_SUPERSAMPLE) -> tuple:
    """Check supplied options."""
    if padding_size < 0:
        raise exceptions.InvalidOption(f"Padding size has to be non-zero, padding size provided: {padding_size}")

    if border_size < 0:
        raise exceptions.InvalidOption(f"Border size has to be non-zero, border size provided: {border_size}")

    if padding_color:
        try:
            padding_color = ImageColor.getrgb(padding_color)
        except ValueError as exc:
            raise exceptions.InvalidOption(f"Invalid padding color provided: {padding_color!r}") from exc

    if border_color:
        try:
            border_color = ImageColor.getrgb(border_color)
        except ValueError as exc:
            raise exceptions.InvalidOption(f"Invalid border color provided: {border_color!r}") from exc

    if background_color:
        try:
            background_color = ImageColor.getrgb(background_color)
        except ValueError as exc:
            raise exceptions.InvalidOption(f"Invalid background color provided: {background_color!r}") from exc

    if supersample < 1:
        raise exceptions.InvalidOption(f"Supersample must not be less than one, supersample provided: {supersample}")

    return border_color, padding_color, background_color


def create_hexsticker(image: str, output: str, *,
                      border_size: int=0, border_color: str=None,
                      padding_size: int=0, padding_color: str=None,
                      background_color=None,
                      supersample: int=DEFAULT_SUPERSAMPLE) -> str:
    """Create a hexagon sticker.

    :param image: A source image to use as a hexsticker source.
    :param output: A path to output file.
    :param border_size: Size of sticker hexagonal border.
    :param border_color: Color of hexagonal border (defaults to white).
    :param padding_size: Optional padding for the image.
    :param padding_color: Color of padded area (defaults to white).
    :param background_color: Color of background around hexagon
    :param supersample: Scale factor to use for supersampling.
    :return: a path to resulting image
    """
    _LOGGER.debug("Checking supplied options")
    border_color, padding_color, background_color = _check_options(
        border_size=border_size, border_color=border_color,
        padding_size=padding_size, padding_color=padding_color,
        background_color=background_color,
        supersample=supersample,
    )

    _LOGGER.debug("Loading input image")
    try:
        source_img = Image.open(image).convert("RGBA")
    except Exception as exc:
        raise exceptions.LoadError(f"Failed to load input image {image}: {str(exc)}") from exc

    # Cut image to fit aspect ratio, crop to center.
    _LOGGER.debug("Cropping source image")
    img = _crop_image(source_img)

    source_size = img.size
    supersample_size = (source_size[0] * supersample, source_size[1] * supersample)

    if supersample > 1:
        _LOGGER.debug(f"Upscaling source image {supersample}x to {supersample_size}")
        img = img.resize(supersample_size)


    if padding_size:
        _LOGGER.debug("Padding image to center")
        img = ImageOps.expand(img, border=padding_size, fill=padding_color or DEFAULT_PADDING_COLOR)
    elif padding_color:
        raise exceptions.InvalidOption(f"Padding size is set to zero, but padding color set to {padding_color!r}")

    if border_size:
        _LOGGER.debug("Creating hexagon border")
        _draw_hexagon(img, color=border_color or DEFAULT_BORDER_COLOR)
        border = Image.new(
            'RGBA',
            (int(img.size[0] + border_size / HEIGHT_TO_WIDTH_RATIO), img.size[1] + border_size),
            color=border_color or DEFAULT_BORDER_COLOR
        )
        border.paste(img, (int((border_size / HEIGHT_TO_WIDTH_RATIO) / 2), border_size // 2))
        img = border
    elif border_color:
        raise exceptions.InvalidOption(f"Border size is set to zero, but border color set to {border_color!r}")

    _LOGGER.debug("Creating surrounding hexagon")
    _draw_hexagon(img, color=background_color or DEFAULT_BACKGROUND_COLOR)

    if supersample > 1:
        _LOGGER.debug(f"Downscaling output image {supersample}x back to {source_size}")
        img = img.resize(source_size, Image.ANTIALIAS)

    output = output or _get_output_file_name(image)
    output_file_type = _get_file_type(output) if output else _get_file_type(image)
    _LOGGER.debug("Resulting file type: %r", output_file_type)

    _LOGGER.info("Writing output to %r", output)
    with open(output, 'wb') as output_file:
        try:
            img.save(output_file, output_file_type.upper())
        except Exception as exc:
            raise exceptions.SaveError(f"Failed to save resulting image: {str(exc)}") from exc

    return output
