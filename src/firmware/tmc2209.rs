//! Interact with a TMC2209's registers over UART.
use embassy_rp::uart::{Blocking, Error, Uart};

/// Calculate the TMC2209 UART CRC-8 checksum.
///
/// - `data`: the UART data buffer
pub fn tmc_crc8(data: &[u8]) -> u8 {
    let mut crc: u8 = 0;

    for &byte in data {
        let mut current = byte;

        for _ in 0..8 {
            let mix = ((crc >> 7) ^ (current & 1)) & 1;
            crc <<= 1;

            if mix != 0 {
                crc ^= 0x07;
            }

            current >>= 1;
        }
    }

    crc
}

/// Write a 32-bit register to a TMC2209.
///
/// - `uart`: the blocking UART peripheral
/// - `address`: the TMC2209 address
/// - `register`: the TMC2209 register
/// - `value`: the bits to write on `register`
pub fn tmc_write_register(
    uart: &mut Uart<'static, Blocking>,
    address: u8,
    register: u8,
    value: u32,
) -> Result<(), Error> {
    let mut packet = [
        0x05,                     // Sync byte
        address,                  // Driver address
        0x80 | (register & 0x7F), // Register address + write flag
        (value >> 24) as u8,
        (value >> 16) as u8,
        (value >> 8) as u8,
        value as u8,
        0, // CRC
    ];

    packet[7] = tmc_crc8(&packet[..7]);

    uart.blocking_write(&packet)
}

/// Construct the 32-bit register for a TMC2209's `IHOLD`, `IRUN`, `IHOLDDELAY` configuration.
///
/// - `ihold`: the holding current (0-31)
/// - `irun`: the running current (0-31)
/// - `iholddelay`: the delay current (0-31)
pub fn tmc_ix(ihold: u8, irun: u8, iholddelay: u8) -> u32 {
    let value = (((iholddelay & 0x0F) as u32) << 16)
        | (((irun & 0x1F) as u32) << 8)
        | ((ihold & 0x1F) as u32);

    value
}
