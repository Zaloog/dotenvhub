from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.css.query import NoMatches
from textual.reactive import var
from textual.widgets import Footer, Header, Button, ListView

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
            key="ctrl+n",
            action="new_file",
            description="New File",
            show=False,
            priority=True,
        ),
        Binding(
            key="ctrl+s",
            action="save_file",
            description="Save",
            show=False,
            priority=True,
        ),
        Binding(
            key="ctrl+z",
            action="change_shell",
            description="Shell Change",
            show=False,
            priority=True,
        ),
        Binding(
            key="ctrl+e",
            action="shell_export",
            description="Shell Export",
            show=False,
            priority=True,
        ),
        Binding(
            key="ctrl+f",
            action="file_export",
            description="File Export",
            show=False,
            priority=True,
        ),
        Binding(
            key="ctrl+c",
            action="copy_path",
            description="Copy Path",
            show=False,
            priority=True,
        ),
        Binding(
            key="e", action="focus_preview", description="Focus Preview", show=False
        ),
        Binding(key="d", action="delete_file", description="File Delete", show=False),
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

    def action_new_file(self):
        self.query_one("#btn-new-file", Button).press()

    def action_save_file(self):
        self.query_one("#btn-save-file", Button).press()

    def action_change_shell(self):
        self.query_one("#btn-shell-select", Button).press()

    def action_shell_export(self):
        self.query_one("#btn-shell-export", Button).press()

    def action_file_export(self):
        self.query_one("#btn-file-export", Button).press()

    def action_copy_path(self):
        self.query_one("#btn-copy-path", Button).press()

    def action_focus_preview(self):
        try:
            # self.query_one(".active", Button).press()
            self.query(".active").first(Button).press()
        except NoMatches:
            self.notify(
                title="Edit Error",
                message="Please select a file to [red]edit[/]",
                severity="warning",
                timeout=1.5,
            )

    def action_delete_file(self):
        try:
            self.query(".active").last(Button).press()
        except NoMatches:
            self.notify(
                title="Delete Error",
                message="Please select a file to [red]delete[/]",
                severity="warning",
                timeout=1.5,
            )

    async def reset_values(self):
        self.file_to_show = ""
        self.file_to_show_path = ""
        self.current_content = ""
        self.content_dict = {}
        await self.file_previewer.new_file()
        self.file_previewer.border_title = "Select file or Create a new one"
