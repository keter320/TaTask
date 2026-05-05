from kivy.core.text import LabelBase
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import FadeTransition, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel

from app_meta import APP_BRIEF, APP_VERSION, AUTHOR_INFO, AUTHOR_NICK
from components.add_task_dialog import AddTaskDialog
from components.complete_dialog import CompleteDialog
from components.confirm_dialog import ConfirmDialog
from db.database import DatabaseManager
from screens.archive_screen import ArchiveScreen
from screens.home_screen import HomeScreen
from theme.colors import BACKGROUND, PRIMARY_PURPLE, TEXT_PRIMARY


# Register fonts before UI is built to avoid fallback fonts.
LabelBase.register(name="Museo", fn_regular="EXLJBRIS_-_MUSEO_CYRL_300-WEBFONT (1).TTF")
LabelBase.register(name="OriginalSurfer", fn_regular="Original by fnkfrsh.otf")


class TaTaskApp(MDApp):
    sm = ObjectProperty(None)
    about_dialog = ObjectProperty(None)

    def build(self):
        self.title = "TaTask"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"

        self.db = DatabaseManager()
        self.confirm_dialog = ConfirmDialog()
        self.add_dialog = AddTaskDialog(self.save_task)
        self.complete_dialog = CompleteDialog(self.complete_task)

        self.sm = ScreenManager(transition=FadeTransition(duration=0.2))
        self.home_screen = HomeScreen(self)
        self.archive_screen = ArchiveScreen(self)
        self.sm.add_widget(self.home_screen)
        self.sm.add_widget(self.archive_screen)
        self.refresh_all()
        return self.sm

    def refresh_all(self):
        active = self.db.get_active_tasks()
        archived = self.db.get_archived_tasks()
        self.home_screen.refresh_tasks(active)
        self.archive_screen.refresh_tasks(archived)

    def open_add_dialog(self):
        self.add_dialog.open()

    def open_edit_dialog(self, task):
        self.add_dialog.open(task=task)

    def open_complete_dialog(self, task):
        self.complete_dialog.open(task)

    def save_task(self, title, description, priority, deadline, task_id=None):
        if task_id:
            self.db.update_task(task_id, title, description, priority, deadline)
        else:
            self.db.create_task(title, description, priority, deadline)
        self.refresh_all()

    def complete_task(self, task):
        self.home_screen.animate_remove(task.id)
        self.db.archive_task(task.id)
        self.refresh_all()

    def confirm_delete_archived_task(self, task):
        self.confirm_dialog.open(
            title="Delete task?",
            text="This action is permanent.",
            action_text="Delete",
            on_confirm=lambda: self._delete_archived_task(task.id),
        )

    def _delete_archived_task(self, task_id):
        self.db.delete_task(task_id)
        self.refresh_all()

    def confirm_clear_archive(self):
        self.confirm_dialog.open(
            title="Clear archive?",
            text="All archived tasks will be permanently deleted.",
            action_text="Clear",
            on_confirm=self._clear_archive,
        )

    def _clear_archive(self):
        self.db.clear_archive()
        self.refresh_all()

    def open_archive(self):
        self.sm.current = "archive"
        self.refresh_all()

    def go_home(self):
        self.sm.current = "home"
        self.refresh_all()

    def show_about(self):
        if self.about_dialog:
            self.about_dialog.dismiss()
            self.about_dialog = None

        content = MDBoxLayout(orientation="vertical", spacing="8dp", adaptive_height=True)
        content.add_widget(MDLabel(text=f"Version: {APP_VERSION}", font_name="Museo", adaptive_height=True))
        content.add_widget(MDLabel(text=f"Author: {AUTHOR_NICK}", font_name="Museo", adaptive_height=True))
        content.add_widget(MDLabel(text=AUTHOR_INFO, font_name="Museo", adaptive_height=True))
        content.add_widget(MDLabel(text=APP_BRIEF, font_name="Museo", adaptive_height=True))

        self.about_dialog = MDDialog(
            title="About TaTask",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="Close", font_name="Museo", on_release=lambda *_: self.about_dialog.dismiss()),
            ],
        )
        self.about_dialog.open()


if __name__ == "__main__":
    TaTaskApp().run()
