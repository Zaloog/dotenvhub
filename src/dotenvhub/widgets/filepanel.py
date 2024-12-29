from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dotenvhub.tui import DotEnvHub

from textual import on
from textual.containers import VerticalScroll
from textual.widgets import Button, Collapsible, Label, ListItem, ListView, Input

from dotenvhub.constants import ENV_FILE_DIR_PATH
from dotenvhub.utils import get_env_content, update_file_tree, env_content_to_dict
from dotenvhub.widgets.previewpanel import VariableInput


class CustomListItem(ListItem):
    def __init__(self, file_name: str, dir_name: str = ".", *args, **kwargs):
        self.file_name = file_name
        self.dir_name = dir_name
        if self.dir_name == ".":
            self.complete_path = ENV_FILE_DIR_PATH / self.file_name
        else:
            self.complete_path = ENV_FILE_DIR_PATH / self.dir_name / self.file_name
        super().__init__(*args, **kwargs)

    def compose(self):
        yield Label(f":page_facing_up: {self.file_name}")
        # yield Button(
        #     "Edit", id=f"btn-edit-{self.file_name}", classes="edit", variant="warning"
        # )
        yield Button(
            "Delete", id=f"btn-del-{self.file_name}", classes="delete", variant="error"
        )

    @on(Button.Pressed, ".delete")
    async def action_delete_env_file(self):
        # Delete File
        self.complete_path.unlink()
        try:
            # If Folder Empty delete Folder
            self.complete_path.parent.rmdir()
        except OSError:
            pass

        self.app.file_tree = update_file_tree()
        self.app.query_one(EnvFileSelector).refresh(recompose=True)

        # Clear Text Missing Border Title
        self.app.reset_values()
        await self.app.file_previewer.clear()

    @on(Button.Pressed, ".edit")
    def edit_env_file(self):
        self.app.query_one(Input).focus()


class EnvFileSelector(VerticalScroll):
    app: "DotEnvHub"

    def compose(self):
        for dirpath, filenames in self.app.file_tree.items():
            if dirpath == ".":
                general_list = ListView(
                    *[
                        CustomListItem(file_name=file, dir_name=dirpath)
                        for file in filenames
                    ],
                    initial_index=None,
                )
                yield general_list
            else:
                folder_list = ListView(
                    *[
                        CustomListItem(file_name=file, dir_name=dirpath)
                        for file in filenames
                    ],
                    id=f"collaps-{dirpath}",
                    initial_index=None,
                )

                folder_colabs = Collapsible(
                    folder_list,
                    title=dirpath,
                    collapsed_symbol=":file_folder:",
                    expanded_symbol=":open_file_folder:",
                )
                yield folder_colabs

    @on(ListView.Selected)
    def get_preview_file_path(self, event: ListView.Selected):
        selected_item = event.list_view.highlighted_child
        self.app.file_to_show = selected_item.file_name
        self.app.file_to_show_path = selected_item.complete_path

        self.query(Button).remove_class("active")
        selected_item.query(Button).add_class("active")

        # only collapsible lists have ID
        if event.list_view.id:
            self.app.file_previewer.border_title = (
                f"{selected_item.dir_name}/{self.app.file_to_show}"
            )
        else:
            self.app.file_previewer.border_title = self.app.file_to_show

    @on(ListView.Selected)
    def reset_highlights(self, event: ListView.Selected):
        for lviews in self.query(ListView):
            if lviews.id != event.list_view.id:
                lviews.index = None

    @on(ListView.Selected)
    def enable_buttons(self):
        self.app.query_one("#btn-shell-export").disabled = False
        self.app.query_one("#btn-file-export").disabled = False
        self.app.query_one("#btn-copy-path").disabled = False

        self.app.query_one("#btn-new-file").disabled = False
        self.app.query_one("#btn-save-file").disabled = True

    @on(ListView.Selected)
    async def update_preview_text(self):
        self.app.current_content = get_env_content(filepath=self.app.file_to_show_path)
        self.app.content_dict = env_content_to_dict(content=self.app.current_content)

        await self.app.file_previewer.clear()
        await self.app.file_previewer.load_values_from_dict(
            env_dict=self.app.content_dict
        )
        self.app.file_previewer.query_one(VariableInput).focus()
