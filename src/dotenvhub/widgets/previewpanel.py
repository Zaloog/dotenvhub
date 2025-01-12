from __future__ import annotations
from typing import TYPE_CHECKING

from textual.binding import Binding
from textual.css.query import NoMatches

if TYPE_CHECKING:
    from dotenvhub.tui import DotEnvHub

from dataclasses import dataclass

from textual import on
from textual.message import Message
from textual.reactive import reactive
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Input, Label, ListView


class VariableInput(Input):
    def __init__(self, key):
        with self.prevent(Input.Changed):
            super().__init__(value=key, placeholder="Enter Variable")


class ValueInput(Input):
    def __init__(self, value):
        with self.prevent(Input.Changed):
            super().__init__(value=value, placeholder="Enter Value")


class KeyValPair(Horizontal):
    app: "DotEnvHub"

    @dataclass
    class ValidMessage(Message):
        kv_pair: KeyValPair

        @property
        def control(self) -> KeyValPair:
            return self.kv_pair

    valid: reactive[bool] = reactive(False)
    key: reactive[str] = reactive("")
    value: reactive[str] = reactive("")

    def __init__(self, key: str = "", value: str = ""):
        super().__init__()
        self.key = key
        self.value = value

    def compose(self):
        yield VariableInput(key=self.key)
        yield Label("=")
        yield ValueInput(value=self.value)

    @on(Input.Changed)
    def check_if_valid(self):
        self.key = self.query_one(VariableInput).value
        self.value = self.query_one(ValueInput).value

        self.valid = all((self.key != "", self.value != ""))

    def watch_valid(self):
        if self.valid:
            self.styles.border_left = ("vkey", "green")
            self.post_message(self.ValidMessage(kv_pair=self))
        else:
            self.styles.border_left = ("vkey", "red")

    @on(VariableInput.Submitted)
    def go_to_next(self, event: Input.Submitted):
        self.app.action_focus_next()


class FilePreviewer(VerticalScroll):
    app: "DotEnvHub"
    has_changed: reactive[bool] = reactive(False, init=False)
    can_focus = False
    BINDINGS = [Binding("escape", "focus_file_selector", show=False, priority=True)]

    def action_focus_file_selector(self):
        try:
            self.app.query_one(".-highlight").parent.focus()
        except NoMatches:
            self.app.query_one(ListView).focus()

    def __init__(self, id: str | None = None):
        super().__init__(id=id)

    def load_values_from_dict(self, env_dict: dict[str, str] | None = None):
        for key, val in env_dict.items():
            kv_pair = KeyValPair(key=key, value=val)
            kv_pair.valid = True
            self.mount(kv_pair)

    async def new_file(self):
        await self.clear()
        await self.mount(KeyValPair())
        self.query_one(KeyValPair).query_one(Input).focus()

    async def clear(self):
        await self.remove_children()

    @on(Input.Changed)
    def update_content_dict(self):
        self.app.content_dict = {}
        self.has_changed = True
        for kv_pair in self.query(KeyValPair):
            if not kv_pair.valid:
                kv_pair.styles.border_left = ("vkey", "red")
                continue
            key, val = kv_pair.key, kv_pair.value
            if key in self.app.content_dict.keys():
                kv_pair.styles.border_left = ("vkey", "yellow")
                kv_pair.query_one(VariableInput).border_title = "duplicate"
                kv_pair.query_one(VariableInput).styles.border = ("tall", "yellow")
                continue
            kv_pair.styles.border_left = ("vkey", "green")
            kv_pair.query_one(VariableInput).border_title = ""
            kv_pair.query_one(VariableInput).styles.border = None
            self.app.content_dict[key] = val

    @on(KeyValPair.ValidMessage)
    def add_new_keyvalpair(self):
        if self.query_children(KeyValPair)[-1].valid:
            self.mount(KeyValPair())

    def watch_has_changed(self):
        self.app.file_interaction.query_exactly_one(
            "#btn-save-file"
        ).disabled = not self.has_changed
        self.app.file_previewer.border_subtitle = (
            "[yellow on black]file was edited[/]" if self.has_changed else None
        )
