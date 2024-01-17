from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label

from ..config import cfg
from ..constants import SHELLS


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
