"""
LlamaPhone - Retro CRT TV Styles
Styling for the nostalgic tube TV aesthetic
"""

# CSS template strings use {variable} syntax

# CRT Color Palette
COLORS = {
    # Phosphor Colors
    "phosphor_green": "#66FF7A",
    "phosphor_amber": "#FF4BD8",
    "phosphor_blue": "#3AD9FF",
    "phosphor_red": "#FF4A8B",
    "phosphor_cyan": "#48F8FF",

    # Cabinet Colors
    "cabinet_dark": "#0B0F23",
    "cabinet_medium": "#161A3A",
    "cabinet_light": "#2A1E57",
    "cabinet_highlight": "#3D2D78",
    "cabinet_edge": "#46D8FF",

    # Screen Colors
    "screen_black": "#07120F",
    "screen_glow": "#133422",
    "scanline": "rgba(0, 0, 0, 0.3)",

    # Button Colors
    "button_normal": "#201B44",
    "button_hover": "#302965",
    "button_pressed": "#151132",
    "button_led_off": "#2A1036",
    "button_led_on": "#FF4BD8",

    # Text Colors
    "text_primary": "#33FF33",
    "text_secondary": "#FFB000",
    "text_dim": "#4DAE77",
    "text_error": "#FF3333",

    # Status Colors
    "status_good": "#33FF33",
    "status_warning": "#FF4BD8",
    "status_error": "#FF4A8B",
    "status_info": "#3AD9FF",
}

# Typography
FONTS = {
    "terminal": "Courier New",
    "display": "Impact",
    "button": "Arial",
    "mono": "Consolas",
}

# Font Sizes
FONT_SIZES = {
    "title": 24,
    "heading": 18,
    "body": 14,
    "small": 12,
    "tiny": 10,
}


