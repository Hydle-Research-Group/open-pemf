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
remaining_label = Label("")


def start_session(app: Application, session_ui: Screen):
    """
    Start a session, enabling the device and swapping the active screen to the "Session" UI.
    """

    SESSION_STATE.set_device_enabled(True)

    level = session_level_control.value()

    if level == 1:
        SESSION_STATE.set_remaining_time(5 * 60)
    elif level == 2:
        SESSION_STATE.set_remaining_time(15 * 60)
    else:
        SESSION_STATE.set_remaining_time(20 * 60)

    app.set_active_screen(session_ui)


def stop_session(app: Application, default: Screen):
    """
    Stop a session, disabling the device and swapping the screen back to `default`.
    """

    SESSION_STATE.set_device_enabled(False)

    app.set_active_screen(default)


async def session_timer_task():
    """
    The session timer task.

    This task decrements `SESSION_STATE`'s remaining time by 1 every second, editing a global `remaining_label` to display the current time.
    """

    while True:
        if SESSION_STATE.remaining_time() > 0:
            remaining = SESSION_STATE.remaining_time() - 1
            remaining_label.set_text(
                f"{int(remaining / 60):02}:{remaining % 60:02} Remaining"
            )

            await asyncio.sleep(1)

            SESSION_STATE.set_remaining_time(remaining)
        else:
            await asyncio.sleep_ms(10)


async def session_task():
    """
    The session task.

    This task sends 30Hz pulses to the on-board TMC2209 driver, ensuring the device is properly connected and enabled before doing so.

    Additionally, the task controls the IRUN current value of the TMC2209, matching a linear relationship with elapsed time.
    """

    en_pin = Pin(17, Pin.OUT, value=1)
    step_pin = Pin(18, Pin.OUT, value=0)
    dir_pin = Pin(19, Pin.OUT, value=0)

    # uart commuication
    tmc2209_uart = UART(1, baudrate=115200, tx=Pin(20), rx=Pin(21))

    while True:
        if (
            SESSION_STATE.device_enabled()
            and SESSION_STATE.connected()
            and SESSION_STATE.remaining_time() > 0
        ):
            en_pin.off()  # enable the driver

            config = tmc_ix(
                16, int((SESSION_STATE.remaining_time() / 60) * 1.6) - 1, 16
            )
            tmc_write_register(
                tmc2209_uart, address=TMC2209_ADDRESS, register=0x10, value=config
            )

            step_pin.on()
            await asyncio.sleep_ms(33)
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
    error_ui = Screen(scrollable=False)

    session_config_ui.add_widget(session_level_control)
    session_config_ui.add_widget(
        Button("Start Session", callback=lambda: start_session(app, session_ui))
    )
    session_ui.add_widget(remaining_label)
    session_ui.add_widget(
        Button("Stop Session", callback=lambda: stop_session(app, session_config_ui))
    )
    error_ui.add_widget(Label("Connect device"))
    error_ui.add_widget(Label("to begin"))

    asyncio.create_task(session_timer_task())
    asyncio.create_task(session_task())

    while True:
        app.update()

        if not SESSION_STATE.connected():
            app.set_active_screen(error_ui)

            continue  # freeze in a busy loop until the device is plugged in

        if SESSION_STATE.remaining_time() == 0:
            app.set_active_screen(session_config_ui)

        # the ui is redrawn every 1ms (1000Hz)
        await asyncio.sleep_ms(1)


asyncio.run(main())
