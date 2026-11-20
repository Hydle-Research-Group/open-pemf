from src.ui.sh1106 import SH1106_I2C
from src.ui.widgets import Button, IntegerAdjuster, Label, Widget

VERTICAL_SPACING = 14


class Screen:
    """
    A screen.

    The `Screen` object renders a list of `Widget` objects vertically, determining which are focused or clicked. It tracks the position of the cursor, ensuring it never exceeds the number of widgets.
    """

    def __init__(self, scrollable: bool = True):
        """
        Construct a new `Screen` object.

        - `scrollable`: if the screen is scrollable (i.e. the cursor position is displayed)
        """
        super().__init__()

        self._scrollable = scrollable
        self._cursor_position = 0
        self._widgets: list[Widget] = []

    def add_widget(self, widget: Widget):
        """
        Add a widget to the widget list.

        - `widget`: the `Widget` object to add
        """

        self._widgets.append(widget)

    def clicked(self):
        """
        The screen was clicked.
        """

        widget = self._widgets[self._cursor_position]
        widget.clicked()

    def clockwise(self):
        """
        The encoder was turned clockwise on the screen.
        """

        widget = self._widgets[self._cursor_position]

        if widget.has_focus():
            widget.clockwise()
        else:
            if self._cursor_position < len(self._widgets) - 1:
                self._cursor_position += 1

    def counterclockwise(self):
        """
        The encoder was turned counter-clockwise on the screen.
        """

        widget = self._widgets[self._cursor_position]

        if widget.has_focus():
            widget.counterclockwise()
        else:
            if self._cursor_position > 0:
                self._cursor_position -= 1

    def draw(self, display: SH1106_I2C):
        """
        Draw the widgets on the provided display.

        - `display`: the display to write to
        """

        display.fill(0)

        x = 2
        y = 1

        for i, widget in enumerate(self._widgets):
            y_spacing = y + i * VERTICAL_SPACING

            if i == self._cursor_position and self._scrollable:
                # display a line indicating "in focus"
                if widget.has_focus():
                    display.line(
                        0,
                        i * VERTICAL_SPACING,
                        0,
                        i * VERTICAL_SPACING + 10,
                        color=1,
                    )
                else:
                    display.rect(0, i * VERTICAL_SPACING, 128, 10, color=1)

            if isinstance(widget, (Label, Button)):
                display.text(widget.text(), x, y_spacing)
            elif isinstance(widget, IntegerAdjuster):
                text = widget.text()

                # if the text is not empty, draw the field after the text
                if text:
                    display.text(f"{text}: {widget.value()}", x, y_spacing)
                else:
                    display.text(str(widget.value()), x, y_spacing)
