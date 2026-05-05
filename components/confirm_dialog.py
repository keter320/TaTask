from typing import Callable

from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog

from theme.colors import ELEVATED_SURFACE, PRIORITY_HIGH, TEXT_SECONDARY


class ConfirmDialog:
    def __init__(self):
        self.dialog = None

    def open(self, title: str, text: str, action_text: str, on_confirm: Callable[[], None]):
        def _confirm(*_):
            self.dialog.dismiss()
            on_confirm()

        self.dialog = MDDialog(
            title=title,
            text=text,
            md_bg_color=ELEVATED_SURFACE,
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    font_name="Museo",
                    theme_text_color="Custom",
                    text_color=TEXT_SECONDARY,
                    on_release=lambda *_: self.dialog.dismiss(),
                ),
                MDRaisedButton(text=action_text, font_name="Museo", md_bg_color=PRIORITY_HIGH, on_release=_confirm),
            ],
        )
        self.dialog.open()
