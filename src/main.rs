#![no_std]
#![no_main]

use core::cell::RefCell;
use defmt::info;
use defmt_rtt as _;
use embassy_executor::Spawner;
use embassy_rp::{
    gpio::{self, AnyPin, Input, Pull},
    i2c::{Async, I2c, InterruptHandler},
    peripherals::I2C0,
    uart::{Blocking, Uart},
};
use embassy_sync::{blocking_mutex::raw::CriticalSectionRawMutex, mutex::Mutex};
use embassy_time::Timer;
use gpio::{Level, Output};
use openpemf::{
    display::Frame,
    firmware::{
        SessionState, UIState,
        tmc2209::{tmc_ix, tmc_write_register},
    },
};
use panic_probe as _;

embassy_rp::bind_interrupts!(struct Irqs {
    I2C0_IRQ => InterruptHandler<embassy_rp::peripherals::I2C0>;
});

// States
static SESSION_STATE: Mutex<CriticalSectionRawMutex, RefCell<SessionState>> =
    Mutex::new(RefCell::new(SessionState::new()));
static UI_STATE: Mutex<CriticalSectionRawMutex, RefCell<UIState>> =
    Mutex::new(RefCell::new(UIState::new()));

// Addresses
const DISPLAY_ADDRESS: u16 = 0x3c;
const TMC2209_ADDRESS: u8 = 0x00;

#[embassy_executor::main(
    executor = "embassy_rp::executor::Executor",
    entry = "cortex_m_rt::entry"
)]
async fn main(_spawner: Spawner) {
    let p = embassy_rp::init(Default::default());

    // driver communications
    let i2c_config = embassy_rp::i2c::Config::default();
    let uart_config = embassy_rp::uart::Config::default();
    let display_driver = I2c::new_async(p.I2C0, p.PIN_1, p.PIN_0, Irqs, i2c_config);
    let tmc2209_uart = Uart::new_blocking(p.UART1, p.PIN_20, p.PIN_21, uart_config); // blocking is ok, we only send commands to the driver occasionally

    // inputs
    let coil_en_pin = Input::new(p.PIN_16, Pull::Up);

    // outputs
    let en_pin = Output::new(p.PIN_17.into::<AnyPin>(), Level::High);
    let step_pin = Output::new(p.PIN_18.into::<AnyPin>(), Level::Low);
    let dir_pin = Output::new(p.PIN_19.into::<AnyPin>(), Level::Low);

    _spawner.spawn(session_timer().unwrap());
    _spawner.spawn(generate_pulses(tmc2209_uart, coil_en_pin, en_pin, step_pin, dir_pin).unwrap());
    _spawner.spawn(draw_ui(display_driver).unwrap());

    let mut led = Output::new(p.PIN_25, Level::Low);

    loop {
        info!("led on!");
        led.set_high();
        Timer::after_millis(500).await;

        info!("led off!");
        led.set_low();
        Timer::after_millis(500).await;
    }
}

/// Session timing task.
///
/// This task updates the global `SESSION_STATE`'s remaining time after every second,
/// decrementing the time by 1.
#[embassy_executor::task]
async fn session_timer() {
    loop {
        let session_state = SESSION_STATE.lock().await;
        let remaining = session_state.borrow().session_remaining_time();

        if session_state.borrow().session_on() && remaining > 0 {
            Timer::after_secs(1).await;

            session_state
                .borrow_mut()
                .set_session_remaining_time(remaining - 1);
        }
    }
}

/// Pulse generation task for the on-board TMC2209 driver.
///
/// This task sends the correct pulses to the STEP pin, while ensuring the EN pin
/// is set low when the session is enabled. Additionally, the task will also maintain the
/// current of the driver depending on what level is polled from the global `SESSION_STATE`.
#[embassy_executor::task]
async fn generate_pulses(
    mut uart: Uart<'static, Blocking>,
    coil_en_pin: Input<'static>,
    mut enable_pin: Output<'static>,
    mut step_pin: Output<'static>,
    mut dir_pin: Output<'static>,
) {
    dir_pin.set_low();

    loop {
        let session_state = SESSION_STATE.lock().await;
        let ui_state = UI_STATE.lock().await;

        if coil_en_pin.is_low() {
            ui_state
                .borrow_mut()
                .display_error("E01:\nDevice Disconnected");

            continue; // skip until the treatment device is connected
        }

        if session_state.borrow().session_on() {
            enable_pin.set_low(); // enable the driver
            ui_state.borrow_mut().display_session(); // display the session UI

            // coil current configuration
            let current_config = tmc_ix(16, session_state.borrow().session_level() * 3, 16);

            if let Ok(()) = tmc_write_register(&mut uart, TMC2209_ADDRESS, 0x10, current_config) {
                info!("TMC2209 current values configured");
            } else {
                ui_state.borrow_mut().display_error("E03:\nTMC2209 UART");
            }

            // single pulse, 30Hz total
            step_pin.set_high();
            Timer::after_millis(33).await;
            step_pin.set_low();
        } else {
            enable_pin.set_high(); // disabled
        }
    }
}

#[embassy_executor::task]
async fn read_control_knob_rotation() {}

#[embassy_executor::task]
async fn read_control_knob_click() {}

/// UI drawing task for the 1.3" OLED display.
///
/// This tasks sends the appropriate bytes (over I2C) to the display driver, depending
/// on what UI is being drawn.
#[embassy_executor::task]
async fn draw_ui(mut display_driver: I2c<'static, I2C0, Async>) {
    let mut frame = Frame::new();

    loop {
        frame.clear(); // clear on every pass

        let session_state = SESSION_STATE.lock().await;
        let ui_state = UI_STATE.lock().await;

        if !session_state.borrow().session_sleeping() {
            ui_state.borrow().draw(&mut frame, &session_state.borrow()); // draw the ui

            if let Ok(()) = display_driver
                .write_async(DISPLAY_ADDRESS, frame.buffer())
                .await
            {
                info!("Writing to display");
            } else {
                ui_state.borrow_mut().display_error("E02:\nDisplay Writing");
            }
        }

        Timer::after_millis(100).await; // re-draw every 100ms
    }
}
