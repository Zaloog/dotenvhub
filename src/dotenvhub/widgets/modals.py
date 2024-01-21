from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.validation import Regex
from textual.widgets import Button, Input, Label, TextArea

from ..config import cfg
from ..constants import ENV_FILE_DIR_PATH, SHELLS
from ..utils import update_file_tree, write_to_file
from .filepanel import EnvFileSelector


class ModalShellSelector(ModalScreen):
    CSS_PATH = Path("../assets/modal_shell.css")

    def compose(self) -> ComposeResult:
        shell_buttons = [
            Button(label=shell, id=shell, variant="primary", classes="shell")
            for shell in SHELLS
        ]
        for btn in shell_buttons:
            btn.can_focus = False
        yield Vertical(
            Label("Which Shell are you using?"),
            *shell_buttons,
            Button("Cancel", id="btn-modal-cancel"),
            id="modal-shell-vert",
        )

    @on(Button.Pressed, "#btn-modal-cancel")
    def close_window(self) -> None:
        self.dismiss()

    @on(Button.Pressed, ".shell")
    def pop_up_shell_select(self, event: Button.Pressed) -> None:
        self.dismiss()
        selected_shell = event.button.id
        self.app.current_shell = selected_shell
        cfg.shell = self.app.current_shell

        self.app.query_one("#btn-shell-select").label = self.app.current_shell


class ModalSaveScreen(ModalScreen):
    CSS_PATH = Path("../assets/modal_save.css")
    preview = reactive(":page_facing_up: Enter File Name")

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("How to save file: e.g. FOLDER/FILE"),
            Input(
                placeholder="New File Name",
                id="inp-new-file-name",
                valid_empty=False,
                validators=[Regex("^[a-zA-Z0-9_.]*(/[a-zA-Z0-9_.]*)?$")],
                validate_on=["changed", "submitted"],
            ),
            Label(self.preview, id="lbl-new-file-name"),
            Button("Save", id="btn-modal-save"),
            Button("Cancel", id="btn-modal-cancel"),
            id="modal-save-vert",
        )

    @on(Input.Submitted)
    def press_button(self):
        self.query_one("#btn-modal-save", Button).press()

    @on(Button.Pressed, "#btn-modal-cancel")
    def close_window(self) -> None:
        self.dismiss()
        self.app.query_one(TextArea).disabled = False
        self.app.query_one(TextArea).focus()

    @on(Button.Pressed, "#btn-modal-save")
    def save_new_file(self) -> None:
        self.dismiss()

        new_path = ENV_FILE_DIR_PATH / self.query_one(Input).value
        write_to_file(path=new_path, content=self.app.current_content)

        self.app.file_tree = update_file_tree()

        self.app.query_one(EnvFileSelector).remove()
        self.app.query_one("#app-grid").mount(
            EnvFileSelector(id="file-selector"), before="#file-preview"
        )

    @on(Input.Changed, "#inp-new-file-name")
    def format_name(self, event: Input.Changed):
        text = event.input.value or event.input.placeholder
        if "/" not in text:
            preview_name = f":page_facing_up: {text}"
        elif len(text.split("/")) == 2:
            folder, file = [el.strip() for el in text.split("/")]
            preview_name = f":file_folder: {folder} / :page_facing_up: {file}"
        else:
            preview_name = ":cross_mark: Enter a valid Folder/File Name"

        self.preview = preview_name

        if self.query_one(Input).is_valid:
            self.query_one("#btn-modal-save", Button).disabled = False
        else:
            self.query_one("#btn-modal-save", Button).disabled = True

        self.query_one("#lbl-new-file-name").remove()
        self.mount(
            Label(self.preview, id="lbl-new-file-name"), after="#inp-new-file-name"
        )
