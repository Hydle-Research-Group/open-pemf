import asyncio

from machine import I2C, UART, Pin

from src.state import SessionState
from src.tmc2209 import tmc_ix, tmc_write_register
from src.ui.application import Application
from src.ui.screen import Screen
from src.ui.widgets import Button, IntegerAdjuster, Label

SESSION_STATE = SessionState(Pin(16, Pin.IN, Pin.PULL_DOWN))
TMC2209_ADDRESS = 0x00

# ui widgets
session_level_control = IntegerAdjuster(1, text="Level", min=1, max=3)
session_frequency_control = IntegerAdjuster(60, text="Frequency (Hz)", min=1, max=1000)
remaining_label = Label("")


def start_session(app: Application, session_ui: Screen, state: SessionState):
    """
    Start a session, enabling the device and swapping the active screen to the "Session" UI.
    """

    state.set_device_enabled(True)

    level = session_level_control.value()
    frequency = session_frequency_control.value()

    if level == 1:
        state.set_duration(5 * 60)
    elif level == 2:
        state.set_duration(15 * 60)
    else:
        state.set_duration(20 * 60)

    state.set_frequency(frequency)

    app.set_active_screen(session_ui)


def stop_session(state: SessionState):
    """
    Stop a session, disabling the device and swapping the screen back to `default`.
    """

    state.reset()


async def session_timer_task():
    """
    The session timer task.

    This task decrements SESSION_STATE's remaining time by 1 every second,
    editing a global remaining_label to display the current time.
    """

    while True:
        current = SESSION_STATE.current_time()

        if current > 0:
            remaining = current - 1
            SESSION_STATE.set_current_time(remaining)

            remaining_label.set_text(
                f"{int(remaining / 60):02}:{remaining % 60:02} Remaining"
            )

            await asyncio.sleep(1)
        else:
            await asyncio.sleep_ms(10)


async def session_task():
    """
    The session task.

    This task sends pulses to the on-board TMC2209 driver, ensuring the device is properly connected and enabled before doing so.

    Additionally, the task controls the IRUN current value of the TMC2209, matching a exponential relationship with elapsed time.
    """

    en_pin = Pin(17, Pin.OUT, value=1)
    step_pin = Pin(18, Pin.OUT, value=0)
    dir_pin = Pin(19, Pin.OUT, value=0)

    # uart commuication
    tmc2209_uart = UART(1, baudrate=115200, tx=Pin(20), rx=Pin(21))

    while True:
        if SESSION_STATE.device_enabled() and SESSION_STATE.current_time() > 0:
            en_pin.off()  # enable the driver

            # configure the TMC2209's current for this range of time
            minutes_normalized = 20 - (
                SESSION_STATE.duration() / 60 - SESSION_STATE.current_time() / 60
            )
            current_adj = (
                32 if minutes_normalized < 4 else round(32 / (minutes_normalized - 3))
            ) - 1

            config = tmc_ix(16, current_adj, 16)
            tmc_write_register(
                tmc2209_uart, address=TMC2209_ADDRESS, register=0x10, value=config
            )

            step_pin.on()
            await asyncio.sleep_ms(round(1000 / SESSION_STATE.frequency()))
            step_pin.off()
        else:
            en_pin.on()  # disable the driver

            await asyncio.sleep_ms(10)


async def main():
    app = Application(
        I2C(
            0,
            scl=Pin(1),
            sda=Pin(0),
            freq=400_000,
        ),
        Pin(2, Pin.IN, Pin.PULL_UP),
        Pin(3, Pin.IN, Pin.PULL_UP),
        Pin(4, Pin.IN, Pin.PULL_UP),
    )

    session_config_ui = Screen()
    session_ui = Screen()

    session_config_ui.add_widget(session_level_control)
    session_config_ui.add_widget(session_frequency_control)
    session_config_ui.add_widget(
        Button(
            "Start Session",
            callback=lambda: start_session(app, session_ui, SESSION_STATE),
        )
    )
    session_ui.add_widget(remaining_label)
    session_ui.add_widget(
        Button("Stop Session", callback=lambda: stop_session(SESSION_STATE))
    )

    asyncio.create_task(session_timer_task())
    asyncio.create_task(session_task())

    while True:
        app.update()

        if SESSION_STATE.current_time() == 0:
            app.set_active_screen(session_config_ui)

        # the ui is redrawn every 1ms (1000Hz)
        await asyncio.sleep_ms(1)


asyncio.run(main())
