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
from .utils import copy_path_to_clipboard, create_copy_in_cwd, get_env_content

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
                general_list = ListView(
                    *[
                        ListItem(Label(f":page_facing_up: {file}"), id=file)
                        for file in filenames
                    ],
                    initial_index=None,
                )
                yield general_list
            else:
                folder_list = ListView(
                    *[
                        ListItem(Label(f":page_facing_up: {file}"), id=file)
                        for file in filenames
                    ],
                    id=str(dirpath),
                    initial_index=None,
                )
                folder_colabs = Collapsible(
                    folder_list,
                    title=f"{dirpath}",
                    collapsed_symbol=":file_folder:",
                    expanded_symbol=":open_file_folder:",
                )
                yield folder_colabs


class FilePreviewer(TextArea):
    pass


class InteractionPanel(Container):
    def compose(self):
        yield Button.warning("Create Shell String", id="shell_export_btn")
        yield Button.warning("Export File to current dir", id="export_btn")
        yield Button.warning("Copy Path to Clipboard", id="clipboard_path_btn")
        yield Label("export filename")
        yield Input(
            value=".env", placeholder="env file name for export", id="export-env-name"
        )


class DotEnvHub(App):
    CSS_PATH = "./assets/tui.css"

    file_to_show = var("")
    file_to_show_path = var("")
    text_to_display = var("")

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        with Container(id="app-grid"):
            with VerticalScroll(id="file-selector"):
                yield EnvFileSelector()

            with Horizontal(id="file-preview"):
                # Add File Name Display
                fp = FilePreviewer(id="text-preview")
                fp.border_title = self.file_to_show_path
                yield fp

            yield InteractionPanel(id="interaction")

    @on(ListView.Selected)
    def preview_file(self, event: ListView.Selected):
        self.file_to_show = Path(event.list_view.highlighted_child.id)
        if event.list_view.id:
            folder = Path(event.list_view.id)
            self.file_to_show_path = ENV_FILE_DIR_PATH / folder / self.file_to_show
        else:
            self.file_to_show_path = ENV_FILE_DIR_PATH / self.file_to_show
        log(self.file_to_show_path)

    @on(ListView.Selected)
    def update_preview_text(self):
        self.text_to_display = get_env_content(filepath=self.file_to_show_path)

        text_widget = self.query_one(TextArea)
        text_widget.text = self.text_to_display
        text_widget.disabled = True
        log(self.text_to_display)

    @on(Button.Pressed, "#clipboard_path_btn")
    def copy_env_path(self):
        copy_path_to_clipboard(path=self.file_to_show_path)
        log("copied file path to clipboard")

    @on(Button.Pressed, "#export_btn")
    def export_env_file(self):
        export_filename = self.query_one(Input).value
        create_copy_in_cwd(filename=export_filename, filepath=self.file_to_show_path)
        log("created Export file")


myapp = DotEnvHub()
