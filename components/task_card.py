from datetime import datetime
from typing import Callable

from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from models.task import Task
from theme.colors import PRIORITY_COLOR_MAP, SURFACE, TEXT_PRIMARY, TEXT_SECONDARY


class TaskCard(MDCard):
    def __init__(self, task: Task, on_complete: Callable[[Task], None], on_edit: Callable[[Task], None], archived=False, on_delete=None, **kwargs):
        super().__init__(**kwargs)
        self.task = task
        self.orientation = "horizontal"
        self.padding = dp(0)
        self.size_hint_y = None
        self.height = dp(120 if task.description else 96)
        self.radius = [18, 18, 18, 18]
        self.md_bg_color = SURFACE
        self.elevation = 0
        self.opacity = 0.65 if archived else 1

        strip = MDBoxLayout(size_hint=(None, 1), width=dp(6))
        strip.md_bg_color = PRIORITY_COLOR_MAP.get(task.priority, PRIORITY_COLOR_MAP[2])
        self.add_widget(strip)

        content = MDBoxLayout(orientation="vertical", padding=(dp(12), dp(10), dp(8), dp(10)), spacing=dp(4))
        title = MDLabel(
            text=task.title,
            font_name="Museo",
            bold=True,
            theme_text_color="Custom",
            text_color=TEXT_PRIMARY,
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=dp(26),
        )
        content.add_widget(title)

        if task.description:
            description = MDLabel(
                text=task.description,
                font_name="Museo",
                theme_text_color="Custom",
                text_color=TEXT_SECONDARY,
                halign="left",
                valign="top",
                size_hint_y=None,
                height=dp(34),
            )
            description.shorten = True
            description.max_lines = 2
            content.add_widget(description)

        date_text = None
        if task.deadline:
            date_text = task.deadline
        if archived and task.completed_at:
            dt = datetime.fromisoformat(task.completed_at)
            date_text = f"Completed: {dt.strftime('%d %b %Y, %H:%M')}"

        if date_text:
            date_row = MDBoxLayout(orientation="horizontal", spacing=dp(6), size_hint_y=None, height=dp(20))
            date_row.add_widget(Image(source="Assets/calendar.png", size_hint=(None, None), size=(dp(16), dp(16)), color=TEXT_SECONDARY))
            date_row.add_widget(
                MDLabel(
                    text=date_text,
                    font_name="Museo",
                    theme_text_color="Custom",
                    text_color=TEXT_SECONDARY,
                    halign="left",
                    valign="middle",
                )
            )
            content.add_widget(date_row)

        self.add_widget(content)

        actions = MDBoxLayout(orientation="vertical", size_hint=(None, 1), width=dp(52), padding=(0, dp(8), dp(8), dp(8)), spacing=dp(10))
        if archived:
            delete_btn = Button(
                background_normal="Assets/trash.png",
                background_down="Assets/trash.png",
                background_color=(1, 1, 1, 1),
                size_hint=(None, None),
                size=(dp(26), dp(26)),
                border=(0, 0, 0, 0),
            )
            delete_btn.bind(on_release=lambda *_: on_delete(task) if on_delete else None)
            actions.add_widget(delete_btn)
        else:
            complete_btn = Button(
                background_normal="Assets/check-square-outline.png",
                background_down="Assets/check-square-outline.png",
                background_color=(1, 1, 1, 1),
                size_hint=(None, None),
                size=(dp(26), dp(26)),
                border=(0, 0, 0, 0),
            )
            complete_btn.bind(on_release=lambda *_: on_complete(task))

            edit_btn = Button(
                background_normal="Assets/pencil.png",
                background_down="Assets/pencil.png",
                background_color=(1, 1, 1, 1),
                size_hint=(None, None),
                size=(dp(26), dp(26)),
                border=(0, 0, 0, 0),
            )
            edit_btn.bind(on_release=lambda *_: on_edit(task))
            actions.add_widget(complete_btn)
            actions.add_widget(edit_btn)

        self.add_widget(actions)
