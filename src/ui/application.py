import time

from machine import I2C, Pin

from src.ui.screen import Screen
from src.ui.sh1106 import SH1106_I2C


class Application:
    """
    An application.

    The `Application` is the primary holder of the display, encoder logic, and active screen (`Screen`).

    *It is up to the developer to implement the drawing loop. `Application.update()` is never ran internally.
    """

    def __init__(
        self, display_i2c: I2C, encoder_push: Pin, encoder_a: Pin, encoder_b: Pin
    ):
        """
        Construct a new `Application` object.

        - `display_i2c`: the display's `I2C` communication
        - `encoder_push`: the encoder push button input
        - `encoder_a`: the rotary encoder "A" phase input
        - `encoder_b`: the rotary encoder "B" phase input
        """
        super().__init__()

        self._encoder_push = encoder_push
        self._encoder_a = encoder_a
        self._encoder_b = encoder_b

        self._encoder_state = (self._encoder_a.value() << 1) | self._encoder_b.value()
        self._encoder_delta = 0

        # quadrature transition table.
        #
        # index = (previous_state << 2) | new_state
        #
        # valid clockwise transitions:
        #   00 -> 01 -> 11 -> 10 -> 00
        #
        # valid counter-clockwise transitions:
        #   00 -> 10 -> 11 -> 01 -> 00
        #
        # everything else is an invalid/bounced transition.
        self._encoder_table = (
            0,  # 00 -> 00
            1,  # 00 -> 01
            -1,  # 00 -> 10
            0,  # 00 -> 11
            -1,  # 01 -> 00
            0,  # 01 -> 01
            0,  # 01 -> 10 (invalid)
            1,  # 01 -> 11
            1,  # 10 -> 00
            0,  # 10 -> 01 (invalid)
            0,  # 10 -> 10
            -1,  # 10 -> 11
            0,  # 11 -> 00 (invalid)
            -1,  # 11 -> 01
            1,  # 11 -> 10
            0,  # 11 -> 11
        )

        # configure interrupts
        self._encoder_push.irq(
            handler=lambda _: self.encoder_clicked(),
            trigger=Pin.IRQ_FALLING,
        )
        self._encoder_a.irq(
            handler=lambda _: self.encoder_rotated(),
            trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING,
        )
        self._encoder_b.irq(
            handler=lambda _: self.encoder_rotated(),
            trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING,
        )

        self._active_screen = None
        self._display = SH1106_I2C(128, 64, display_i2c)
        self._display.init_display()
        self._display.flip()

        self._last_encoder_click = 0

    def set_active_screen(self, screen: Screen):
        """
        Set the active screen.

        - `screen`: the `Screen` object to display
        """

        self._active_screen = screen

    def encoder_clicked(self):
        """
        The rotary encoder was pressed.
        """

        now = time.ticks_ms()

        if time.ticks_diff(now, self._last_encoder_click) < 200:
            return

        self._last_encoder_click = now

        if self._active_screen:
            self._active_screen.clicked()

    def encoder_rotated(self):
        """
        The rotary encoder was rotated.
        """

        new_state = (self._encoder_a.value() << 1) | self._encoder_b.value()

        # look up the direction of this transition
        transition = (self._encoder_state << 2) | new_state

        self._encoder_delta += self._encoder_table[transition]

        # store state for the next interrupt
        self._encoder_state = new_state

        if self._encoder_delta >= 4:
            self._encoder_delta = 0

            if self._active_screen:
                self._active_screen.counterclockwise()

        elif self._encoder_delta <= -4:
            self._encoder_delta = 0

            if self._active_screen:
                self._active_screen.clockwise()

    def update(self):
        """
        Draw the active screen and update the display.
        """

        if self._active_screen:
            self._active_screen.draw(self._display)

        self._display.show()
