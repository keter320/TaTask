from kivy.animation import Animation
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView

from components.task_card import TaskCard
from theme.colors import BACKGROUND, PRIMARY_PURPLE, TEXT_PRIMARY, TEXT_SECONDARY


class HomeScreen(MDScreen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.name = "home"
        self.md_bg_color = BACKGROUND

        root = MDBoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))
        top = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(48))
        top.add_widget(MDLabel(text="TaTask", font_name="OriginalSurfer", theme_text_color="Custom", text_color=TEXT_PRIMARY, font_style="H5"))
        self.counter = MDLabel(text="0 active", font_name="Museo", theme_text_color="Custom", text_color=TEXT_SECONDARY, size_hint_x=None, width=dp(88))
        top.add_widget(self.counter)
        archive_btn = Button(
            background_normal="Assets/archive_icon.png",
            background_down="Assets/archive_icon.png",
            background_color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(dp(24), dp(24)),
            border=(0, 0, 0, 0),
        )
        archive_btn.bind(on_release=lambda *_: self.app.open_archive())
        top.add_widget(archive_btn)
        root.add_widget(top)

        self.scroll = MDScrollView()
        self.list_box = MDBoxLayout(orientation="vertical", adaptive_height=True, spacing=dp(10))
        self.scroll.add_widget(self.list_box)
        root.add_widget(self.scroll)

        self.empty_box = MDBoxLayout(orientation="vertical", spacing=dp(10), adaptive_height=True, pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.empty_box.add_widget(Image(source="Assets/list_icon.png", size_hint=(None, None), size=(dp(80), dp(80)), color=TEXT_SECONDARY))
        self.empty_box.add_widget(MDLabel(text="No active tasks", font_name="Museo", theme_text_color="Custom", text_color=TEXT_SECONDARY, halign="center"))
        root.add_widget(self.empty_box)

        fab_row = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(68))
        fab_row.add_widget(MDBoxLayout())
        self.fab = Button(
            background_normal="Assets/+_icon.png",
            background_down="Assets/+_icon.png",
            background_color=PRIMARY_PURPLE,
            size_hint=(None, None),
            size=(dp(56), dp(56)),
            border=(0, 0, 0, 0),
        )
        self.fab.bind(on_release=lambda *_: self.app.open_add_dialog())
        fab_row.add_widget(self.fab)
        root.add_widget(fab_row)
        self.add_widget(root)

    def refresh_tasks(self, tasks):
        self.list_box.clear_widgets()
        self.counter.text = f"{len(tasks)} active"
        has_tasks = len(tasks) > 0
        self.scroll.opacity = 1 if has_tasks else 0
        self.empty_box.opacity = 0 if has_tasks else 1

        for task in tasks:
            card = TaskCard(task, self.app.open_complete_dialog, self.app.open_edit_dialog)
            self.list_box.add_widget(card)

    def animate_remove(self, task_id: int):
        for card in list(self.list_box.children):
            if card.task.id == task_id:
                anim = Animation(opacity=0, duration=0.2)
                anim.bind(on_complete=lambda *_: self.list_box.remove_widget(card))
                anim.start(card)
                break