def get_crt_stylesheet():
    """Get the complete CRT TV stylesheet."""
    return f"""
/* ==================== MAIN WINDOW ==================== */
QMainWindow {{
    background: qradialgradient(cx:0.5, cy:0.3, radius:1.1,
        stop:0 {COLORS['cabinet_light']},
        stop:0.45 {COLORS['cabinet_medium']},
        stop:1 {COLORS['cabinet_dark']});
    border: none;
}}

/* ==================== TV CABINET FRAME ==================== */
#tvFrame {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #341C7E,
        stop:0.5 #1A1E5A,
        stop:1 {COLORS['cabinet_dark']});
    border-radius: 20px;
    border: 3px solid {COLORS['cabinet_edge']};
    padding: 10px;
}}

/* ==================== SCREEN CONTAINER ==================== */
#screenContainer {{
    background-color: {COLORS['screen_black']};
    border-radius: 15px;
    border: 4px solid {COLORS['cabinet_edge']};
    padding: 5px;
}}

/* ==================== CRT SCREEN WITH EFFECTS ==================== */
#crtScreen {{
    background: qradialgradient(cx:0.5, cy:0.5, radius:0.9,
        stop:0 #4BFF6A,
        stop:0.45 #2AAE51,
        stop:1 {COLORS['screen_black']});
    border-radius: 10px;
    padding: 15px;
}}

/* CRT Scanline Overlay */
#crtScreen::before {{
    border-image: none;
    background: repeating-linear-gradient(
        0deg,
        rgba(0, 0, 0, 0.2) 0px,
        rgba(0, 0, 0, 0.2) 1px,
        transparent 1px,
        transparent 2px
    );
}}

/* CRT Vignette Effect */
#crtScreen::after {{
    border-image: none;
    background: radial-gradient(
        ellipse at center,
        transparent 60%,
        rgba(0, 0, 0, 0.4) 100%
    );
    border-radius: 10px;
}}

/* ==================== TEXT EDIT / TERMINAL ==================== */
QTextEdit, QPlainTextEdit {{
    background-color: rgba(8, 18, 15, 220);
    color: {COLORS['phosphor_green']};
    border: 2px solid #3AD9FF;
    border-radius: 8px;
    padding: 10px;
    font-family: '{FONTS['terminal']}', monospace;
    font-size: {FONT_SIZES['body']}px;
    selection-background-color: {COLORS['phosphor_green']};
    selection-color: {COLORS['screen_black']};
}}

QTextEdit:hover, QPlainTextEdit:hover {{
    border: 2px solid {COLORS['phosphor_green']};
}}

/* ==================== LINE EDIT / INPUT ==================== */
QLineEdit {{
    background-color: {COLORS['screen_black']};
    color: {COLORS['phosphor_amber']};
    border: 2px solid {COLORS['cabinet_edge']};
    border-radius: 5px;
    padding: 8px 12px;
    font-family: '{FONTS['terminal']}', monospace;
    font-size: {FONT_SIZES['body']}px;
    selection-background-color: {COLORS['phosphor_amber']};
}}

QLineEdit:focus {{
    border: 2px solid {COLORS['phosphor_green']};
}}

QLineEdit::placeholder {{
    color: {COLORS['text_dim']};
}}

/* ==================== PUSH BUTTONS (TV BUTTONS) ==================== */
QPushButton {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {COLORS['button_normal']},
        stop:0.5 {COLORS['cabinet_medium']},
        stop:1 {COLORS['button_pressed']});
    color: #FF70DF;
    border: 2px solid #2CCEFF;
    border-radius: 8px;
    padding: 10px 15px;
    font-family: '{FONTS['button']}', sans-serif;
    font-size: {FONT_SIZES['small']}px;
    font-weight: bold;
    min-width: 80px;
    min-height: 35px;
}}

QPushButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {COLORS['button_hover']},
        stop:0.5 {COLORS['cabinet_light']},
        stop:1 {COLORS['button_normal']});
    color: #5DFF89;
}}

QPushButton:pressed {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {COLORS['button_pressed']},
        stop:0.5 {COLORS['cabinet_dark']},
        stop:1 {COLORS['button_pressed']});
    padding-top: 12px;
    padding-bottom: 8px;
}}

QPushButton:disabled {{
    background: {COLORS['cabinet_dark']};
    color: {COLORS['text_dim']};
    border: 2px solid {COLORS['cabinet_medium']};
}}

/* LED Indicator on Buttons */
QPushButton LED {{
    background-color: {COLORS['button_led_off']};
    border-radius: 4px;
}}

/* ==================== TOOL BUTTONS (SMALLER) ==================== */
QToolButton {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {COLORS['button_normal']},
        stop:1 {COLORS['button_pressed']});
    color: {COLORS['phosphor_blue']};
    border: 2px solid {COLORS['cabinet_edge']};
    border-radius: 5px;
    padding: 5px 10px;
    font-family: '{FONTS['button']}', sans-serif;
    font-size: {FONT_SIZES['tiny']}px;
}}

QToolButton:hover {{
    color: {COLORS['phosphor_green']};
    border: 2px solid {COLORS['phosphor_green']};
}}

/* ==================== SCROLL BAR ==================== */
QScrollBar:vertical {{
    background: {COLORS['cabinet_dark']};
    width: 15px;
    margin: 3px;
    border-radius: 7px;
}}

QScrollBar::handle:vertical {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {COLORS['cabinet_medium']},
        stop:0.5 {COLORS['cabinet_light']},
        stop:1 {COLORS['cabinet_medium']});
    border-radius: 5px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: {COLORS['phosphor_green']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background: {COLORS['cabinet_dark']};
    height: 15px;
    margin: 3px;
    border-radius: 7px;
}}

QScrollBar::handle:horizontal {{
    background: {COLORS['cabinet_medium']};
    border-radius: 5px;
    min-width: 30px;
}}

/* ==================== COMBO BOX (DROPDOWN) ==================== */
QComboBox {{
    background-color: {COLORS['cabinet_medium']};
    color: {COLORS['phosphor_amber']};
    border: 2px solid {COLORS['cabinet_edge']};
    border-radius: 5px;
    padding: 5px 10px;
    font-family: '{FONTS['button']}', sans-serif;
}}

QComboBox:hover {{
    border: 2px solid {COLORS['phosphor_green']};
}}

QComboBox::drop-down {{
    border: none;
    width: 25px;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 8px solid {COLORS['phosphor_amber']};
}}

QComboBox QAbstractItemView {{
    background-color: {COLORS['cabinet_dark']};
    color: {COLORS['phosphor_green']};
    border: 2px solid {COLORS['phosphor_green']};
    selection-background-color: {COLORS['phosphor_green']};
    selection-color: {COLORS['screen_black']};
}}

/* ==================== TAB WIDGET ==================== */
QTabWidget::pane {{
    background-color: {COLORS['screen_black']};
    border: 2px solid {COLORS['cabinet_edge']};
    border-radius: 5px;
}}

QTabBar::tab {{
    background-color: {COLORS['cabinet_medium']};
    color: {COLORS['phosphor_amber']};
    padding: 8px 20px;
    margin-right: 2px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
}}

QTabBar::tab:selected {{
    background-color: rgba(7, 18, 15, 220);
    color: #5DFF89;
    border-bottom: 2px solid #5DFF89;
}}

QTabBar::tab:hover:!selected {{
    background-color: {COLORS['cabinet_light']};
    color: {COLORS['phosphor_green']};
}}

/* ==================== PROGRESS BAR ==================== */
QProgressBar {{
    background-color: {COLORS['cabinet_dark']};
    border: 2px solid {COLORS['cabinet_edge']};
    border-radius: 5px;
    height: 20px;
    text-align: center;
    color: {COLORS['phosphor_green']};
    font-family: '{FONTS['terminal']}', monospace;
}}

QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {COLORS['phosphor_green']},
        stop:1 {COLORS['phosphor_cyan']});
    border-radius: 3px;
}}

/* ==================== MENU BAR ==================== */
QMenuBar {{
    background-color: {COLORS['cabinet_medium']};
    color: {COLORS['phosphor_amber']};
    border-bottom: 2px solid {COLORS['cabinet_edge']};
}}

QMenuBar::item:selected {{
    background-color: {COLORS['phosphor_green']};
    color: {COLORS['screen_black']};
}}

QMenu {{
    background-color: {COLORS['cabinet_dark']};
    color: {COLORS['phosphor_green']};
    border: 2px solid {COLORS['cabinet_edge']};
}}

QMenu::item:selected {{
    background-color: {COLORS['phosphor_green']};
    color: {COLORS['screen_black']};
}}

/* ==================== TOOL TIP ==================== */
QToolTip {{
    background-color: {COLORS['cabinet_dark']};
    color: {COLORS['phosphor_amber']};
    border: 2px solid {COLORS['phosphor_green']};
    padding: 5px;
    border-radius: 3px;
    font-family: '{FONTS['terminal']}', monospace;
}}

/* ==================== STATUS BAR ==================== */
QStatusBar {{
    background-color: #0E1230;
    color: #FF70DF;
    border-top: 2px solid #2CCEFF;
}}

QStatusBar::item {{
    border: none;
}}

/* ==================== SPLASH SCREEN ==================== */
#splashFrame {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {COLORS['cabinet_light']},
        stop:0.5 {COLORS['cabinet_medium']},
        stop:1 {COLORS['cabinet_dark']});
    border-radius: 30px;
    border: 5px solid {COLORS['cabinet_edge']};
}}

#splashScreen {{
    background-color: {COLORS['screen_black']};
    border-radius: 20px;
    border: 3px solid {COLORS['phosphor_green']};
}}

/* ==================== DIALOG ==================== */
QDialog {{
    background-color: {COLORS['cabinet_medium']};
}}

/* ==================== GROUP BOX ==================== */
QGroupBox {{
    background-color: {COLORS['cabinet_dark']};
    color: {COLORS['phosphor_amber']};
    border: 2px solid {COLORS['cabinet_edge']};
    border-radius: 8px;
    margin-top: 10px;
    padding: 10px;
    font-family: '{FONTS['button']}', sans-serif;
    font-weight: bold;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 10px;
    color: {COLORS['phosphor_green']};
}}

/* ==================== LIST WIDGET ==================== */
QListWidget {{
    background-color: {COLORS['screen_black']};
    color: {COLORS['phosphor_green']};
    border: 2px solid {COLORS['cabinet_edge']};
    border-radius: 5px;
    padding: 5px;
    font-family: '{FONTS['terminal']}', monospace;
}}

QListWidget::item:selected {{
    background-color: {COLORS['phosphor_green']};
    color: {COLORS['screen_black']};
}}

QListWidget::item:hover {{
    background-color: {COLORS['screen_glow']};
}}

/* ==================== TABLE WIDGET ==================== */
QTableWidget {{
    background-color: {COLORS['screen_black']};
    color: {COLORS['phosphor_green']};
    border: 2px solid {COLORS['cabinet_edge']};
    gridline-color: {COLORS['cabinet_medium']};
    font-family: '{FONTS['terminal']}', monospace;
}}

QHeaderView::section {{
    background-color: {COLORS['cabinet_medium']};
    color: {COLORS['phosphor_amber']};
    padding: 5px;
    border: 1px solid {COLORS['cabinet_edge']};
    font-weight: bold;
}}

/* ==================== CHECK BOX ==================== */
QCheckBox {{
    color: {COLORS['phosphor_green']};
    spacing: 10px;
    font-family: '{FONTS['button']}', sans-serif;
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border: 2px solid {COLORS['phosphor_green']};
    border-radius: 3px;
    background-color: {COLORS['screen_black']};
}}

QCheckBox::indicator:checked {{
    background-color: {COLORS['phosphor_green']};
    image: none;
}}

QCheckBox::indicator:checked:after {{
    content: '✓';
    color: {COLORS['screen_black']};
    font-weight: bold;
}}

/* ==================== RADIO BUTTON ==================== */
QRadioButton {{
    color: {COLORS['phosphor_green']};
    spacing: 10px;
    font-family: '{FONTS['button']}', sans-serif;
}}

QRadioButton::indicator {{
    width: 18px;
    height: 18px;
    border: 2px solid {COLORS['phosphor_green']};
    border-radius: 9px;
    background-color: {COLORS['screen_black']};
}}

QRadioButton::indicator:checked {{
    background-color: {COLORS['phosphor_green']};
}}

QRadioButton::indicator:checked:after {{
    width: 8px;
    height: 8px;
    border-radius: 4px;
    background-color: {COLORS['screen_black']};
    margin: 3px;
}}
"""


