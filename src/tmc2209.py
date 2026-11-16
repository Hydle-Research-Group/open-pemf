from machine import UART


def tmc_crc8(data: bytes) -> int:
    """Calculate the TMC2209 UART CRC-8 checksum."""

    crc = 0

    for byte in data:
        current = byte

        for _ in range(8):
            mix = ((crc >> 7) ^ (current & 1)) & 1
            crc = (crc << 1) & 0xFF

            if mix:
                crc ^= 0x07

            current >>= 1

    return crc


def tmc_write_register(
    uart: UART,
    address: int,
    register: int,
    value: int,
) -> None:
    """Write a 32-bit register to a TMC2209."""

    packet = bytearray(
        [
            0x05,  # Sync byte
            address,  # Driver address
            0x80 | (register & 0x7F),  # Register address + write flag
            (value >> 24) & 0xFF,
            (value >> 16) & 0xFF,
            (value >> 8) & 0xFF,
            value & 0xFF,
            0,  # CRC
        ]
    )

    packet[7] = tmc_crc8(packet[:7])

    uart.write(packet)


def tmc_ix(
    ihold: int,
    irun: int,
    iholddelay: int,
) -> int:
    """Construct the IHOLD_IRUN register value."""

    value = ((iholddelay & 0x0F) << 16) | ((irun & 0x1F) << 8) | (ihold & 0x1F)

    return value
