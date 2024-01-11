from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.screen import Screen
from textual.widgets import Placeholder

# Fragen
# Do Updates happen in Displayed UI based on File System Changes
# Shell Auto Detection


class Header(Placeholder):
    pass


class Footer(Placeholder):
    pass


class TextArea(Placeholder):
    pass


class FileListView(Placeholder):
    pass


class ViewScreen(Screen):
    def compose(self) -> ComposeResult:
        yield VerticalScroll(
            Container(
                Header(id="header"),
                Horizontal(
                    FileListView(id="filelist"), TextArea(variant="text", id="text")
                ),
                Footer(id="footer"),
                id="container",
            )
        )


class DotEnvHub(App):
    CSS_PATH = "./assets/tui.css"

    def on_ready(self) -> None:
        self.push_screen(ViewScreen())


myapp = DotEnvHub()
