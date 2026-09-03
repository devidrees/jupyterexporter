from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors


def add_table(content, rows, styles):

    """
    Render a Markdown table as a ReportLab Table.

    The Markdown parser is responsible for understanding
    Markdown table syntax.

    This function is responsible only for converting the
    already-parsed table into a PDF table.
    """

    table_data = []

    for row_index, row in enumerate(rows):

        table_row = []

        for cell in row:

            # Convert each cell into a ReportLab Paragraph
            # so Markdown formatting inside table cells
            # can still be rendered.
            table_row.append(
                Paragraph(
                    cell,
                    styles["table_text"],
                )
            )

        table_data.append(table_row)

    if not table_data:
        return

    table = Table(
        table_data,
        repeatRows=1,
        hAlign="LEFT",
    )

    table.setStyle(
        TableStyle(
            [
                # Outer border.
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),

                # Lines between cells.
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.25,
                    colors.lightgrey,
                ),

                # Header row.
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#eeeeee"),
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),

                # Cell padding.
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    4,
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    4,
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
            ]
        )
    )

    content.append(table)


def render_table(
    content,
    block,
    styles
):
    """
    Render a parsed Markdown table.
    """

    add_table(
        content,
        block["rows"],
        styles
    )    