def get_knob_stylesheet():
    """Get stylesheet for rotary knob controls."""
    return f"""
QDial {{
    background-color: {COLORS['cabinet_dark']};
    border: 3px solid {COLORS['cabinet_edge']};
    border-radius: 30px;
}}

QDial::groove:vertical {{
    border: none;
    height: 50px;
    margin: 20px;
    background: {COLORS['cabinet_medium']};
    border-radius: 5px;
}}

QDial::handle:vertical {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {COLORS['cabinet_light']},
        stop:0.5 {COLORS['cabinet_highlight']},
        stop:1 {COLORS['cabinet_medium']});
    height: 20px;
    width: 20px;
    border-radius: 10px;
    border: 2px solid {COLORS['cabinet_edge']};
    margin: -5px 15px;
}}

QSlider::handle:horizontal {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {COLORS['cabinet_light']},
        stop:0.5 {COLORS['cabinet_highlight']},
        stop:1 {COLORS['cabinet_medium']});
    width: 20px;
    height: 20px;
    border-radius: 10px;
    border: 2px solid {COLORS['cabinet_edge']};
    margin: -5px 0;
}}
"""


def get_screen_effect_styles():
    """Get CSS-style effects for the CRT screen."""
    return """
    /* Scanline Overlay */
    .scanlines {
        pointer-events: none;
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: repeating-linear-gradient(
            0deg,
            rgba(0, 0, 0, 0.15),
            rgba(0, 0, 0, 0.15) 1px,
            transparent 1px,
            transparent 2px
        );
        z-index: 1000;
        border-radius: inherit;
    }

    /* Phosphor Glow */
    .phosphor-glow {
        text-shadow: 0 0 5px currentColor, 0 0 10px currentColor;
    }

    /* Screen Flicker Animation */
    @keyframes flicker {
        0% { opacity: 0.98; }
        5% { opacity: 1.0; }
        10% { opacity: 0.97; }
        15% { opacity: 1.0; }
        100% { opacity: 1.0; }
    }

    .screen-flicker {
        animation: flicker 0.15s infinite;
    }

    /* CRT Curvature */
    .crt-curve {
        border-radius: 50% / 10%;
    }

    /* RGB Split Effect */
    @keyframes rgb-shift {
        0% { text-shadow: -1px 0 #ff0000, 1px 0 #00ffff; }
        50% { text-shadow: -2px 0 #ff0000, 2px 0 #00ffff; }
        100% { text-shadow: -1px 0 #ff0000, 1px 0 #00ffff; }
    }

    .rgb-split {
        animation: rgb-shift 0.1s infinite;
    }
    """


# CSS animations for the HTML components
CRT_ANIMATIONS = """
<style>
@keyframes warmup {
    0% { opacity: 0; transform: scale(0.8); }
    50% { opacity: 0.7; }
    100% { opacity: 1; transform: scale(1); }
}

@keyframes blink {
    0%, 50% { opacity: 1; }
    51%, 100% { opacity: 0; }
}

@keyframes scanline-move {
    0% { top: -100%; }
    100% { top: 100%; }
}

@keyframes glow-pulse {
    0%, 100% { text-shadow: 0 0 10px #33FF33, 0 0 20px #33FF33; }
    50% { text-shadow: 0 0 20px #33FF33, 0 0 40px #33FF33, 0 0 60px #33FF33; }
}

@keyframes static-noise {
    0% { background-position: 0 0; }
    100% { background-position: 100% 100%; }
}

.boot-text {
    animation: glow-pulse 2s infinite;
}

.cursor-blink {
    animation: blink 1s infinite;
}
</style>
"""
