from pathlib import Path

from jupyterexporter.pdf.document import create_pdf


# main export notebook function 
def export_notebook(notebook_path, output_path=None):
    notebook_path = Path(notebook_path)

    if notebook_path.suffix.lower() != ".ipynb":
                        raise ValueError(
                            "Input file must be a Jupyter Notebook (.ipynb) file."
                        )

    if not notebook_path.exists():
        raise FileNotFoundError(
            f"Notebook not found at the given path: {notebook_path}"
        )

    if output_path is None:
        output_path = notebook_path.with_suffix(".pdf")
    
    else:
        # we need to handle here if the user gives a wrong extension
        output_path = Path(output_path) 

        if output_path.suffix.lower() != ".pdf":
                    raise ValueError(
                        "Output file must be a PDF (.pdf) file."
                    )

    create_pdf(str(notebook_path), str(output_path))

    return f"The generated pdf file is at: {output_path}"