# embedded images
# external/local images
# image output handling

import os
import base64
import io
import urllib.request

from reportlab.lib.units import mm
from reportlab.platypus import Image, Spacer, Paragraph

from reportlab.lib.utils import ImageReader
from reportlab.lib import colors

def add_external_or_local_image(content, image_source, notebook_dir):
    """
    Load an image from either:

    1. An HTTP/HTTPS URL
    2. A local file relative to the notebook

    If the image cannot be loaded, return False so that the
    Markdown renderer can fall back to displaying the reference
    as a clickable link.
    """

    try:

        # -------------------------------------------------
        # CASE 1: Image comes from the internet
        # -------------------------------------------------

        if image_source.startswith(("http://", "https://")):

            # Some websites reject requests that do not
            # identify themselves like a normal browser.
            request = urllib.request.Request(
                image_source,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            image_bytes = urllib.request.urlopen(
                request,
                timeout=10
            ).read()

            image_stream = io.BytesIO(
                image_bytes
            )

        # -------------------------------------------------
        # CASE 2: Image is a local file
        # -------------------------------------------------

        else:

            image_path = os.path.join(
                notebook_dir,
                image_source
            )

            # Convert to an absolute path.
            image_path = os.path.abspath(
                image_path
            )

            if not os.path.isfile(image_path):
                return False

            # Read the file into memory.
            # This avoids keeping a file handle open while
            # ReportLab builds the PDF.
            with open(image_path, "rb") as file:

                image_bytes = file.read()

            image_stream = io.BytesIO(
                image_bytes
            )

        # -------------------------------------------------
        # Create the ReportLab image
        # -------------------------------------------------

        image = Image(
            image_stream
        )

        # Keep large images inside the PDF page.
        max_width = 165 * mm
        max_height = 230 * mm

        scale = min(
            max_width / image.drawWidth,
            max_height / image.drawHeight,
            1
        )

        image.drawWidth *= scale
        image.drawHeight *= scale

        content.append(
            image
        )

        content.append(
            Spacer(1, 8)
        )

        return True

    except Exception:

        # If anything goes wrong, don't crash the
        # entire PDF conversion.
        #
        # The renderer will show the original image
        # reference as a clickable link instead.
        return False


def add_embedded_image(content, image_data):
    """
    Render an image whose actual image data is already
    embedded in the notebook as base64.
    """

    # Decode the base64 image data.
    image_bytes = base64.b64decode(image_data)

    # Keep the image in memory.
    image_stream = io.BytesIO(
        image_bytes
    )

    # Create a ReportLab image.
    image = Image(
        image_stream
    )

    # Keep large images within the PDF page.
    max_width = 165 * mm

    if image.drawWidth > max_width:

        scale = (
            max_width
            / image.drawWidth
        )

        image.drawWidth *= scale
        image.drawHeight *= scale

    # Add the image to the PDF.
    content.append(
        image
    )

    content.append(
        Spacer(1, 8)
    )


def add_output_image(content, image_data):
    """
    Render an image stored in a Jupyter code-cell output.

    This handles images produced when a notebook cell was
    actually executed.
    """

    # Convert the base64 text stored by Jupyter
    # back into normal image bytes.
    image_bytes = base64.b64decode(
        image_data
    )

    # Keep the image in memory instead of creating
    # a temporary image file on disk.
    image_stream = io.BytesIO(
        image_bytes
    )

    # Create a ReportLab Image from the in-memory data.
    image = Image(
        image_stream
    )

    # Limit the width so large notebook images
    # don't run outside the PDF page.
    #
    # 165 mm leaves some room for the PDF margins.
    max_width = 165 * mm

    if image.drawWidth > max_width:

        # Maintain the original aspect ratio.
        scale = (
            max_width
            / image.drawWidth
        )

        image.drawWidth *= scale
        image.drawHeight *= scale

    # Add the image to the PDF.
    content.append(
        image
    )

    # Add a little space after the image.
    content.append(
        Spacer(1, 8)
    )


def render_image(content, block, styles):

    add_embedded_image(
        content,
        block["data"]
    )


def render_external_image(content, block, styles):

    success = add_external_or_local_image(
        content,
        block["source"],
        block["notebook_dir"]
    )

    if not success:

        # Escape characters that are special in
        # ReportLab Paragraph markup.
        source = (
            block["source"]
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )

        alt_text = (
            block.get("alt")
            or block["source"]
        )

        alt_text = (
            alt_text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

        content.append(
            Paragraph(
                f'<link href="{source}" color="blue">'
                f'{alt_text}'
                f'</link>',
                styles["text"]
            )
        )
