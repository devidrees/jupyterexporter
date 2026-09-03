import sys
from exporter.pdf.document import create_pdf


def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("python main.py notebook.ipynb")
        sys.exit(1)

    notebook_file = sys.argv[1]
    pdf_file = notebook_file[:-6] + ".pdf"

    create_pdf(notebook_file, pdf_file)
    print("PDF created:", pdf_file)


if __name__ == "__main__":
    main()
