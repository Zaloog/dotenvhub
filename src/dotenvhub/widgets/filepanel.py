from typing import TYPE_CHECKING

from textual.css.query import NoMatches

if TYPE_CHECKING:
    from dotenvhub.tui import DotEnvHub

from textual import on
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.widgets import Button, Collapsible, Label, ListItem, ListView, Input
from rich.text import Text

from dotenvhub.constants import ENV_FILE_DIR_PATH
from dotenvhub.utils import get_env_content, update_file_tree, env_content_to_dict


class CustomListItem(ListItem):
    app: "DotEnvHub"

    def __init__(self, file_name: str, dir_name: str = ".", *args, **kwargs):
        self.file_name = file_name
        self.dir_name = dir_name
        if self.dir_name == ".":
            self.complete_path = ENV_FILE_DIR_PATH / self.file_name
        else:
            self.complete_path = ENV_FILE_DIR_PATH / self.dir_name / self.file_name
        super().__init__(*args, **kwargs)

    def compose(self):
        yield Label(Text.from_markup(f":page_facing_up: {self.file_name}"))

        # Replace dots and other invalid chars with underscores for IDs
        safe_filename = self.file_name.replace(".", "_")

        btn_edit = Button(
            "edit",
            id=f"btn-edit-{safe_filename}",
            classes="edit",
            variant="warning",
        )
        btn_edit.jump_mode = "click"
        yield btn_edit

        btn_delete = Button(
            "delete",
            id=f"btn-del-{safe_filename}",
            classes="delete",
            variant="error",
        )
        btn_delete.jump_mode = "click"
        yield btn_delete

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
        await self.app.reset_values()
        # await self.app.file_previewer.clear()
        try:
            self.app.query_one(ListView).focus()
        except NoMatches:
            pass

    @on(Button.Pressed, ".edit")
    def edit_env_file(self):
        self.app.query_one(Input).focus()


class CustomListView(ListView):
    app: "DotEnvHub"
    BINDINGS = [
        Binding(
            key="k,up", action="new_cursor_up", description="Up", key_display="↑/k"
        ),
        Binding(
            key="j,down",
            action="new_cursor_down",
            description="Down",
            key_display="↓/j",
        ),
    ]

    def on_focus(self):
        self.index = 0

    def action_new_cursor_up(self):
        if self.index != 0:
            self.action_cursor_up()
        else:
            self.app.action_focus_previous()
            self.index = None

    def action_new_cursor_down(self):
        if self.index != (len(self.children) - 1):
            self.action_cursor_down()
        else:
            self.app.action_focus_next()
            self.index = None


class CustomCollapsible(Collapsible):
    app: "DotEnvHub"
    BINDINGS = [
        Binding("enter,space", "toggle_show", description="Toggle", show=False),
        Binding(
            key="k,up", action="new_cursor_up", description="Up", key_display="↑/k"
        ),
        Binding(
            key="j,down",
            action="new_cursor_down",
            description="Down",
            key_display="↓/j",
        ),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jump_mode = "click"
        self.can_focus = True

    def action_toggle_show(self):
        self.collapsed = not self.collapsed

    def action_new_cursor_up(self):
        self.app.action_focus_previous()

    def action_new_cursor_down(self):
        self.app.action_focus_next()


class EnvFileSelector(VerticalScroll):
    app: "DotEnvHub"
    can_focus = False

    def compose(self):
        for dirpath, filenames in self.app.file_tree.items():
            if dirpath == ".":
                general_list = CustomListView(
                    *[
                        CustomListItem(file_name=file, dir_name=dirpath)
                        for file in filenames
                    ],
                    initial_index=None,
                )
                yield general_list
            else:
                folder_list = CustomListView(
                    *[
                        CustomListItem(file_name=file, dir_name=dirpath)
                        for file in filenames
                    ],
                    id=f"collaps-{dirpath}",
                    initial_index=None,
                )

                folder_colabs = CustomCollapsible(
                    folder_list,
                    title=dirpath,
                    collapsed_symbol="📁",
                    expanded_symbol="📂",
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
        self.app.file_previewer.has_changed = False

    @on(ListView.Selected)
    async def update_preview_text(self):
        self.app.current_content = get_env_content(filepath=self.app.file_to_show_path)
        self.app.content_dict = env_content_to_dict(content=self.app.current_content)

        await self.app.file_previewer.clear()
        self.app.file_previewer.load_values_from_dict(env_dict=self.app.content_dict)
