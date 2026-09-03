# create pdf
# load nb, create pdf builder, create styles, create nb renderer, 
# build pdf

import os
from ..notebook import NotebookLoader
from ..parser.markdown_parser import parse_markdown, format_markdown
from ..renderers.notebook import NotebookRenderer
from .styles import create_styles
from .builder import PDFBuilder



def create_pdf(notebook_file, pdf_file):
    # Read the notebook JSON.
    # Load the notebook through the Notebook layer.
    loader = NotebookLoader()
    notebook = loader.load(notebook_file)

    # Get notebook-level information through the Notebook object.
    notebook_language = notebook.language
    notebook_dir = os.path.dirname(os.path.abspath(notebook_file))

    # PDFBuilder is responsible for PDF-level configuration.
    pdf_builder = PDFBuilder(pdf_file)

    # Create all styles required by the PDF renderers.
    styles = create_styles()

    content = []

    # NotebookRenderer is responsible for deciding how each
    # notebook cell should be rendered.
    renderer = NotebookRenderer(
        styles=styles,
        notebook_language=notebook_language,
        notebook_dir=notebook_dir,
    )

    renderer.render(
        notebook,
        content,
    )

    # Build the final PDF.
    pdf_builder.build(content)
