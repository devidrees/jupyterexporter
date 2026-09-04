# Jupyter Exporter
Export Jupyter Notebooks (.ipynb) to PDF.

A lightweight Python project for exporting Jupyter notebooks into static, shareable formats for documentation, publishing, and automation.

`jupyterexporter` provides a simple Python API and command-line interface (CLI) for converting Jupyter Notebook files into PDF documents.

---

## Overview

Jupyter notebooks are excellent for exploratory work, experiments, and data analysis, but they are not always ideal for distribution or long-term documentation. Jupyter Exporter provides a clean, project-oriented workflow to convert notebook content into exportable output while keeping the original notebook source intact.

This repository is designed to support open-source development and practical notebook publishing workflows.

---

## Features

- Convert Jupyter Notebooks to PDF
- Simple command-line interface
- Python API for use in scripts and applications
- Specify a custom output path
- Supports relative and absolute file paths
- Clear validation and error messages
- Lightweight and Fast - Jupyter itself is not required to perform the conversion

---

## Project goals

- Keep exports reproducible
- Preserve the notebook source as the canonical artifact
- Minimize dependency on interactive notebook environments for publishing
- Make notebook-based content easier to share and review
- Maintain a clean, open-source repository structure

## Getting started

### Prerequisites

Before using the project, make sure you have:

- Python 3.9 or newer
- Jupyter or JupyterLab is not really needed but good to have if you do. 

## Installation

Install `jupyterexporter` using pip:

```bash
pip install jupyterexporter
```

After installation, the `jupyterexporter` command will be available in your terminal.

---

## Command-Line Usage

### 1. Basic Usage

Convert a notebook to PDF:

```bash
jupyterexporter notebook_name.ipynb
```
Make sure the notebook(.ipynb) exists in the terminal folder.
The PDF will be created in the same directory.


### 2. Specify an Output File Name

Use the flag `-o` or `--output` to specify the output name of the PDF:

```bash
jupyterexporter notebook.ipynb -o lesson.pdf
``` 


### 3. Specify an Output Path

You can also provide a complete input or output path:

```bash
jupyterexporter "C:\Users\YourName\Documents\notebook.ipynb" -o "C:\Users\YourName\Documents\lesson.pdf"
```

On Linux or macOS:

```bash
jupyterexporter "/home/yourname/Documents/notebook.ipynb" -o "/home/yourname/Documents/lesson.pdf"
```

### Help

Display the available command-line options:

```bash
jupyterexporter --help
```

---

## Python API

`jupyterexporter` can also be used directly from Python.

### 1. Basic Usage

```python
from jupyterexporter import export_notebook

export_notebook("notebook.ipynb")
```

This creates the pdf file in the same directory as the notebook.

### 2. Specify an Output File

```python
from jupyterexporter import export_notebook

output = export_notebook(
    "notebook.ipynb",
    "lesson.pdf"
)

print(output)
```
The function returns the path of the generated PDF.

### 3. Using Full Paths

Both the input and output paths can be absolute paths:

```python
from jupyterexporter import export_notebook

output = export_notebook(
    r"C:\Projects\Notebooks\analysis.ipynb",
    r"C:\Projects\PDFs\analysis.pdf"
)

print(output)
```

---

## Input and Output

### Input

The input file must be a Jupyter Notebook with the `.ipynb` extension for example: `text analysis.ipynb`

### Output

The output file must use the `.pdf` extension for example: `analysis.pdf` 

If an output file with another extension is supplied, the exporter will raise an error.

---

## Error Handling

The Python API provides clear exceptions for invalid input.

If the notebook does not exist, a `FileNotFoundError` is raised.

If the input is not a Jupyter Notebook, a `ValueError` is raised.

If the output is not a PDF, a `ValueError` is raised.

```python
export_notebook(
    "notebook.ipynb",
    "output.jpg"
)
```

The command-line interface catches these expected errors and displays a user-friendly error message.

---

## Requirements

- Python 3.10 or newer
- ReportLab

Jupyter Notebook or JupyterLab is **not currently required** to perform the conversion.

---

## Development - For Developers

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/jupyterexporter.git
cd jupyterexporter
```

### Create a Virtual Environment

Windows:

```bash
py -3.14 -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Development Dependencies

```bash
python -m pip install -e ".[dev]"
```

Then make whatever changes you want to. 

### Run Tests

```bash
pytest
```

### Build the Package

```bash
python -m build
```

The distribution files will be created in the `dist/` directory.

---

## Project Structure

The project is organized around a public Python API and command-line interface:

```text
jupyterexporter/
│
├── jupyterexporter/
│   ├── __init__.py
│   ├── main.py
│   ├── notebook.py
│   │
│   ├── parser/
│   │
│   ├── pdf/
│   │
│   └── renderers/
│
├── tests/
│   └── test_api.py
│
├── README.md
├── pyproject.toml
└── ...
```

The main public function is:

```python
from jupyterexporter import export_notebook
```

The command-line interface uses the same underlying API.

---

## Current Status

`jupyterexporter` is currently under active development.

The current release provides:

- Jupyter Notebook to PDF conversion
- Python API
- Command-line interface
- Custom output paths
- Input and output validation
- Automated tests

Additional rendering and notebook-export features are planned for future releases.

---

## License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

---

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests or validation as applicable
5. Submit a pull request with a clear description

Please keep the project professional, maintainable, and aligned with its purpose as an open-source notebook export tool.

Before submitting changes, please make sure to test your features.
Create your test functions in `test_api.py` and run the test suite:

```bash
pytest
```

---

## Roadmap

Future versions may include:

- Improved PDF rendering
- More notebook element support
- Improved image handling
- Better styling and formatting options
- Additional command-line options
- More comprehensive test coverage
- Integration with Jupyter and development environments

