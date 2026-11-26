class Widget:
    """
    A widget class.

    The `Widget` object encapsulates methods for click events and knob rotations. It maintains the focus state of the widget.
    """

    def __init__(self):
        super().__init__()

        self._has_focus = False

    def clicked(self):
        """
        The widget was clicked.
        """

        self._has_focus = not self._has_focus

    def clockwise(self):
        """
        The encoder was turned clockwise on the widget.
        """

        pass

    def counterclockwise(self):
        """
        The encoder was turned clockwise on the widget.
        """

        pass

    def has_focus(self) -> bool:
        """
        Returns if the widget is in focus.
        """

        return self._has_focus


class Label(Widget):
    """
    A label widget.

    The `Label` widget renders a string of text.
    """

    def __init__(self, text: str):
        """
        Construct a new `Label` object.

        - `text`: the text of the label
        """
        super().__init__()

        self._text = text

    def has_focus(self) -> bool:
        return False  # can never focus on a label

    def set_text(self, text: str):
        """
        Set the text of the label.
        """

        self._text = text

    def text(self) -> str:
        """
        Returns the text of the label.
        """

        return self._text


class Button(Widget):
    """
    A button widget.

    The `Button` widget renders a section of "clickable" text that can trigger an optional callback.
    """

    def __init__(self, text: str, callback: callable | None = None):
        """
        Construct a new `Button` object.

        - `text`: the text of the button
        - `callable`: the optional function to call when the button is clicked (no arguments are passed to this callback)
        """
        super().__init__()

        self._text = text
        self._callback = callback

    def clicked(self):
        if self._callback:
            self._callback()

    def has_focus(self) -> bool:
        return False  # can never focus on a button

    def text(self) -> str:
        """
        Returns the text of the button.
        """

        return self._text


class IntegerAdjuster(Widget):
    """
    An integer adjusting widget.

    The `IntegerAdjuster` widget renders both text and an integer value. When it is clicked on, the value becomes editable. Clockwise movements cause the value to increase, and counter-clockwise movements cause the value to decrease.
    """

    def __init__(
        self,
        value: int,
        prefix: str = "",
        suffix: str = "",
        increment: int = 1,
        min: int = 0,
        max: int = 1000000,
        callback: callable | None = None,
    ):
        """
        Construct a new `IntegerAdjuster` object.

        - `value`: the initial value
        - `prefix`: the text to display before the internal value
        - `suffix`: the text to display after the internal value
        - `increment`: the increment amount (this determines is how much is added/subtracted when values are changed)
        - `min`: the minimum amount (never exceeded)
        - `max`: the maximum amount (never exceeded)
        - `callback`: the optional function to call when the value is changed (the integer value of the adjuster is passed as an argument)
        """
        super().__init__()

        self._value = value
        self._prefix = prefix
        self._suffix = suffix
        self._increment = increment
        self._min = min
        self._max = max
        self._callback = callback

    def clicked(self):
        super().clicked()

        if not self.has_focus() and self._callback:
            self._callback(self._value)

    def clockwise(self):
        if self._value + self._increment <= self._max:
            self._value += self._increment
        else:
            self._value = self._max

    def counterclockwise(self):
        if self._value - self._increment >= self._min:
            self._value -= self._increment
        else:
            self._value = self._min

    def value(self) -> int:
        """
        Returns the value of the integer adjuster.
        """

        return self._value

    def prefix(self) -> str:
        """
        Returns the prefix text of the integer adjuster.
        """

        return self._prefix

    def suffix(self) -> str:
        """
        Returns the suffix text of the integer adjuster.
        """

        return self._suffix
