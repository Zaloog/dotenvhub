from __future__ import annotations

from dataclasses import dataclass

from textual import on
from textual.message import Message
from textual.reactive import reactive
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import TextArea, Input, Label


class FilePreviewer2(Horizontal):
    def compose(self):
        yield TextArea(id="text-preview")

    @on(TextArea.Changed)
    def disable_buttons(self):
        save_button = self.app.query_one("#btn-save-file")
        save_button.disabled = False


class KeyInput(Input):
    def __init__(self, key):
        super().__init__(value=key, placeholder="Enter Key")


class ValueInput(Input):
    def __init__(self, value):
        super().__init__(value=value, placeholder="Enter Value")


class KeyValPair(Horizontal):
    @dataclass
    class ValidMessage(Message):
        kv_pair: KeyValPair

        @property
        def control(self) -> KeyValPair:
            """Alias for self.input."""
            return self.kv_pair

    valid: reactive[bool] = reactive(False)
    key: reactive[str] = reactive("")
    value: reactive[str] = reactive("")

    def __init__(self, key: str = "", value: str = ""):
        super().__init__()
        self.key = key
        self.value = value

    def compose(self):
        yield KeyInput(key=self.key)
        yield Label("=")
        yield ValueInput(value=self.value)

    @on(Input.Changed)
    def check_if_valid(self):
        self.key = self.query_one(KeyInput).value
        self.value = self.query_one(ValueInput).value
        self.notify(f"key {self.key}, value:{self.value}", timeout=1)

        self.valid = all((self.key != "", self.value != ""))

    def watch_valid(self):
        self.notify(f"watch valid: {self.valid}", timeout=1)
        if self.valid:
            self.styles.border_left = ("vkey", "green")
            self.post_message(self.ValidMessage(kv_pair=self))
        else:
            self.styles.border_left = ("vkey", "red")

    @on(Input.Submitted)
    def go_to_next(self):
        self.app.action_focus_next()


class FilePreviewer(VerticalScroll):
    def __init__(self, id: str | None = None):
        super().__init__(id=id)

    def on_mount(self):
        self.mount(KeyValPair())

    @on(KeyValPair.ValidMessage)
    def add_new_keyvalpair(self):
        if self.query_children(KeyValPair)[-1].valid:
            self.mount(KeyValPair())
