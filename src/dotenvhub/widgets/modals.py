from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dotenvhub.tui import DotEnvHub

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.validation import Regex
from textual.widgets import Button, Input, Label

from rich.text import Text

from dotenvhub.constants import ENV_FILE_DIR_PATH, SHELLS


class ModalShellSelector(ModalScreen):
    app: "DotEnvHub"
    CSS_PATH = Path("../assets/modal_shell.tcss")
    BINDINGS = [
        Binding(key="escape", action="app.pop_screen", show=False, priority=True)
    ]

    def compose(self) -> ComposeResult:
        with Vertical(id="modal-shell-vert"):
            yield Label("Which Shell are you using?")
            for shell in SHELLS:
                yield Button(label=shell, id=shell, variant="primary", classes="shell")
            yield Button("Cancel", id="btn-modal-cancel")

    @on(Button.Pressed, "#btn-modal-cancel")
    def close_window(self) -> None:
        self.dismiss()

    @on(Button.Pressed, ".shell")
    def pop_up_shell_select(self, event: Button.Pressed) -> None:
        self.dismiss()
        selected_shell = event.button.id
        self.app.current_shell = selected_shell
        self.app.cfg.shell = self.app.current_shell

        self.app.query_one("#btn-shell-select", Button).label = self.app.current_shell
        self.notify(
            title="Shell Selected",
            message=f"Current active Shell: [green]{self.app.current_shell}[/]",
            timeout=1.5,
        )


class ModalSaveScreen(ModalScreen):
    app: "DotEnvHub"
    CSS_PATH = Path("../assets/modal_save.tcss")
    BINDINGS = [Binding(key="escape", action="close_window", show=False, priority=True)]
    preview = reactive(Text.from_markup(":page_facing_up: Enter File Name"))

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
            Button("Save", id="btn-modal-save", disabled=True),
            Button("Cancel", id="btn-modal-cancel"),
            id="modal-save-vert",
        )

    @on(Input.Submitted)
    def press_button(self):
        self.query_one("#btn-modal-save", Button).press()

    @on(Button.Pressed, "#btn-modal-cancel")
    def action_close_window(self) -> None:
        self.dismiss()

    @on(Button.Pressed, "#btn-modal-save")
    def save_new_file(self) -> None:
        new_path = ENV_FILE_DIR_PATH / self.query_one(Input).value
        self.dismiss(result=new_path)

        # write_to_file(
        #     path=new_path,
        #     content=env_dict_to_content(content_dict=self.app.content_dict),
        # )
        #
        # self.app.file_tree = update_file_tree()
        #
        # self.app.query_one(EnvFileSelector).refresh(recompose=True).focus()

    @on(Input.Changed, "#inp-new-file-name")
    def format_name(self, event: Input.Changed):
        text = event.input.value or event.input.placeholder
        if "/" not in text:
            preview_name = Text.from_markup(f":page_facing_up: {text}")
        elif len(text.split("/")) == 2:
            folder, file = [el.strip() for el in text.split("/")]
            preview_name = Text.from_markup(
                f":file_folder: {folder} / :page_facing_up: {file}"
            )
        else:
            preview_name = Text.from_markup(
                ":cross_mark: Enter a valid Folder/File Name"
            )

        self.preview = preview_name

        if event.input.is_valid and event.input.value:
            self.query_one("#btn-modal-save", Button).disabled = False
        else:
            self.query_one("#btn-modal-save", Button).disabled = True

        self.query_one("#lbl-new-file-name", Label).update(self.preview)
