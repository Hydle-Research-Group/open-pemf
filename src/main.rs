#![no_std]
#![no_main]

use defmt::*;
use defmt_rtt as _;
use embassy_executor::Spawner;
use embassy_rp::{
    gpio::{self, AnyPin, Input, Pull},
    i2c::{Async, I2c, InterruptHandler},
    peripherals::I2C0,
    uart::{Blocking, Uart},
};
use embassy_time::Timer;
use gpio::{Level, Output};
use openpemf::{
    display::Frame,
    firmware::{SessionState, UIState},
};
use panic_probe as _;

embassy_rp::bind_interrupts!(struct Irqs {
    I2C0_IRQ => InterruptHandler<embassy_rp::peripherals::I2C0>;
});

// States
const SESSION_STATE: SessionState = SessionState::new();
const UI_STATE: UIState = UIState::new();

// Addresses
const DISPLAY_ADDRESS: u16 = 0x3c;

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
    let en_pin = Output::new(p.PIN_17.into::<AnyPin>(), Level::Low);
    let step_pin = Output::new(p.PIN_18.into::<AnyPin>(), Level::Low);
    let dir_pin = Output::new(p.PIN_19.into::<AnyPin>(), Level::Low);

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

#[embassy_executor::task]
async fn generate_pulses(
    mut tmc2209_uart: Uart<'static, Blocking>,
    coil_en_pin: Input<'static>,
    mut enable_pin: Output<'static>,
    mut step_pin: Output<'static>,
    mut dir_pin: Output<'static>,
) {
}

#[embassy_executor::task]
async fn read_control_knob_rotation() {}

#[embassy_executor::task]
async fn read_control_knob_click() {}

#[embassy_executor::task]
async fn draw_ui(mut display_driver: I2c<'static, I2C0, Async>) {
    let mut frame = Frame::new();

    loop {
        frame.clear(); // clear on every pass
        UI_STATE.draw(&mut frame, &SESSION_STATE); // draw the ui

        if let Ok(()) = display_driver
            .write_async(DISPLAY_ADDRESS, frame.buffer())
            .await
        {
            info!("Writing to display");
        } else {
            error!("Writing display bytes failed");
        }

        Timer::after_millis(100).await; // re-draw every 100ms
    }
}
