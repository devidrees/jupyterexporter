# Jupyter Exporter — Refactored

This is the first structural refactor of the working notebook-to-PDF converter.

## Run

From this folder:

```text
python main.py test_nb.ipynb
```

## Structure

- `main.py` — command-line entry point
- `exporter/notebook.py` — notebook loading and language detection
- `exporter/parser/markdown_parser.py` — Markdown parsing and inline formatting
- `exporter/renderers/markdown.py` — ReportLab rendering for Markdown, code, tables, lists and images
- `exporter/pdf/document.py` — PDF document orchestration and styles

The HTML rendering experiment is intentionally not included. HTML inside Markdown remains plain text, matching the stable milestone.
