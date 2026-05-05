from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView

from components.task_card import TaskCard
from theme.colors import BACKGROUND, TEXT_PRIMARY, TEXT_SECONDARY


class ArchiveScreen(MDScreen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.name = "archive"
        self.md_bg_color = BACKGROUND

        root = MDBoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))
        top = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(48))
        back_btn = Button(
            background_normal="Assets/arrow_LEFT!.png",
            background_down="Assets/arrow_LEFT!.png",
            background_color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(dp(24), dp(24)),
            border=(0, 0, 0, 0),
        )
        back_btn.bind(on_release=lambda *_: self.app.go_home())
        top.add_widget(back_btn)
        top.add_widget(MDLabel(text="Archive", font_name="OriginalSurfer", theme_text_color="Custom", text_color=TEXT_PRIMARY))
        clear_btn = MDFlatButton(text="Clear All", font_name="Museo")
        clear_btn.bind(on_release=lambda *_: self.app.confirm_clear_archive())
        top.add_widget(clear_btn)
        root.add_widget(top)

        self.scroll = MDScrollView()
        self.list_box = MDBoxLayout(orientation="vertical", adaptive_height=True, spacing=dp(10))
        self.scroll.add_widget(self.list_box)
        root.add_widget(self.scroll)

        self.empty_box = MDBoxLayout(orientation="vertical", spacing=dp(10), adaptive_height=True)
        self.empty_box.add_widget(Image(source="Assets/list_icon.png", size_hint=(None, None), size=(dp(80), dp(80)), color=TEXT_SECONDARY))
        self.empty_box.add_widget(MDLabel(text="Archive is empty", font_name="Museo", theme_text_color="Custom", text_color=TEXT_SECONDARY, halign="center"))
        root.add_widget(self.empty_box)
        self.add_widget(root)

    def refresh_tasks(self, tasks):
        self.list_box.clear_widgets()
        has_tasks = len(tasks) > 0
        self.scroll.opacity = 1 if has_tasks else 0
        self.empty_box.opacity = 0 if has_tasks else 1
        for task in tasks:
            card = TaskCard(task, None, None, archived=True, on_delete=self.app.confirm_delete_archived_task)
            self.list_box.add_widget(card)
