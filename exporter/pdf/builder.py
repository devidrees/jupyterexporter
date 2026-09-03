# Reportlab document configurations 


from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate


class PDFBuilder:
    """
    Responsible for creating and building the ReportLab PDF document.

    This class handles PDF-level configuration only.
    It does not know anything about Jupyter notebooks or Markdown.
    """

    def __init__(self, filename):
        self.filename = filename

    def create_document(self):
        """
        Create and return the configured ReportLab document.
        """

        return SimpleDocTemplate(
            self.filename,
            pagesize=A4,
            rightMargin=20 * mm,
            leftMargin=20 * mm,
            topMargin=20 * mm,
            bottomMargin=20 * mm,
        )

    def build(self, content):
        """
        Build the PDF from the supplied ReportLab flowables.
        """

        pdf = self.create_document()
        pdf.build(content)