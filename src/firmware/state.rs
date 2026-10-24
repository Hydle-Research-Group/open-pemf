use crate::display::{ActiveScreen, Frame, Screen, SessionConfigUI, SessionUI};

/// The session state of the firmware.
///
/// During user sessions, the firmware will poll from a global `SessionState` to run
/// session related actions.
pub struct SessionState {
    session_on: bool,
    session_sleeping: bool,
    session_level: u8,
    session_remaining_time: u16, // in seconds
}

impl SessionState {
    /// Constructs a new `SessionState`.
    pub const fn new() -> Self {
        Self {
            session_on: false,
            session_sleeping: false,
            session_level: 0,
            session_remaining_time: 0,
        }
    }

    /// Set the session state on or off.
    ///
    /// - `on`: the session state (`true` for on, `false` for off)
    pub fn set_session_on(&mut self, on: bool) {
        self.session_on = on;
    }

    /// Set the session state's sleep mode.
    ///
    /// - `sleeping`: the session state's sleep mode (`true` for on, `false` for off)
    ///
    /// If `true`, the session will not pause, rather the screen will be turned off temporarily.
    pub fn set_session_sleeping(&mut self, sleeping: bool) {
        self.session_sleeping = sleeping;
    }

    /// Set the session level.
    ///
    /// - `level`: the session level (in the range 1-10)
    pub fn set_session_level(&mut self, level: u8) {
        self.session_level = level;
    }

    /// Set the session's remaining time.
    ///
    /// - `time`: the session's remaining time (in seconds)
    pub fn set_session_remaining_time(&mut self, time: u16) {
        self.session_remaining_time = time;
    }

    /// Returns if the session is on (`true` if on, else `false`).
    pub fn session_on(&self) -> bool {
        self.session_on
    }

    /// Returns if the session is sleeping (`true` if sleeping, else `false`).
    pub fn session_sleeping(&self) -> bool {
        self.session_sleeping
    }

    /// Returns the session level (1-10)
    pub fn session_level(&self) -> u8 {
        self.session_level
    }

    /// Returns the session's remaining time (in seconds)
    pub fn session_remaining_time(&self) -> u16 {
        self.session_remaining_time
    }
}

/// The UI state of the firmware.
///
/// During display rendering and control knob changes, the firmware will poll from a global `UIState` to
/// render the appropriate interface. Additionally, the `UIState` modifies a global `SessionState` based
/// on actions sent from the UI.
pub struct UIState {
    active_screen: ActiveScreen,
    session_config_ui: SessionConfigUI,
    session_ui: SessionUI,
    error: &'static str,
}

impl UIState {
    /// Constructs a new `UIState`.
    pub const fn new() -> Self {
        Self {
            active_screen: ActiveScreen::SessionConfig,
            session_config_ui: SessionConfigUI::new(),
            session_ui: SessionUI::new(),
            error: "",
        }
    }

    /// A click event on the UI.
    ///
    /// - `session_state`: a global `SessionState` to modify depending on click events.
    pub fn clicked(&mut self, session_state: &mut SessionState) {
        match self.active_screen {
            ActiveScreen::Session => {
                self.session_ui.click();

                session_state.set_session_on(self.session_ui.stopped());
                session_state.set_session_sleeping(self.session_ui.sleep_mode());
            }
            ActiveScreen::SessionConfig => {
                self.session_config_ui.click();

                session_state.set_session_on(self.session_config_ui.started());
                session_state.set_session_level(self.session_config_ui.level());
                session_state.set_session_remaining_time(self.session_config_ui.duration_seconds());
            }
            ActiveScreen::Error => {
                self.active_screen = ActiveScreen::SessionConfig;
            }
        }
    }

    /// A control knob up event on the UI.
    pub fn knob_up(&mut self) {
        match self.active_screen {
            ActiveScreen::Session => self.session_ui.knob_up(),
            ActiveScreen::SessionConfig => self.session_config_ui.knob_up(),
            ActiveScreen::Error => {}
        }
    }

    /// A control knob down event on the UI.
    pub fn knob_down(&mut self) {
        match self.active_screen {
            ActiveScreen::Session => self.session_ui.knob_down(),
            ActiveScreen::SessionConfig => self.session_config_ui.knob_down(),
            ActiveScreen::Error => {}
        }
    }

    /// Draw the active user-interface on a `Frame` object.
    ///
    /// - `frame`: the `Frame` to draw on
    /// - `session_state`: a referenced `SessionState` to obtain session info
    pub fn draw(&self, frame: &mut Frame, session_state: &SessionState) {
        match self.active_screen {
            ActiveScreen::Session => {
                // frame.draw_text("  Remaining Time: ", (0, 0));
                // frame.draw_text("  Sleep", (0, 9));
                // frame.draw_text("  Stop Session", (0, 18));
            }
            ActiveScreen::SessionConfig => {
                // frame.draw_text("  Session Duration:", (0, 0));
                // frame.draw_text("  Session Level:", (0, 9));
                // frame.draw_text("  Start Session", (0, 18));
            }
            ActiveScreen::Error => {
                frame.draw_text(self.error, (0, 0));
            }
        }
    }

    /// Display the session UI.
    pub fn display_session(&mut self) {
        self.active_screen = ActiveScreen::Session;
    }

    /// Display the session configuration UI.
    pub fn display_session_config(&mut self) {
        self.active_screen = ActiveScreen::SessionConfig;
    }

    /// Display the error UI.
    ///
    /// - `message`: the error message to display
    pub fn display_error(&mut self, message: &'static str) {
        self.error = message;
        self.active_screen = ActiveScreen::Error;
    }
}
