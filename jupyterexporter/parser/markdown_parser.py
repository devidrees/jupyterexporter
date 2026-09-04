import json
import re
import os
import base64
import io
import urllib.request
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Spacer, Preformatted, Table, TableStyle, Image
from reportlab.lib.styles import ParagraphStyle


def format_markdown(text):

    # -----------------------------------------------------
    # Escape characters that have a special meaning in ReportLab's Paragraph markup.
    # -----------------------------------------------------

    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")

    # -----------------------------------------------------
    # Temporarily protect inline code
    #
    # We use placeholders containing NO *, _, or other
    # Markdown formatting characters.
    # This prevents our bold/italic processing from accidentally modifying the placeholder.
    # -----------------------------------------------------

    code_parts = []

    def save_code(match):

        code_parts.append(match.group(1))

        return f"XINLCODE{len(code_parts) - 1}X"

    text = re.sub(
        r"`([^`]+)`",
        save_code,
        text
    )

    # -----------------------------------------------------
    # Temporarily protect links
    #
    # Example:
    #
    # [Google](https://google.com)
    #
    # becomes:
    #
    # XINLLINK0X
    # -----------------------------------------------------

    link_parts = []

    def save_link(match):

        label = match.group(1)
        url = match.group(2)

        link_parts.append(
            (label, url)
        )

        return f"XINLLINK{len(link_parts) - 1}X"

    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        save_link,
        text
    )

    # -----------------------------------------------------
    # Bold
    #
    # **bold text**
    # -----------------------------------------------------

    text = re.sub(
        r"\*\*(.+?)\*\*",
        r"<b>\1</b>",
        text
    )

    # Also support:
    #
    # __bold text__
    #

    text = re.sub(
        r"__(.+?)__",
        r"<b>\1</b>",
        text
    )

    # -----------------------------------------------------
    # Strikethrough
    #
    # ~~deleted text~~
    # -----------------------------------------------------

    text = re.sub(
        r"~~(.+?)~~",
        r"<strike>\1</strike>",
        text
    )

    # -----------------------------------------------------
    # Italic
    #
    # The negative lookarounds prevent the * characters
    # belonging to **bold** from being treated as italic.
    # -----------------------------------------------------

    text = re.sub(
        r"(?<!\*)\*([^*\n]+?)\*(?!\*)",
        r"<i>\1</i>",
        text
    )

    # Also support:
    #
    # _italic text_
    # -----------------------------------------------------

    text = re.sub(
        r"(?<!_)_([^_\n]+?)_(?!_)",
        r"<i>\1</i>",
        text
    )

    # -----------------------------------------------------
    # Restore links
    # -----------------------------------------------------

    for number, (label, url) in enumerate(link_parts):

        replacement = (
            f'<link href="{url}" color="blue">'
            f'{label}'
            f'</link>'
        )

        text = text.replace(
            f"XINLLINK{number}X",
            replacement
        )

    # -----------------------------------------------------
    # Restore inline code
    # -----------------------------------------------------

    for number, code in enumerate(code_parts):

        replacement = (
            f'<font name="Courier">{code}</font>'
        )

        text = text.replace(
            f"XINLCODE{number}X",
            replacement
        )

    return text


def is_table_separator(line):

    line = line.strip().strip("|")

    cells = line.split("|")

    for cell in cells:

        cell = cell.strip()

        if not re.fullmatch(
            r":?-+:?",
            cell
        ):
            return False

    return len(cells) > 0


def is_table_start(lines, index):

    # We need a current line and a following line
    if index + 1 >= len(lines):
        return False

    current = lines[index].strip()
    next_line = lines[index + 1].strip()

    # The first line must contain |
    if "|" not in current:
        return False

    # The second line must be a Markdown separator
    if not is_table_separator(next_line):
        return False

    return True


def parse_table_row(line):

    # Remove whitespace and outer | characters
    line = line.strip().strip("|")

    # Split into individual cells
    cells = line.split("|")

    # Remove surrounding whitespace
    return [
        cell.strip()
        for cell in cells
    ]


def parse_list_item(line):

    # Keep the original indentation.
    level = get_list_level(line)

    stripped = line.strip()

    # -----------------------------------------------------
    # Bullet
    #
    # - item
    # * item
    # + item
    # -----------------------------------------------------

    bullet_match = re.match(
        r"^[-*+]\s+(.+)$",
        stripped
    )

    if bullet_match:

        return {
            "kind": "bullet",
            "content": bullet_match.group(1),
            "level": level,
        }

    # -----------------------------------------------------
    # Numbered
    #
    # 1. item
    # 2. item
    #
    # Also allow:
    #
    # 1) item
    # -----------------------------------------------------

    numbered_match = re.match(
        r"^(\d+)[.)]\s+(.+)$",
        stripped
    )

    if numbered_match:

        return {
            "kind": "numbered",
            "number": int(numbered_match.group(1)),
            "content": numbered_match.group(2),
            "level": level,
        }

    return None


