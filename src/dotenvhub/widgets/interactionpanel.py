from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dotenvhub.tui import DotEnvHub

from textual import on
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Button, Input, Label, ListView

from dotenvhub.utils import (
    update_file_tree,
    copy_path_to_clipboard,
    create_copy_in_cwd,
    create_shell_export_str,
    write_to_file,
    env_dict_to_content,
)
from dotenvhub.widgets.modals import ModalSaveScreen, ModalShellSelector


class InteractionPanel(Container):
    app: "DotEnvHub"

    def compose(self):
        yield Button(
            "Create Shell String [black on yellow]^e[/]",
            id="btn-shell-export",
            disabled=True,
            variant="primary",
        )
        yield Button(
            "Export File to current dir [black on yellow]^f[/]",
            id="btn-file-export",
            disabled=True,
            variant="primary",
        )
        yield Button(
            "Copy Path to Clipboard [black on yellow]^c[/]",
            id="btn-copy-path",
            disabled=True,
            variant="primary",
        )
        with Vertical(id="interaction-shell-select"):
            yield Label("Select Shell")
            yield Button(
                label=self.app.current_shell + " [black on yellow]^z[/]",
                id="btn-shell-select",
                variant="primary",
            )
        with Vertical(id="interaction-export-name"):
            yield Label("Export filename")
            yield Input(
                value=".env",
                placeholder="env file name for export",
                id="export-env-name",
            )
        with Horizontal(id="horizontal-save-new"):
            yield Button(
                "New Env File [black on yellow]^n[/]",
                id="btn-new-file",
                disabled=False,
                variant="success",
            )
            yield Button(
                "Save Env File [black on yellow]^s[/]",
                id="btn-save-file",
                disabled=True,
                variant="success",
            )

    # Export Interactions
    @on(Button.Pressed, "#btn-copy-path")
    def copy_env_path(self):
        copy_str = copy_path_to_clipboard(path=self.app.file_to_show_path)
        self.notify(title="Copied to Clipboard", message=f"Path: [green]{copy_str}[/]")

    @on(Button.Pressed, "#btn-file-export")
    def export_env_file(self):
        export_filename = self.query_one(Input).value
        create_copy_in_cwd(
            filename=export_filename, filepath=self.app.file_to_show_path
        )
        self.notify(title="Env File Created", message=f"Created: {export_filename}")

    @on(Button.Pressed, "#btn-shell-export")
    def export_env_str_shell(self):
        shell_str = create_shell_export_str(
            shell=self.app.current_shell, env_content=self.app.current_content
        )
        self.notify(
            title="Copied to Clipboard",
            message=f"Command: [green]{shell_str}[/]",
        )

    # Shell Select Interactions
    @on(Button.Pressed, "#btn-shell-select")
    def pop_modal_shell(self):
        self.app.push_screen(ModalShellSelector())

    # Env File Interactions
    @on(Button.Pressed, "#btn-new-file")
    async def new_file(self, event: Button.Pressed):
        await self.app.reset_values()

        # await self.app.file_previewer.new_file()

        event.button.disabled = True
        self.query_one("#btn-save-file").disabled = False

        self.app.query_one("#file-preview").border_title = "Creating New .Env File ..."

        for views in self.app.query(ListView):
            views.query(Button).remove_class("active")
            views.index = None

    @on(Button.Pressed, "#btn-save-file")
    def save_file(self, event: Button.Pressed):
        self.app.file_previewer.update_content_dict()
        self.app.file_previewer.has_changed = False
        if not self.app.content_dict:
            self.notify(
                severity="warning",
                title="Warning",
                message="No valid Values to save",
            )
            return

        self.query_one("#btn-new-file").disabled = False

        self.app.current_content = env_dict_to_content(
            content_dict=self.app.content_dict
        )
        if self.app.file_to_show:
            write_to_file(
                path=Path(self.app.file_to_show_path), content=self.app.current_content
            )
        else:
            self.app.push_screen(ModalSaveScreen(), callback=self.modal_select_new_file)

    async def modal_select_new_file(self, new_path: Path | None):
        if new_path is None:
            return

        write_to_file(
            path=new_path,
            content=env_dict_to_content(content_dict=self.app.content_dict),
        )

        self.app.file_tree = update_file_tree()

        self.app.query_one("#file-selector").refresh(recompose=True)
        await self.app.reset_values()
