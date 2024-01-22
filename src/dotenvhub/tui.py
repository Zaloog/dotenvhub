from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import var
from textual.widgets import Footer, Header

from .config import cfg
from .utils import update_file_tree
from .widgets.filepanel import EnvFileSelector
from .widgets.interactionpanel import InteractionPanel
from .widgets.previewpanel import FilePreviewer


class DotEnvHub(App):
    CSS_PATH = Path("assets/tui.css")

    file_to_show = var("")
    file_to_show_path = var("")
    file_tree = var(update_file_tree())
    current_content = var("")
    current_shell = var(cfg.shell)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        with Container(id="app-grid"):
            file_selector = EnvFileSelector(id="file-selector")
            file_selector.border_title = "Select your .env File"
            yield file_selector

            file_previewer = FilePreviewer(id="file-preview")
            file_previewer.border_title = "No Env File Selected"
            yield file_previewer

            file_interaction = InteractionPanel(id="interaction")
            file_interaction.border_title = "What do you want to do?"
            yield file_interaction
