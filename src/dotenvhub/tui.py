import os
from pathlib import Path

from textual import log, on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.reactive import var
from textual.widgets import (
    Button,
    Collapsible,
    Footer,
    Header,
    Input,
    Label,
    ListItem,
    ListView,
    TextArea,
)

from .constants import ENV_FILE_DIR_PATH
from .utils import copy_path_to_clipboard, get_env_content

# Fragen
# Do Updates happen in Displayed UI based on File System Changes
# Shell Auto Detection


class EnvFileSelector(VerticalScroll):
    def build_selector(self, path: Path = ENV_FILE_DIR_PATH):
        self.dir_paths = {}
        for dirpath, _, filenames in os.walk(path):
            rel_path = Path(dirpath).relative_to(path)
            log(rel_path, filenames)
            self.dir_paths[rel_path] = filenames

    def compose(self):
        self.build_selector()
        for dirpath, filenames in self.dir_paths.items():
            if dirpath == Path("."):
                yield ListView(
                    *[ListItem(Label(file), id=file) for file in filenames],
                )
            else:
                yield Collapsible(
                    ListView(
                        *[ListItem(Label(file), id=file) for file in filenames],
                        id=str(dirpath),
                    ),
                    title=dirpath,
                )


class FilePreviewer(TextArea):
    pass


class DotEnvHub(App):
    CSS_PATH = "./assets/tui.css"

    file_to_show_path = var("")
    text_to_display = var("")

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        with Container(id="app-grid"):
            with VerticalScroll(id="file-selector"):
                yield EnvFileSelector()

            with Horizontal(id="file-preview"):
                yield FilePreviewer(id="text-preview")

            with Container(id="interaction"):
                yield Button.warning("Create Shell String", id="shell_export_btn")
                yield Button.warning("Export File to current dir", id="export_btn")
                yield Button.warning("Copy Path to Clipboard", id="clipboard_path_btn")
                yield Label("export filename")
                yield Input(placeholder="env name", id="bottom-right-final")

    @on(ListView.Selected)
    def preview_file(self, event: ListView.Selected):
        file = Path(event.list_view.highlighted_child.id)
        if event.list_view.id:
            folder = Path(event.list_view.id)
            self.file_to_show_path = ENV_FILE_DIR_PATH / folder / file
        else:
            self.file_to_show_path = ENV_FILE_DIR_PATH / file
        log(self.file_to_show_path)

    @on(ListView.Selected)
    def update_preview_text(self):
        self.text_to_display = get_env_content(filepath=self.file_to_show_path)

        text_widget = self.query_one(TextArea)
        text_widget.text = self.text_to_display
        text_widget.disabled = True
        log(self.text_to_display)

    @on(Button.Pressed, "#clipboard_path_btn")
    def current_env_to_clipboard(self):
        copy_path_to_clipboard(path=self.file_to_show_path)
        log("copied file path to clipboard")


myapp = DotEnvHub()
