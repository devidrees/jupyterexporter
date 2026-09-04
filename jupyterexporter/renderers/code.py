# handle code cells and inline code
# code box    Jupyter code cells    cell outputs    

from reportlab.platypus import (
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.units import mm

from .images import add_output_image

def add_code_box(
    content,
    code,
    styles,
    language=None
):

    # Show the language above fenced code blocks
    if language:

        content.append(
            Paragraph(
                language.upper(),
                styles["code_language"]
            )
        )

    code = code.rstrip()

    # Preformatted keeps indentation and spacing intact
    code_block = Preformatted(
        code,
        styles["code"]
    )

    # Put the code inside a table so we can draw a box
    code_table = Table(
        [[code_block]],
        colWidths=[170 * mm]
    )

    code_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                colors.whitesmoke
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.5,
                colors.lightgrey
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                8
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8
            ),
        ])
    )

    content.append(
        code_table
    )

    content.append(
        Spacer(1, 10)
    )


def add_code_cell(
    content,
    source,
    styles,
    language=None
):

    # Use the language name when known.
    # Otherwise use CODE: as the fallback.
    if language:

        label = language.upper()

    else:

        label = "CODE:"

    content.append(
        Paragraph(
            label,
            styles["code_label"]
        )
    )

    add_code_box(
        content,
        source,
        styles
    )


def add_cell_outputs(content, cell):

    # Get all outputs from this cell.
    #
    # If the cell has never been executed, "outputs"
    # will normally be an empty list.
    outputs = cell.get("outputs", [])

    for output in outputs:

        # Different output types store their data slightly
        # differently, so first get the "data" dictionary.
        data = output.get("data", {})

        # -------------------------------------------------
        # PNG image
        # -------------------------------------------------

        if "image/png" in data:

            add_output_image(
                content,
                data["image/png"]
            )

        # -------------------------------------------------
        # JPEG image
        # -------------------------------------------------

        elif "image/jpeg" in data:

            add_output_image(
                content,
                data["image/jpeg"]
            )


def render_code(
    content,
    block,
    styles
):

    language = block["language"]

    # Show the language if it is available
    if language:

        content.append(
            Paragraph(
                language.upper(),
                styles["code_language"]
            )
        )

    add_code_box(
        content,
        block["content"],
        styles
    )
