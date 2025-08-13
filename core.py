"""
NumPad - Core Logic Module

This module contains the core business logic for the typing accuracy test,
separated from the UI layer for better maintainability.
"""

import time
import random
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class TypingStats:
    """Data class to hold typing test statistics."""

    correct_chars: int = 0
    total_chars_typed: int = 0
    start_time: float = 0.0
    elapsed_time: float = 0.0

    @property
    def accuracy_percentage(self) -> float:
        """Calculate accuracy percentage."""
        if self.total_chars_typed == 0:
            return 0.0
        return (self.correct_chars / self.total_chars_typed) * 100

    @property
    def npm(self) -> float:
        """Calculate Numbers Per Minute (NPM)."""
        if self.elapsed_time <= 0:
            return 0.0
        # NPM: numbers typed per minute
        return self.total_chars_typed / (self.elapsed_time / 60)


class TypingTestEngine:
    """Core engine for the typing accuracy test."""

    def __init__(self, window_size: int = 2):
        """
        Initialize the typing test engine.

        Args:
            window_size: Number of digits to show around current position
        """
        self.window_size = window_size
        self.target_string: List[str] = []
        self.typed_chars: List[str] = []
        self.current_pos = 0
        self.stats = TypingStats()
        self.is_active = False

    def start_new_test(self) -> None:
        """Start a new typing test session."""
        self.reset_stats()
        self.generate_initial_sequence()
        self.stats.start_time = time.time()
        self.is_active = True

    def reset_stats(self) -> None:
        """Reset all statistics and game state."""
        self.stats = TypingStats()
        self.typed_chars = []
        self.current_pos = 0

    def generate_initial_sequence(self) -> None:
        """Generate initial sequence of random digits."""
        self.target_string = [
            self.get_random_digit() for _ in range(self.window_size * 2 + 1)
        ]

    def get_random_digit(self) -> str:
        """Generate a single random digit from 0-9."""
        return str(random.randint(0, 9))

    def process_input(self, user_char: str) -> bool:
        """
        Process user input character.

        Args:
            user_char: The character typed by the user

        Returns:
            bool: True if input was processed, False if invalid
        """
        if not self.is_active:
            return False

        # Only process digit input
        if not (len(user_char) == 1 and user_char.isdigit()):
            return False

        # Store input and update stats
        self.typed_chars.append(user_char)

        if user_char == self.target_string[self.current_pos]:
            self.stats.correct_chars += 1

        self.stats.total_chars_typed += 1
        self.current_pos += 1

        # Update elapsed time
        self.stats.elapsed_time = time.time() - self.stats.start_time

        # Check if we need to slide the window
        if self.current_pos >= self.window_size + 1:
            self.slide_window()

        return True

    def slide_window(self) -> None:
        """Slide the window and generate new digit."""
        self.target_string = self.target_string[1:]
        self.typed_chars = self.typed_chars[1:]
        self.current_pos -= 1
        self.target_string.append(self.get_random_digit())

    def get_display_data(self) -> Tuple[List[Tuple[str, str]], TypingStats]:
        """
        Get data for UI display.

        Returns:
            Tuple of (character_data, stats) where character_data is a list of
            (character, status) tuples. Status can be 'correct', 'incorrect',
            'current', or 'future'.
        """
        char_data = []

        for i, char in enumerate(self.target_string):
            if i < self.current_pos:
                # Already typed characters
                if i < len(self.typed_chars):
                    status = (
                        "correct"
                        if self.typed_chars[i] == char
                        else "incorrect"
                    )
                else:
                    status = "future"
            elif i == self.current_pos:
                # Current character to type
                status = "current"
            else:
                # Future characters
                status = "future"

            char_data.append((char, status))

        return char_data, self.stats

    def stop_test(self) -> None:
        """Stop the current test."""
        self.is_active = False
        if self.stats.start_time > 0:
            self.stats.elapsed_time = time.time() - self.stats.start_time
