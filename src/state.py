from machine import Pin


class SessionState:
    """
    The session state.
    """

    def __init__(self, device_connected_pin: Pin):
        """
        Construct a new `SessionState` object.

        - `device_connected_pin`: the low-pulled pin read to determine if the treatement coil is connected
        """
        super().__init__()

        self._device_connected_pin = device_connected_pin
        self._device_enabled = False
        self._duration = 0
        self._current_time = 0
        self._frequency = 60

    def reset(self):
        """
        Reset the session state.
        """

        self._device_enabled = False
        self._duration = 0
        self._current_time = 0

    def set_device_enabled(self, enabled: bool):
        """
        Set the device enabled.

        - `enabled`: `True` if the device is enabled, else `False`
        """

        self._device_enabled = enabled

    def set_duration(self, sec: int):
        """
        Set the session's duration (in seconds)

        - `sec`: the duration in seconds
        """

        self._duration = sec
        self._current_time = sec

    def set_current_time(self, sec: int):
        """
        Set the session's current time (in seconds)

        - `sec`: the time in seconds
        """

        self._current_time = sec

    def set_frequency(self, freq: int):
        """
        Set the session frequency (in hertz)

        - `freq`: the frequency in hertz
        """

        self._frequency = freq

    def connected(self) -> bool:
        """
        Returns if the treatment coil is connected (`True` if connected, else `False`)
        """

        return self._device_connected_pin.value() == 1

    def device_enabled(self) -> bool:
        """
        Returns if the device is enabled (`True` if enabled, else `False`).
        """

        return self._device_enabled

    def duration(self) -> int:
        """
        Returns the duration of the session (in seconds)
        """

        return self._duration

    def current_time(self) -> int:
        """
        Returns the current time of the session (in seconds)
        """

        return self._current_time

    def frequency(self) -> int:
        """
        Returns the frequency of the session (in hertz)
        """

        return self._frequency
