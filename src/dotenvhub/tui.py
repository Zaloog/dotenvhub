from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.css.query import NoMatches
from textual.reactive import var
from textual.widgets import Footer, Header, Button, ListView
from textual_jumper import Jumper

from dotenvhub.config import DotEnvHubConfig
from dotenvhub.utils import update_file_tree
from dotenvhub.widgets.filepanel import EnvFileSelector
from dotenvhub.widgets.interactionpanel import InteractionPanel
from dotenvhub.widgets.previewpanel import FilePreviewer
from dotenvhub.constants import ENV_FILE_DIR_PATH, CONFIG_FILE_PATH


class DotEnvHub(App):
    CSS_PATH = Path("assets/tui.tcss")

    cfg: DotEnvHubConfig
    file_to_show = var("")
    file_to_show_path = var("")
    file_tree = var({})
    current_content = var("")
    content_dict = var({})
    current_shell = var("")

    BINDINGS = [
        Binding(
            key="ctrl+o",
            action="show_jumper",
            description="Jump",
            show=True,
            priority=True,
        ),
    ]

    def __init__(
        self, config_path: Path = CONFIG_FILE_PATH, data_path: Path = ENV_FILE_DIR_PATH
    ):
        self.config_path = config_path
        self.data_path = data_path
        super().__init__()
        self.cfg = DotEnvHubConfig(path=config_path)
        self.current_shell = self.cfg.shell

    def compose(self) -> ComposeResult:
        self.file_tree = update_file_tree(path=self.data_path)

        yield Header()
        yield Footer()
        yield Jumper()

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

    def on_ready(self):
        try:
            self.query_one(ListView).focus()
        except NoMatches:
            self.query_one("#btn-new-file", Button).focus()

    def action_show_jumper(self) -> None:
        self.query_one(Jumper).show()

    async def reset_values(self):
        self.file_to_show = ""
        self.file_to_show_path = ""
        self.current_content = ""
        self.content_dict = {}
        await self.file_previewer.new_file()
        self.file_previewer.border_title = "Select file or Create a new one"
