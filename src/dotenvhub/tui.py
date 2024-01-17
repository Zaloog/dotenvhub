from pathlib import Path

from textual import log, on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.reactive import var
from textual.screen import ModalScreen
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

from .config import cfg
from .constants import ENV_FILE_DIR_PATH, SHELLS
from .utils import (
    copy_path_to_clipboard,
    create_copy_in_cwd,
    create_shell_export_str,
    get_env_content,
    update_file_tree,
    write_to_file,
)

# Fragen
# Do Updates happen in Displayed UI based on File System Changes
# Shell Auto Detection


class EnvFileSelector(VerticalScroll):
    def compose(self):
        for dirpath, filenames in self.app.file_tree.items():
            if dirpath == ".":
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
                    id=dirpath,
                    initial_index=None,
                )
                folder_colabs = Collapsible(
                    folder_list,
                    title=dirpath,
                    collapsed_symbol=":file_folder:",
                    expanded_symbol=":open_file_folder:",
                )
                yield folder_colabs


class FilePreviewer(TextArea):
    ...


class InteractionPanel(Container):
    def compose(self):
        yield Button(
            "Create Shell String",
            id="btn-shell-export",
            disabled=True,
            variant="primary",
        )
        yield Button(
            "Export File to current dir",
            id="btn-file-export",
            disabled=True,
            variant="primary",
        )
        yield Button(
            "Copy Path to Clipboard",
            id="btn-copy-path",
            disabled=True,
            variant="primary",
        )
        with Vertical(id="interaction-shell-select"):
            yield Label("Select your Shell")
            yield Button(label=f"{cfg.shell}", id="btn-shell-select", variant="primary")
        with Vertical(id="interaction-export-name"):
            yield Label("Export filename")
            yield Input(
                value=".env",
                placeholder="env file name for export",
                id="export-env-name",
            )
        yield Button(
            "New Env File", id="btn-new-file", disabled=False, variant="success"
        )
        yield Button(
            "Edit Env File", id="btn-edit-file", disabled=True, variant="warning"
        )
        yield Button(
            "Save Env File", id="btn-save-file", disabled=True, variant="success"
        )


class ModalShellSelector(ModalScreen):
    def compose(self) -> ComposeResult:
        shell_buttons = [
            Button(label=shell, id=shell, variant="primary") for shell in SHELLS
        ]
        for btn in shell_buttons:
            btn.can_focus = False
        yield Vertical(
            Label("Which Shell are you using?"),
            *shell_buttons,
            id="modal-shell-vert",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.pop_screen()
        selected_shell = event.button.id
        self.app.shell_in_use = selected_shell
        cfg.shell = self.app.shell_in_use

        shell_button = self.app.query_one("#btn-shell-select")
        shell_button.label = self.app.shell_in_use


class ModalSaveScreen(ModalScreen):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Label(":page_facing_up: Enter File Name"),
            Input(
                placeholder="New File Name", id="inp-new-file-name", valid_empty=False
            ),
            Label(":file_folder: Enter Folder Name"),
            Input(
                placeholder="Enter Folder Name or leave empty", id="inp-new-folder-name"
            ),
            Button("Save"),
            id="modal-save-vert",
        )

    @on(Button.Pressed)
    def save_new_file(self) -> None:
        self.app.pop_screen()

        folder_file = "/".join(
            inp.value for inp in self.query(Input)[::-1] if inp.value
        )
        new_path = ENV_FILE_DIR_PATH / folder_file
        write_to_file(path=new_path, content=self.app.text_to_display)


