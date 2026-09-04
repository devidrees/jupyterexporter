"""
Markdown orchestration.

This module is responsible for:

1. Passing Markdown source to the Markdown parser.
2. Receiving parsed blocks.
3. Finding the appropriate renderer.
4. Adding the resulting ReportLab flowables
   to the document content.
"""

from ..parser.markdown_parser import parse_markdown

from .registry import BLOCK_RENDERERS


def render_block(
    content,
    block,
    styles
):
    """
    Render a single parsed Markdown block.

    The Markdown parser determines the block type.
    The renderer registry determines which function
    should handle that block.
    """

    block_type = block["type"]

    # Look up the renderer for this block type.
    renderer = BLOCK_RENDERERS.get(
        block_type
    )

    # If no renderer exists for this block type,
    # simply skip it for now.
    if renderer is None:
        return

    # Execute the appropriate renderer.
    renderer(
        content,
        block,
        styles
    )


def add_markdown(
    content,
    source,
    styles,
    attachments=None,
    cell=None,
    notebook_dir=None
):
    """
    Parse and render an entire Markdown cell.

    The parser converts Markdown into structured blocks.
    Each block is then passed to the appropriate renderer.
    """

    blocks = parse_markdown(
        source,
        attachments,
        cell,
        notebook_dir
    )

    for block in blocks:

        render_block(
            content,
            block,
            styles
        )