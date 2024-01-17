from textual.containers import Container, Vertical
from textual.widgets import Button, Input, Label


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
            yield Button(
                label=self.app.current_shell, id="btn-shell-select", variant="primary"
            )
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
