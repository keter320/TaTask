from typing import Callable

from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel

from models.task import Task
from theme.colors import ELEVATED_SURFACE, PRIMARY_PURPLE, TEXT_PRIMARY, TEXT_SECONDARY


class SwipeCompleteWidget(Widget):
    progress = NumericProperty(0)

    def __init__(self, on_complete: Callable[[], None], **kwargs):
        super().__init__(**kwargs)
        self.on_complete = on_complete
        self.dragging = False
        self.size_hint_y = None
        self.height = dp(56)
        self.bind(pos=self._draw, size=self._draw, progress=self._draw)

    def _draw(self, *_):
        self.canvas.clear()
        with self.canvas:
            Color(0.27, 0.28, 0.38, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[self.height / 2])
            Color(*PRIMARY_PURPLE)
            handle_x = self.x + (self.width - self.height) * self.progress
            RoundedRectangle(pos=(handle_x, self.y), size=(self.height, self.height), radius=[self.height / 2])

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.dragging = True
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.dragging:
            rel = (touch.x - self.x - self.height / 2) / max(1, (self.width - self.height))
            self.progress = max(0, min(1, rel))
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.dragging:
            self.dragging = False
            if self.progress >= 0.9:
                self.progress = 1
                self.on_complete()
            else:
                self.progress = 0
            return True
        return super().on_touch_up(touch)


class CompleteDialog:
    def __init__(self, on_confirm: Callable[[Task], None]):
        self.on_confirm = on_confirm
        self.dialog = None
        self.task = None

    def open(self, task: Task):
        self.task = task
        content = MDBoxLayout(orientation="vertical", spacing=dp(12), size_hint_y=None, height=dp(200))
        content.add_widget(MDLabel(text="Complete task?", font_name="OriginalSurfer", theme_text_color="Custom", text_color=TEXT_PRIMARY, font_style="H6"))
        content.add_widget(MDLabel(text=task.title, font_name="Museo", theme_text_color="Custom", text_color=TEXT_SECONDARY, size_hint_y=None, height=dp(34)))

        slider_wrap = MDBoxLayout(orientation="vertical", size_hint_y=None, height=dp(62))
        self.slider = SwipeCompleteWidget(on_complete=self._confirm)
        slider_wrap.add_widget(self.slider)
        self.slide_label = MDLabel(
            text="Slide to complete",
            font_name="Museo",
            theme_text_color="Custom",
            text_color=TEXT_PRIMARY,
            halign="center",
            valign="middle",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.slider.bind(progress=lambda *_: setattr(self.slide_label, "opacity", 1 - self.slider.progress))
        slider_wrap.add_widget(self.slide_label)
        content.add_widget(slider_wrap)

        self.dialog = MDDialog(
            md_bg_color=ELEVATED_SURFACE,
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="Cancel", font_name="Museo", theme_text_color="Custom", text_color=TEXT_SECONDARY, on_release=lambda *_: self.dialog.dismiss())
            ],
        )
        self.dialog.open()

    def _confirm(self):
        try:
            from android.vibrator import vibrate  # type: ignore

            vibrate(0.05)
        except Exception:
            pass
        self.dialog.dismiss()
        self.on_confirm(self.task)
