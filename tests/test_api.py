import pytest
from pathlib import Path

from jupyterexporter import export_notebook


def test_export_notebook(tmp_path):
    notebook = Path("test_nb.ipynb")
    output = tmp_path / "output.pdf"

    result = export_notebook(notebook, output)

    assert result == f"The generated pdf file is at: {output}"
    assert output.exists()


def test_missing_notebook():
    with pytest.raises(FileNotFoundError):
        export_notebook("does_not_exist.ipynb")


def test_invalid_input_extension(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("not a notebook")

    with pytest.raises(ValueError):
        export_notebook(file)


def test_invalid_output_extension():
    with pytest.raises(ValueError):
        export_notebook("test_nb.ipynb", "output.jpg")