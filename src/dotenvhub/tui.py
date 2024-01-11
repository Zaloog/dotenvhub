from pathlib import Path
from typing import Iterable

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import (
    Button,
    Collapsible,
    DirectoryTree,
    Footer,
    Header,
    Input,
    Label,
    ListItem,
    Static,
    TextArea,
)

# Fragen
# Do Updates happen in Displayed UI based on File System Changes
# Shell Auto Detection


class FilteredDirectoryTree(DirectoryTree):
    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        return [path for path in paths if not path.name.startswith(".")]


class DotEnvHub(App):
    CSS_PATH = "./assets/tui.css"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        with Container(id="app-grid"):
            with VerticalScroll(id="left-pane"):
                yield FilteredDirectoryTree(".")
                yield Collapsible(
                    DirectoryTree("."),
                    Static("Test"),
                    Static("Test"),
                    title="AWESOME COllapsible with many children",
                )
                yield Collapsible(
                    ListItem(Label("Test")),
                    ListItem(Label("Test")),
                    title="AWESOME COllapsible with many children",
                )
            with Horizontal(id="file-preview"):
                yield TextArea()
            with Container(id="interaction"):
                yield Button("[b]Create Shell String[/]", variant="warning")
                yield Button("Export File to current dir")
                yield Button("Copy Path to Clipboard")
                yield Input(placeholder="env name", id="bottom-right-final")


myapp = DotEnvHub()