class DotEnvHub(App):
    CSS_PATH = Path("assets/tui.css")

    file_to_show = var("")
    file_to_show_path = var("")
    text_to_display = var("")
    file_tree = var(update_file_tree())

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        with Container(id="app-grid"):
            file_selector = VerticalScroll(id="file-selector")
            file_selector.border_title = "Select your .env File"
            with file_selector:
                yield EnvFileSelector()

            file_previewer = Horizontal(id="file-preview")
            file_previewer.border_title = "No Env File Selected"
            with file_previewer:
                yield FilePreviewer(id="text-preview")

            file_interaction = InteractionPanel(id="interaction")
            file_interaction.border_title = "What do you want to do?"
            yield file_interaction

    # Interactions

    # File Selection
    @on(ListView.Selected)
    def get_preview_file_path(self, event: ListView.Selected):
        self.file_to_show = event.list_view.highlighted_child.id

        if event.list_view.id:
            folder = Path(event.list_view.id)
            self.file_to_show_path = (
                ENV_FILE_DIR_PATH / folder / Path(self.file_to_show)
            )
            self.query_one(
                "#file-preview"
            ).border_title = f"{folder} / {self.file_to_show}"
        else:
            self.file_to_show_path = ENV_FILE_DIR_PATH / Path(self.file_to_show)
            self.query_one("#file-preview").border_title = self.file_to_show

    @on(ListView.Selected)
    def reset_highlights(self, event: ListView.Selected):
        for views in self.query(ListView):
            if views.highlighted_child:
                if views.highlighted_child.id != event.list_view.highlighted_child.id:
                    views.index = None

    @on(ListView.Selected)
    def enable_buttons(self):
        self.query_one("#btn-shell-export").disabled = False
        self.query_one("#btn-file-export").disabled = False
        self.query_one("#btn-copy-path").disabled = False

        self.query_one("#btn-new-file").disabled = False
        self.query_one("#btn-save-file").disabled = True
        self.query_one("#btn-edit-file").disabled = False

    @on(ListView.Selected)
    def update_preview_text(self):
        self.text_to_display = get_env_content(filepath=self.file_to_show_path)

        text_widget = self.query_one(TextArea)
        text_widget.text = self.text_to_display
        text_widget.action_cursor_page_down()
        text_widget.disabled = True

    # Export Interactions
    @on(Button.Pressed, "#btn-copy-path")
    def copy_env_path(self):
        copy_path_to_clipboard(path=self.file_to_show_path)
        log("copied file path to clipboard")

    @on(Button.Pressed, "#btn-file-export")
    def export_env_file(self):
        export_filename = self.query_one(Input).value
        create_copy_in_cwd(filename=export_filename, filepath=self.file_to_show_path)

    @on(Button.Pressed, "#btn-shell-export")
    def export_env_str_shell(self):
        create_shell_export_str(shell=cfg.shell, env_content=self.text_to_display)

    # Shell Select Interactions
    @on(Button.Pressed, "#btn-shell-select")
    def pop_modal_shell(self):
        self.push_screen(ModalShellSelector())

    # Env File Interactions
    @on(Button.Pressed, "#btn-new-file")
    def new_file(self, event: Button.Pressed):
        self.file_to_show = ""
        self.file_to_show_path = ""

        text_widget = self.query_one(TextArea)
        text_widget.text = ""
        text_widget.disabled = False
        text_widget.focus()

        event.button.disabled = True
        self.query_one("#btn-edit-file").disabled = True
        self.query_one("#btn-save-file").disabled = False

        self.query_one("#file-preview").border_title = "Creating New .Env File ..."

        for views in self.query(ListView):
            if views.highlighted_child:
                views.index = None

    @on(Button.Pressed, "#btn-edit-file")
    def edit_file(self, event: Button.Pressed):
        text_widget = self.query_one(TextArea)
        text_widget.disabled = False
        text_widget.focus()

        save_button = self.query_one("#btn-save-file")
        save_button.disabled = False
        event.button.disabled = True

        # log(self.file_tree)
        # self.file_tree = update_file_tree()
        # log(self.file_tree)
        # self.query_one(EnvFileSelector).compose()

    @on(Button.Pressed, "#btn-save-file")
    def save_file(self, event: Button.Pressed):
        text_widget = self.query_one(TextArea)
        self.text_to_display = text_widget.text
        text_widget.disabled = True

        event.button.disabled = True
        self.query_one("#btn-edit-file").disabled = False

        if self.file_to_show:
            write_to_file(
                path=Path(self.file_to_show_path), content=self.text_to_display
            )
        else:
            self.push_screen(ModalSaveScreen())


myapp = DotEnvHub()
