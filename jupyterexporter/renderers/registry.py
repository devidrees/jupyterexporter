"""
Renderer registry.

This module maps parsed Markdown block types to the function
responsible for rendering each block.
"""

from .blocks import (
    render_heading,
    render_paragraph,
    render_list,
    render_quote,
    render_horizontal_rule,
    render_raw_text,
)

from .images import (
    render_image,
    render_external_image,
)

from .code import render_code

from .tables import render_table


# Maps the block type produced by the Markdown parser
# to the renderer responsible for that block.
BLOCK_RENDERERS = {

    "heading": render_heading,

    "paragraph": render_paragraph,

    "list": render_list,

    "quote": render_quote,

    "code": render_code,

    "table": render_table,

    "horizontal_rule": render_horizontal_rule,

    "image": render_image,

    "external_image": render_external_image,

    "raw_text": render_raw_text,
}