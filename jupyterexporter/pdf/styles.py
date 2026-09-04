# following the single responsibility principle we separated out the styles as a separate file

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def create_styles():
    """
    Create and return all ReportLab styles used by the jupyterexporter.

    Keeping styles in their own module means the PDF document
    orchestration code does not need to know how individual
    styles are configured.
    """

    # Start with ReportLab's standard styles.
    base = getSampleStyleSheet()

    styles = {}

    # ------------------------------------------------------------
    # Normal Markdown text
    # ------------------------------------------------------------

    styles["text"] = ParagraphStyle(
        "text",
        parent=base["BodyText"],
        fontSize=10,
        leading=14,
        spaceAfter=6,
    )

    # ------------------------------------------------------------
    # Headings
    # ------------------------------------------------------------

    styles["h1"] = ParagraphStyle(
        "heading1",
        parent=base["Heading1"],
        fontSize=22,
        leading=26,
        spaceAfter=10,
    )

    styles["h2"] = ParagraphStyle(
        "heading2",
        parent=base["Heading2"],
        fontSize=18,
        leading=22,
        spaceAfter=8,
    )

    styles["h3"] = ParagraphStyle(
        "heading3",
        parent=base["Heading3"],
        fontSize=15,
        leading=19,
        spaceAfter=7,
    )

    styles["h4"] = ParagraphStyle(
        "heading4",
        parent=styles["text"],
        fontSize=13,
        leading=17,
        spaceAfter=6,
    )

    styles["h5"] = ParagraphStyle(
        "heading5",
        parent=styles["text"],
        fontSize=11.5,
        leading=15,
        spaceAfter=5,
    )

    styles["h6"] = ParagraphStyle(
        "heading6",
        parent=styles["text"],
        fontSize=10,
        leading=14,
        spaceAfter=4,
    )

    # ------------------------------------------------------------
    # Lists
    # ------------------------------------------------------------

    styles["bullet"] = ParagraphStyle(
        "bullet",
        parent=styles["text"],
        leftIndent=14,
        firstLineIndent=-8,
    )

    # ------------------------------------------------------------
    # Block quotes
    # ------------------------------------------------------------

    styles["quote"] = ParagraphStyle(
        "quote",
        parent=styles["text"],
        leftIndent=20,
        rightIndent=10,
        spaceBefore=6,
        spaceAfter=6,
    )

    # ------------------------------------------------------------
    # Code
    # ------------------------------------------------------------

    styles["code"] = ParagraphStyle(
        "code",
        parent=base["Code"],
        fontSize=8,
        leading=10,
    )

    styles["code_label"] = ParagraphStyle(
        "code_label",
        parent=styles["text"],
        fontSize=8,
        leading=10,
        spaceAfter=2,
    )

    # Some existing renderer code uses this older name.
    # Keep it as an alias so both names refer to the same style.
    styles["code_language"] = styles["code_label"]

    # ------------------------------------------------------------
    # Tables
    # ------------------------------------------------------------

    styles["table_text"] = ParagraphStyle(
        "table_text",
        parent=styles["text"],
        fontSize=8,
        leading=10,
        spaceAfter=0,
    )

    # ------------------------------------------------------------
    # Raw / literal text
    # ------------------------------------------------------------

    styles["raw_text"] = ParagraphStyle(
        "raw_text",
        parent=base["Code"],
        fontName="Courier",
        fontSize=8,
        leading=10,
        spaceBefore=4,
        spaceAfter=6,
    )

    return styles