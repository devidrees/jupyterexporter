import json


class Notebook:
    """
    Represents a Jupyter Notebook.

    This class keeps notebook-specific information together so that
    the rest of the exporter does not need to work directly with
    the raw JSON structure.
    """

    def __init__(self, data):
        self.data = data

    @property
    def cells(self):
        """Return the notebook's cells."""
        return self.data.get("cells", [])

    @property
    def metadata(self):
        """Return the notebook metadata."""
        return self.data.get("metadata", {})

    @property
    def language(self):
        """
        Determine the programming language used by the notebook.

        Prefer language_info because it is generally more specific.
        Fall back to kernelspec if necessary.
        """

        # Prefer language_info if it exists.
        language_info = self.metadata.get("language_info", {})
        language = language_info.get("name")

        if language:
            return language

        # Fall back to kernelspec.
        kernelspec = self.metadata.get("kernelspec", {})
        language = kernelspec.get("language")

        if language:
            return language

        # No language information was found.
        return None


class NotebookLoader:
    """
    Responsible only for loading a .ipynb file.
    """

    def load(self, filename):
        """Read a notebook JSON file and return a Notebook object."""

        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        return Notebook(data)