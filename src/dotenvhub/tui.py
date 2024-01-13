import os
from pathlib import Path

from textual import log, on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
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

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        with Container(id="app-grid"):
            with VerticalScroll(id="file-selector"):
                yield EnvFileSelector()

            with Horizontal(id="file-preview"):
                yield FilePreviewer()

            with Container(id="interaction"):
                yield Button.warning("[b]Create Shell String[/]")
                yield Button.warning("Export File to current dir")
                yield Button.warning("Copy Path to Clipboard")
                yield Label("export filename")
                yield Input(placeholder="env name", id="bottom-right-final")

    @on(ListView.Selected)
    def preview_file(self, event: ListView.Selected):
        file = event.list_view.highlighted_child
        folder = event.list_view.id
        print(file, folder)

        pass


myapp = DotEnvHub()
