"""
Style configuration module for NumPad application.
Defines colors, fonts, and other visual styling properties.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class CharacterStyle:
    """Style configuration for a character display."""

    bg_color: str
    fg_color: str
    font_weight: str
    font_size: int
    border_color: str = "#000000"
    border_width: int = 1


class StyleManager:
    """Manages all styling for the NumPad application."""

    # Font settings
    FONT_FAMILY = "Courier New"
    NORMAL_FONT_SIZE = 48
    CURRENT_FONT_SIZE = 56

    # Color definitions
    COLORS = {
        "current": "#FFD700",  # Gold
        "correct": "#90EE90",  # Light Green
        "incorrect": "#FFB6C1",  # Light Pink
        "future": "#F0F0F0",  # Light Gray
        "text": "#000000",  # Black
        "background": "#FFFFFF",  # White
    }

    # Character styles
    STYLES = {
        "current": CharacterStyle(
            bg_color=COLORS["current"],
            fg_color=COLORS["text"],
            font_weight="bold",
            font_size=CURRENT_FONT_SIZE,
        ),
        "correct": CharacterStyle(
            bg_color=COLORS["correct"],
            fg_color=COLORS["text"],
            font_weight="normal",
            font_size=NORMAL_FONT_SIZE,
        ),
        "incorrect": CharacterStyle(
            bg_color=COLORS["incorrect"],
            fg_color=COLORS["text"],
            font_weight="normal",
            font_size=NORMAL_FONT_SIZE,
        ),
        "future": CharacterStyle(
            bg_color=COLORS["future"],
            fg_color=COLORS["text"],
            font_weight="normal",
            font_size=NORMAL_FONT_SIZE,
        ),
    }

    @classmethod
    def get_style(cls, status: str) -> CharacterStyle:
        """Get style configuration for a given status."""
        return cls.STYLES.get(status, cls.STYLES["future"])

    @classmethod
    def get_font_tuple(cls, style: CharacterStyle) -> Tuple[str, int, str]:
        """Get font tuple for tkinter."""
        return (cls.FONT_FAMILY, style.font_size, style.font_weight)
