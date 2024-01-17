from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label

from ..config import cfg
from ..constants import ENV_FILE_DIR_PATH, SHELLS
from ..utils import update_file_tree, write_to_file
from .filepanel import EnvFileSelector


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

    @on(Button.Pressed)
    def pop_up_shell_select(self, event: Button.Pressed) -> None:
        self.app.pop_screen()
        selected_shell = event.button.id
        self.app.current_shell = selected_shell
        cfg.shell = self.app.current_shell

        shell_button = self.app.query_one("#btn-shell-select")
        shell_button.label = self.app.current_shell


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
        write_to_file(path=new_path, content=self.app.current_content)

        self.app.file_tree = update_file_tree()

        self.app.query_one(EnvFileSelector).remove()
        self.app.query_one("#app-grid").mount(
            EnvFileSelector(id="file-selector"), before="#file-preview"
        )
