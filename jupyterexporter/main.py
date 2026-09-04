import argparse
import sys

from jupyterexporter import export_notebook


# this function will get our terminal commands working
# e.g. jupyterexporter test_nb.ipynb -o lesson.pdf
def main():
    parser = argparse.ArgumentParser(
        description = "Export a Jupyter Notebook to PDF."
    )

    # add argument 1 : notebook path
    parser.add_argument(
        "notebook",
        help = "Path to the Jupyter Notebook (.ipynb)"
    )

    # add argument 2 : output path
    parser.add_argument(
        "-o",
        "--output",
        help = "Output PDF path (.pdf)"
    )

    args = parser.parse_args()

    # implement arguments into export_notebook to get output
    try:
        output_path = export_notebook(
            args.notebook,
            args.output
        )
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")

        sys.exit(1)

    print("PDF created successfully:", output_path)


if __name__ == "__main__":
    main()