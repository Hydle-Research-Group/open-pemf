/// The active (current) screen to display.
pub enum ActiveScreen {
    SessionConfig,
    Session,
    Error,
}

/// A screen's UI.
///
/// This trait contains a set of methods for UI rendering and control knob actions, including:
///
/// - `click`: a single control knob click
/// - `knob_up`: a single turn of the control knob left or "up"
/// - `knob_down`: a single turn of the control knob right or "down"
/// - `element_count`: the number of elements in the ui
pub trait Screen {
    /// The control knob was clicked.
    fn click(&mut self);

    /// The control knob was rotated up.
    fn knob_up(&mut self);

    /// The control knob was rotated down.
    fn knob_down(&mut self);

    /// The number of vertical scrollable UI elements.
    fn element_count(&self) -> u8;

    /// The current cursor position (0-255)
    fn cursor_position(&self) -> u8;
}

/// The session configuration UI.
pub struct SessionConfigUI {
    cursor_position: u8,
    controlling_duration: bool,
    controlling_level: bool,
    duration: u8, // 5, 10, 15, 20 min
    level: u8,    // 1 - 10
    started: bool,
}

impl Screen for SessionConfigUI {
    fn click(&mut self) {
        if self.controlling_duration {
            self.controlling_duration = false;
        }

        if self.controlling_level {
            self.controlling_level = false;
        }

        if self.cursor_position == 0 {
            self.controlling_duration = true;
        } else if self.cursor_position == 1 {
            self.controlling_level = true;
        }

        if self.cursor_position == self.element_count() - 1 {
            self.started = true;
        }
    }

    fn knob_up(&mut self) {
        if self.controlling_duration && self.duration <= 15 {
            self.duration += 5;

            return;
        }

        if self.controlling_level && self.level < 10 {
            self.level += 1;

            return;
        }

        if self.cursor_position < self.element_count() - 1 {
            self.cursor_position += 1;
        }
    }

    fn knob_down(&mut self) {
        if self.controlling_duration && self.duration >= 10 {
            self.duration -= 5;

            return;
        }

        if self.controlling_level && self.level > 1 {
            self.level += 1;

            return;
        }

        if self.cursor_position < self.element_count() - 1 {
            self.cursor_position += 1;
        }
    }

    fn element_count(&self) -> u8 {
        3
    }

    fn cursor_position(&self) -> u8 {
        self.cursor_position
    }
}

impl SessionConfigUI {
    /// Constructs a new `SessionConfigUI`.
    pub const fn new() -> Self {
        Self {
            cursor_position: 0,
            controlling_duration: false,
            controlling_level: false,
            duration: 5,
            level: 1,
            started: false,
        }
    }

    /// Returns the duration of the session (in seconds)
    pub fn duration_seconds(&self) -> u16 {
        self.duration as u16 * 60
    }

    /// Returns the level of the session (in the range 1-10)
    pub fn level(&self) -> u8 {
        self.level
    }

    /// Returns if the session was started (`true` if started, else `false`)
    pub fn started(&self) -> bool {
        self.started
    }
}

/// The session UI.
pub struct SessionUI {
    cursor_position: u8,
    stopped: bool,
    sleep_mode: bool,
}

impl Screen for SessionUI {
    fn click(&mut self) {
        if self.sleep_mode {
            self.sleep_mode = false; // wake screen up

            return;
        }

        if self.cursor_position == 0 {
            self.sleep_mode = true;
        } else if self.cursor_position == 1 {
            self.stopped = true;
        }
    }

    fn knob_up(&mut self) {
        if self.cursor_position < self.element_count() - 1 {
            self.cursor_position += 1;
        }
    }

    fn knob_down(&mut self) {
        if self.cursor_position > 0 {
            self.cursor_position -= 1;
        }
    }

    fn element_count(&self) -> u8 {
        2
    }

    fn cursor_position(&self) -> u8 {
        self.cursor_position
    }
}

impl SessionUI {
    /// Constructs a new `SessionUI`.
    pub const fn new() -> Self {
        Self {
            cursor_position: 0,
            stopped: false,
            sleep_mode: false,
        }
    }

    /// Returns if the session was stopped (`true` if stopped, else `false`)
    pub fn stopped(&self) -> bool {
        self.stopped
    }

    /// Returns if the sleep mode is enabled (`true` if enabled, else `false`)
    pub fn sleep_mode(&self) -> bool {
        self.sleep_mode
    }
}
