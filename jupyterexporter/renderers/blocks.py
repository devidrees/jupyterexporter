#  headings     paragraphs     lists     quotes     horizontal rules    raw text

from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    Spacer,
    Preformatted,
    Table,
    TableStyle,
)
from reportlab.lib.styles import ParagraphStyle

from ..parser.markdown_parser import format_markdown


def render_heading(
    content,
    block,
    styles
):

    level = block["level"]

    content.append(
        Paragraph(
            format_markdown(
                block["content"]
            ),
            styles[f"h{level}"]
        )
    )


def render_paragraph(
    content,
    block,
    styles
):

    content.append(
        Paragraph(
            format_markdown(
                block["content"]
            ),
            styles["text"]
        )
    )


def render_list(
    content,
    block,
    styles
):

    for item in block["items"]:

        level = item["level"]

        # Increase indentation for nested items
        indentation = level * 8 * mm

        # Create a style specifically for this level
        list_style = ParagraphStyle(
            f"ListLevel{level}",
            parent=styles["text"],
            leftIndent=indentation,
        )

        # Decide which marker to display
        if item["kind"] == "bullet":

            marker = "•"

        else:

            marker = f"{item['number']}."

        content.append(
            Paragraph(
                marker
                + " "
                + format_markdown(
                    item["content"]
                ),
                list_style
            )
        )


def render_quote(
    content,
    block,
    styles
):

    content.append(
        Paragraph(
            format_markdown(
                block["content"]
            ),
            styles["quote"]
        )
    )


def render_horizontal_rule(
    content,
    block,
    styles
):

    # A small table is used as a simple horizontal line.
    rule = Table(
        [[""]],
        colWidths=[170 * mm],
        rowHeights=[0.5 * mm]
    )

    rule.setStyle(
        TableStyle([
            (
                "LINEBELOW",
                (0, 0),
                (-1, -1),
                0.7,
                colors.grey
            ),
        ])
    )

    content.append(
        Spacer(1, 5)
    )

    content.append(
        rule
    )

    content.append(
        Spacer(1, 8)
    )


def render_raw_text(
    content,
    block,
    styles
):

    content.append(
        Preformatted(
            block["content"],
            styles["raw_text"]
        )
    )

    content.append(
        Spacer(1, 8)
    )