"""Exception hierarchy for the hexsticker tool."""


class HexstickerExceptionBase(Exception):
    """A base class for exception hierarchy."""


class UnknownFileType(HexstickerExceptionBase):
    """Raised on invalid/unknown file type. File types are determined based on file extension."""


class LoadError(HexstickerExceptionBase):
    """Raised if the given image file cannot be loaded."""


class SaveError(HexstickerExceptionBase):
    """Raised if the resulting image cannot be saved."""


class InvalidOption(HexstickerExceptionBase):
    """Raised if called with invalid options."""
