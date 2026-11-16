class SessionState:
    """
    Session state.
    """

    def __init__(
        self,
    ):
        super().__init__()

        self._device_enabled = False
        self._remaining_time = 0

    def set_device_enabled(self, enabled: bool):
        """
        Set the device enabled.

        - `enabled`: `True` if the device is enabled, else `False`
        """

        self._device_enabled = enabled

    def set_remaining_time(self, sec: int):
        """
        Set the session time (in seconds)

        - `sec`: the time in seconds
        """

        self._remaining_time = sec

    def device_enabled(self) -> bool:
        """
        Returns if the device is enabled (`True` if enabled, else `False`).
        """

        return self._device_enabled

    def remaining_time(self) -> int:
        """
        Returns the remaining time of the session (in seconds)
        """

        return self._remaining_time
