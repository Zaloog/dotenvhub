from textual.containers import Horizontal
from textual.widgets import TextArea


class FilePreviewer(Horizontal):
    def compose(self):
        yield TextArea(id="text-preview")