def is_list_item(line):

    return parse_list_item(line) is not None


def is_horizontal_rule(line):

    stripped = line.strip()

    return (
        re.fullmatch(
            r"-\s*-\s*-+",
            stripped
        )
        or
        re.fullmatch(
            r"\*\s*\*\s*\*+",
            stripped
        )
        or
        re.fullmatch(
            r"_\s*_\s*_+",
            stripped
        )
    )


def get_list_level(line):

    # Count spaces before the actual text
    leading_spaces = len(
        line
    ) - len(
        line.lstrip(" ")
    )

    # We treat every 2 spaces as one nesting level
    return leading_spaces // 2


def is_html_block(text):

    text = text.strip()

    if not text:
        return False

    # Common HTML block tags used in notebooks.
    html_tags = (
        "<div",
        "<span",
        "<p",
        "<h1",
        "<h2",
        "<h3",
        "<h4",
        "<h5",
        "<h6",
        "<table",
        "<ul",
        "<ol",
        "<li",
        "<hr",
        "<br",
    )

    return text.lower().startswith(html_tags)


def parse_markdown(
    source,
    attachments=None,
    cell=None,
    notebook_dir=None
):

    if attachments is None:
        attachments = {}

    if cell is None:
        cell = {}

    if notebook_dir is None:
        notebook_dir = os.getcwd()

    lines = source.splitlines()
    blocks = []
    index = 0

    while index < len(lines):

        # Keep the original line.
        # This is important because indentation matters
        # for nested lists.
        raw_line = lines[index]

        # A stripped version is useful for most Markdown checks.
        line = raw_line.strip()

                # -------------------------------------------------
        # HTML block
        #
        # HTML inside a Markdown cell is NOT rendered as HTML.
        #
        # We keep it as plain text so the original HTML source
        # remains visible in the PDF. We use the raw lines here
        # instead of the stripped lines so indentation is kept.
        # -------------------------------------------------

        if is_html_block(line):

            html_lines = [raw_line]
            index += 1

            # Keep collecting consecutive non-empty lines.
            # We intentionally do not try to understand HTML
            # tags or match opening/closing tags here.
            while index < len(lines):

                current_line = lines[index]

                if not current_line.strip():
                    break

                html_lines.append(current_line)
                index += 1

            blocks.append({
                "type": "raw_text",
                "content": "\n".join(html_lines)
            })

            continue

        # -------------------------------------------------
        # Ignore empty lines
        # -------------------------------------------------

        if not line:

            index += 1
            continue

        # -------------------------------------------------
        # Fenced code block
        # -------------------------------------------------

        if line.startswith("```"):

            language = line[3:].strip() or None

            code_lines = []

            index += 1

            # Collect lines until the closing ```
            while index < len(lines):

                current_line = lines[index]

                if current_line.strip().startswith("```"):
                    break

                code_lines.append(
                    current_line
                )

                index += 1

            blocks.append({
                "type": "code",
                "language": language,
                "content": "\n".join(
                    code_lines
                ),
            })

            # Skip the closing ```
            if index < len(lines):
                index += 1

            continue

        # -------------------------------------------------
        # Markdown table
        # -------------------------------------------------

        if is_table_start(
            lines,
            index
        ):

            rows = []

            # Header row
            rows.append(
                parse_table_row(
                    lines[index]
                )
            )

            # Skip header + separator
            index += 2

            # Read table rows
            while index < len(lines):

                current_line = (
                    lines[index].strip()
                )

                if "|" not in current_line:
                    break

                if is_table_separator(
                    current_line
                ):
                    break

                rows.append(
                    parse_table_row(
                        current_line
                    )
                )

                index += 1

            blocks.append({
                "type": "table",
                "rows": rows,
            })

            continue

        # -------------------------------------------------
        # Horizontal rule
        # -------------------------------------------------

        if is_horizontal_rule(line):

            blocks.append({
                "type": "horizontal_rule",
            })

            index += 1

            continue

        # -------------------------------------------------
        # Heading
        # -------------------------------------------------

        heading_match = re.match(
            r"^(#{1,6})\s+(.+)$",
            line
        )

        if heading_match:

            level = len(
                heading_match.group(1)
            )

            text = heading_match.group(2)

            blocks.append({
                "type": "heading",
                "level": level,
                "content": text,
            })

            index += 1

            continue

        # -------------------------------------------------
        # List
        # -------------------------------------------------
        #
        # Previously bullet and numbered lists were parsed
        # separately.
        #
        # Now we collect BOTH kinds into one list block.
        #
        # This means mixed lists are possible.
        # -------------------------------------------------

        if is_list_item(line):

            items = []

            while index < len(lines):

                current_line = lines[index]

                item = parse_list_item(
                    current_line
                )

                if item is None:
                    break

                items.append(item)

                index += 1

            blocks.append({
                "type": "list",
                "items": items,
            })

            continue

        # -------------------------------------------------
        # Block quote
        # -------------------------------------------------

        if line.startswith("> "):

            blocks.append({
                "type": "quote",
                "content": line[2:],
            })

            index += 1

            continue


        # -------------------------------------------------
        # image detection part
        # -------------------------------------------------
        image_match = re.fullmatch(
            r'!\[([^\]]*)\]\(data:image/([^;]+);base64,(.+)\)',
            line.strip()
        )
        
        if image_match:
        
            blocks.append({
                "type": "image",
                "data": image_match.group(3),
                "format": image_match.group(2),
            })
            index += 1
            continue

        # ---------------------------------------------------------
        # Check for a Jupyter notebook attachment
        # ---------------------------------------------------------
        #
        # Jupyter stores pasted/attached images inside the
        # Markdown cell's "attachments" metadata.
        #
        # Example Markdown:
        #
        #     ![flower.jpg](attachment:flower.jpg)
        #
        # The actual image data is stored in:
        #
        #     attachments["flower.jpg"]["image/jpeg"]
        #
        # So we don't need the original image file or internet.
        # ---------------------------------------------------------
        
        attachment_match = re.fullmatch(
            r'!\[([^\]]*)\]\(attachment:([^)]+)\)',
            line.strip()
        )
        
        if attachment_match:
        
            alt_text = attachment_match.group(1)
            attachment_name = attachment_match.group(2)
        
            attachment = attachments.get(
                attachment_name
            )
        
            if attachment:
            
                # Jupyter can store attachments as PNG, JPEG,
                # GIF, etc. We currently support the formats
                # ReportLab can use directly.
                image_data = None
        
                if "image/png" in attachment:
                
                    image_data = attachment["image/png"]
        
                elif "image/jpeg" in attachment:
                
                    image_data = attachment["image/jpeg"]
        
                if image_data:
                
                    blocks.append({
                        "type": "image",
                        "data": image_data,
                    })
        
                    index += 1
                    continue


        # ---------------------------------------------------------
        # Check for an external URL or local Markdown image
        # ---------------------------------------------------------
        #
        # Examples:
        #
        #     ![sunflower](https://example.com/sunflower.jpg)
        #
        #     ![diagram](images/diagram.png)
        #
        # We do not load the image while parsing.
        # Instead, we create a block and let the renderer
        # handle the URL/local-file lookup later.
        # ---------------------------------------------------------

        external_image_match = re.fullmatch(
            r'!\[([^\]]*)\]\(([^)]+)\)',
            line.strip()
        )

        if external_image_match:

            alt_text = external_image_match.group(1)
            image_source = external_image_match.group(2)

            blocks.append({
                "type": "external_image",
                "source": image_source,
                "alt": alt_text,
                "notebook_dir": notebook_dir,
            })

            index += 1
            continue


        # -------------------------------------------------
        # Normal paragraph
        #
        # Keep collecting lines until we reach something
        # that clearly starts a new Markdown block.
        # -------------------------------------------------

        paragraph_lines = [line]

        index += 1

        while index < len(lines):

            next_raw_line = lines[index]
            next_line = next_raw_line.strip()

            # Blank line = end of paragraph
            if not next_line:
                break

            # A new Markdown structure = end of paragraph

            if next_line.startswith("```"):
                break

            if is_table_start(
                lines,
                index
            ):
                break

            if is_horizontal_rule(
                next_line
            ):
                break

            if re.match(
                r"^(#{1,6})\s+(.+)$",
                next_line
            ):
                break

            if is_list_item(
                next_line
            ):
                break

            if next_line.startswith("> "):
                break

            # Markdown image starts a new block
            if re.fullmatch(
                r'!\[([^\]]*)\]\(([^)]+)\)',
                next_line
            ):
                break

            # Otherwise this is another line belonging
            # to the same paragraph.
            paragraph_lines.append(
                next_line
            )

            index += 1

        blocks.append({
            "type": "paragraph",
            "content": " ".join(
                paragraph_lines
            ),
        })

    return blocks
