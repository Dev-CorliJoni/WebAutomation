import win32clipboard

from io import BytesIO
from PIL import Image


from logging_helper import get_logger


logger = get_logger(__name__)


def _send_to_clipboard(data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()

    if isinstance(data, str):
        win32clipboard.SetClipboardText(data)
    elif isinstance(data, bytes):
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)

    win32clipboard.CloseClipboard()


def copy(data):
    if isinstance(data, Image.Image):
        with BytesIO() as output:
            data.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]

    _send_to_clipboard(data)