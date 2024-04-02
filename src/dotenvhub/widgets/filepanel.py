from pathlib import Path

from textual import on
from textual.containers import VerticalScroll
from textual.widgets import Button, Collapsible, Label, ListItem, ListView, TextArea

from ..constants import ENV_FILE_DIR_PATH
from ..utils import get_env_content, update_file_tree


class EnvFileSelector(VerticalScroll):
    def compose(self):
        for dirpath, filenames in self.app.file_tree.items():
            if dirpath == ".":
                general_list = ListView(
                    *[
                        ListItem(
                            Label(f":page_facing_up: {file}"),
                            Button.warning(
                                "Edit", id=f"btn-edit-{file}", classes="edit"
                            ),
                            Button.error(
                                "Delete", id=f"btn-del-{file}", classes="delete"
                            ),
                            id=f"file-{file}",
                        )
                        for file in filenames
                    ],
                    initial_index=None,
                )
                yield general_list
            else:
                folder_list = ListView(
                    *[
                        ListItem(
                            Label(f":page_facing_up: {file}"),
                            Button.warning(
                                "Edit", id=f"btn-edit-{dirpath}-{file}", classes="edit"
                            ),
                            Button.error(
                                "Delete",
                                id=f"btn-del-{dirpath}-{file}",
                                classes="delete",
                            ),
                            id=f"{dirpath}-{file}",
                        )
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
        self.app.file_to_show = event.list_view.highlighted_child.id.split("-")[1]
        self.query(Button).remove_class("active")
        event.list_view.highlighted_child.query(Button).add_class("active")

        # only collapsible lists have ID
        if event.list_view.id:
            folder = Path(event.list_view.id.split("-")[1])
            self.app.file_to_show_path = (
                ENV_FILE_DIR_PATH / folder / self.app.file_to_show
            )
            self.app.query_one(
                "#file-preview"
            ).border_title = f"{folder} / {self.app.file_to_show}"
        else:
            self.app.file_to_show_path = ENV_FILE_DIR_PATH / self.app.file_to_show
            self.app.query_one("#file-preview").border_title = self.app.file_to_show

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
    def update_preview_text(self):
        self.app.current_content = get_env_content(filepath=self.app.file_to_show_path)

        text_widget = self.app.query_one(TextArea)
        text_widget.text = self.app.current_content
        text_widget.action_cursor_page_down()
        text_widget.disabled = True

    @on(Button.Pressed, ".delete")
    def delete_env_file(self, event: Button.Pressed):
        folder_file_path = event.button.id[8:].replace("-", "/")

        # Delete File
        (ENV_FILE_DIR_PATH / folder_file_path).unlink()
        try:
            # If Folder Empty delete Folder
            (ENV_FILE_DIR_PATH / folder_file_path).parent.rmdir()
        except OSError:
            pass

        self.app.file_tree = update_file_tree()
        self.app.query_one(EnvFileSelector).remove()
        self.app.query_one("#app-grid").mount(
            EnvFileSelector(id="file-selector"), before="#file-preview"
        )

        # Clear Text Missing Border Title
        self.app.file_to_show = ""
        self.app.file_to_show_path = ""
        self.app.current_content = ""

        text_widget = self.app.query_one(TextArea)
        text_widget.text = ""

    @on(Button.Pressed, ".edit")
    def edit_env_file(self):
        text_widget = self.app.query_one(TextArea)
        text_widget.disabled = False
        text_widget.focus()
