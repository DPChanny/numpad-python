"""
Character management module for NumPad application.
Handles character generation and validation.
"""

import random
from typing import List


class CharacterManager:
    """Manages character generation and validation for typing practice."""

    # Character sets
    DIGITS = "0123456789"
    OPERATORS = "+-*/"
    SPECIAL = "."

    # Combined character set for numpad
    NUMPAD_CHARS = DIGITS + OPERATORS + SPECIAL

    @classmethod
    def get_random_character(cls) -> str:
        """Generate a random character from the numpad character set."""
        return random.choice(cls.NUMPAD_CHARS)

    @classmethod
    def is_valid_input(cls, char: str) -> bool:
        """Check if the character is a valid numpad input."""
        return len(char) == 1 and char in cls.NUMPAD_CHARS

    @classmethod
    def generate_sequence(cls, length: int) -> List[str]:
        """Generate a sequence of random characters."""
        return [cls.get_random_character() for _ in range(length)]
