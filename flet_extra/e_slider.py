from typing import Optional
import os

from flet_core.control import OptionalNumber
from flet_core.types import AnimationValue
from flet_core import (
    GestureDetector,
    Stack,
    Container,
    Column,
    Animation,
    AnimationCurve,
    MainAxisAlignment,
    colors,
    alignment,
    LinearGradient,
    ImageRepeat
)


class ESlider(GestureDetector):
    def __init__(
            self,
            orientation: Optional[str] = 'horizontal',
            length: OptionalNumber = 200,
            thickness: OptionalNumber = 30,
            min: OptionalNumber = 0,
            max: OptionalNumber = 100,
            divisions: Optional[int] = None,
            color: Optional[str] = colors.PRIMARY,
            bgcolor: Optional[str] = colors.PRIMARY_CONTAINER,
            gradient_bgcolor: list[str] = None,
            margin: Optional[int] = 0,
            animate: AnimationValue = Animation(400, AnimationCurve.EASE),
            border_radius: Optional[int] = None,
            value: OptionalNumber = 0,
            on_change=None
    ):
        super().__init__()
        self.orientation = orientation
        self.length = length
        self.thickness = thickness
        self.min = min
        self.max = max
        self.divisions = divisions
        self.color = color
        self.bgcolor = bgcolor
        self.gradient_bgcolor = gradient_bgcolor
        self.margin = margin
        self.animate = animate
        self.border_radius = border_radius
        self.value = value
        self.on_pan_start = self.update_slider
        self.on_pan_update = self.update_slider
        self.on_pan_end = self.enable_animation
        self.on_change = on_change

        self.content = Stack()
        self.slider_transparent = None
        self.slider_background = None
        self.slider_foreground = None
        self.valid_orientations = None
        self.build_slider()

    def build_slider(self):
        self.border_radius = self.border_radius or self.thickness // 2
        self.valid_orientations = {
            'horizontal': self.slide_horizontal,
            'vertical': self.slide_vertical
        }

        self.slider_transparent = Container(
            margin=self.margin,
            image_src=os.path.join(os.path.dirname(__file__), 'transparent_grid.png'),
            image_repeat=ImageRepeat.REPEAT,
            border_radius=self.border_radius - self.margin
        )

        self.slider_background = Container(
            margin=self.margin,
            border_radius=self.border_radius - self.margin
        )

        if self.gradient_bgcolor:
            self.slider_background.gradient = LinearGradient(
                begin=alignment.center_left if self.orientation == 'horizontal' else alignment.bottom_center,
                end=alignment.center_right if self.orientation == 'horizontal' else alignment.top_center,
                colors=self.gradient_bgcolor
            )
        else:
            self.slider_background.bgcolor = self.bgcolor

        self.slider_foreground = Container(
            bgcolor=self.color,
            border_radius=self.border_radius,
            animate=self.animate
        )

        if self.orientation == 'horizontal':
            self.slider_foreground.width = self.value_to_position() if self.value else self.thickness
            self.content.width = self.length
            self.content.height = self.thickness

            self.content.controls = [
                self.slider_transparent,
                self.slider_background,
                self.slider_foreground
            ]

        elif self.orientation == 'vertical':
            self.slider_foreground.height = self.value_to_position() if self.value else self.thickness
            self.content.width = self.thickness
            self.content.height = self.length

            self.content.controls = [
                self.slider_transparent,
                self.slider_background,
                Column(
                    controls=[
                        self.slider_foreground
                    ],
                    alignment=MainAxisAlignment.END
                )
            ]

    def value_to_position(self):
        value_range = self.max - self.min
        available_range = self.length - self.thickness
        relative_value = self.value - self.min
        return relative_value / value_range * available_range + self.thickness

    def position_to_value(self, pos):
        value_range = self.max - self.min
        available_range = self.length - self.thickness
        return pos * value_range / available_range + self.min

    def update_value(self, value):
        self.value = value
        if callable(self.on_change):
            self.on_change(self.value)

    def get_clipped_position(self, value):
        return sorted([0, value - self.thickness / 2, self.length - self.thickness])[1]

    def round_to_nearest_n(self, value):
        base = (self.length - self.thickness) / self.divisions
        return base * round(value / base)

    def slide_horizontal(self, e):
        position_x = self.get_clipped_position(e.local_x)
        value = self.round_to_nearest_n(position_x) if self.divisions else position_x
        self.slider_foreground.width = value + self.thickness
        return value

    def slide_vertical(self, e):
        position_y = self.get_clipped_position(e.local_y)
        value = self.length - self.round_to_nearest_n(position_y) if self.divisions else self.length - position_y
        self.slider_foreground.height = value
        return value - self.thickness

    def update_slider(self, e):
        if callable(selected_orientation := self.valid_orientations.get(self.orientation)):
            position = selected_orientation(e)
            self.update_value(self.position_to_value(position))
            self.slider_foreground.update()
            self.disable_animation(e)

    def enable_animation(self, e):
        self.slider_foreground.animate = self.animate
        self.slider_foreground.update()

    def disable_animation(self, e):
        self.slider_foreground.animate = None
