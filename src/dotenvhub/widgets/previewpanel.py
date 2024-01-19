from textual import on
from textual.containers import Horizontal
from textual.widgets import TextArea


class FilePreviewer(Horizontal):
    def compose(self):
        yield TextArea(id="text-preview")

    @on(TextArea.Changed)
    def disable_buttons(self):
        save_button = self.app.query_one("#btn-save-file")
        save_button.disabled = False
