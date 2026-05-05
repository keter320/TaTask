from datetime import date
from typing import Callable, Optional

from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.textfield import MDTextField

from models.task import Task
from theme.colors import ELEVATED_SURFACE, PRIMARY_PURPLE, PRIORITY_COLOR_MAP, TEXT_PRIMARY, TEXT_SECONDARY


class AddTaskDialog:
    def __init__(self, on_save: Callable[[str, str, int, Optional[str], Optional[int]], None]):
        self.on_save = on_save
        self.selected_priority = 2
        self.deadline = None
        self.edit_task_id = None
        self.dialog = None
        self.priority_checks = {}

    def open(self, task: Optional[Task] = None):
        self.edit_task_id = task.id if task else None
        self.selected_priority = task.priority if task else 2
        self.deadline = task.deadline if task else None

        content = MDBoxLayout(orientation="vertical", spacing=dp(12), size_hint_y=None, height=dp(360))
        title_text = "Edit Task" if task else "New Task"
        content.add_widget(MDLabel(text=title_text, font_name="OriginalSurfer", theme_text_color="Custom", text_color=TEXT_PRIMARY, font_style="H6"))

        self.title_field = MDTextField(
            hint_text="Task title",
            text=task.title if task else "",
            mode="rectangle",
            font_name="Museo",
            required=True,
        )
        self.description_field = MDTextField(
            hint_text="Add description...",
            text=task.description if task and task.description else "",
            multiline=True,
            mode="rectangle",
            font_name="Museo",
        )
        content.add_widget(self.title_field)
        content.add_widget(self.description_field)

        priority_row = MDBoxLayout(orientation="horizontal", spacing=dp(8), size_hint_y=None, height=dp(40))
        priority_row.add_widget(MDLabel(text="Priority", font_name="Museo", theme_text_color="Custom", text_color=TEXT_SECONDARY, size_hint_x=0.4))
        for level in (1, 2, 3):
            wrap = MDBoxLayout(orientation="horizontal", size_hint_x=0.2)
            check = MDCheckbox(group="priority", active=level == self.selected_priority)
            check.bind(active=lambda checkbox, value, l=level: self._set_priority(l, value))
            label = MDLabel(
                text=str(level),
                font_name="Museo",
                theme_text_color="Custom",
                text_color=PRIORITY_COLOR_MAP[level],
            )
            wrap.add_widget(check)
            wrap.add_widget(label)
            self.priority_checks[level] = check
            priority_row.add_widget(wrap)
        content.add_widget(priority_row)

        deadline_row = MDBoxLayout(orientation="horizontal", spacing=dp(8), size_hint_y=None, height=dp(44))
        deadline_row.add_widget(MDLabel(text="Deadline", font_name="Museo", theme_text_color="Custom", text_color=TEXT_SECONDARY, size_hint_x=0.35))
        self.deadline_label = MDLabel(
            text=self.deadline if self.deadline else "No deadline",
            font_name="Museo",
            theme_text_color="Custom",
            text_color=TEXT_PRIMARY if self.deadline else TEXT_SECONDARY,
        )
        pick_btn = MDFlatButton(text="Pick", font_name="Museo", on_release=self._pick_date)
        deadline_row.add_widget(self.deadline_label)
        deadline_row.add_widget(pick_btn)
        content.add_widget(deadline_row)

        self.dialog = MDDialog(
            md_bg_color=ELEVATED_SURFACE,
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="Cancel", font_name="Museo", theme_text_color="Custom", text_color=TEXT_SECONDARY, on_release=lambda *_: self.dialog.dismiss()),
                MDRaisedButton(text="Save", font_name="Museo", md_bg_color=PRIMARY_PURPLE, on_release=self._save),
            ],
        )
        self.dialog.open()

    def _set_priority(self, level, value):
        if value:
            self.selected_priority = level

    def _pick_date(self, *_):
        picker = MDDatePicker()
        picker.bind(on_save=self._on_date_saved)
        picker.open()

    def _on_date_saved(self, _instance, value: date, _date_range):
        self.deadline = value.isoformat()
        self.deadline_label.text = self.deadline
        self.deadline_label.text_color = TEXT_PRIMARY

    def _save(self, *_):
        title = self.title_field.text.strip()
        if not title:
            self.title_field.error = True
            self.title_field.helper_text = "Title is required"
            return
        self.on_save(
            title,
            self.description_field.text.strip(),
            self.selected_priority,
            self.deadline,
            self.edit_task_id,
        )
        self.dialog.dismiss()
