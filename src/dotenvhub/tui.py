from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.reactive import var
from textual.widgets import Footer, Header, Button

from dotenvhub.config import cfg
from dotenvhub.utils import update_file_tree
from dotenvhub.widgets.filepanel import EnvFileSelector
from dotenvhub.widgets.interactionpanel import InteractionPanel
from dotenvhub.widgets.previewpanel import FilePreviewer


class DotEnvHub(App):
    CSS_PATH = Path("assets/tui.tcss")

    file_to_show = var("")
    file_to_show_path = var("")
    file_tree = var(update_file_tree())
    current_content = var("")
    content_dict = var({})
    current_shell = var(cfg.shell)

    BINDINGS = [
        Binding(key="ctrl+n", action="new_file", description="New File"),
        Binding(key="ctrl+s", action="save_file", description="Save"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        with Container(id="app-grid"):
            self.file_selector = EnvFileSelector(id="file-selector")
            self.file_selector.border_title = "Select your .env File"
            yield self.file_selector

            self.file_previewer = FilePreviewer(id="file-preview")
            self.file_previewer.border_title = "Select file or Create a new one"
            yield self.file_previewer

            self.file_interaction = InteractionPanel(id="interaction")
            self.file_interaction.border_title = "What do you want to do?"
            yield self.file_interaction

    def action_new_file(self):
        self.query_one("#btn-new-file", Button).press()

    def action_save_file(self):
        self.query_one("#btn-save-file", Button).press()

    def reset_values(self):
        self.file_to_show = ""
        self.file_to_show_path = ""
        self.current_content = ""
        self.content_dict = {}
