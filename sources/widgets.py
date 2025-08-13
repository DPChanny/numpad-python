"""
UI Widgets module for NumPad application.
Contains reusable UI components and widget management.
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Tuple, Optional
from style import StyleManager, CharacterStyle


class DigitDisplay:
    """Manages the display of digit labels with efficient updating."""

    def __init__(self, parent_container: tk.Widget):
        """Initialize the digit display."""
        self.container = parent_container
        self.labels: List[tk.Label] = []
        self.last_char_data: List[Tuple[str, str]] = []

    def initialize_labels(self, char_data: List[Tuple[str, str]]):
        """Initialize digit labels with proper styling."""
        self.clear_labels()

        for i, (char, status) in enumerate(char_data):
            style = StyleManager.get_style(status)
            font = StyleManager.get_font_tuple(style)

            label = tk.Label(
                self.container,
                text=char,
                font=font,
                bg=style.bg_color,
                fg=style.fg_color,
                width=2,
                relief="solid",
                borderwidth=style.border_width,
            )
            label.grid(row=0, column=i, padx=2, pady=10)
            self.labels.append(label)

        self.last_char_data = list(char_data)

    def update_labels(self, char_data: List[Tuple[str, str]]):
        """Update labels efficiently - only change what's necessary."""
        # Adjust number of labels if needed
        self._adjust_label_count(char_data)

        # Batch all label updates
        updates_needed = self._calculate_updates(char_data)

        # Apply all updates at once
        self._apply_updates(updates_needed)

        # Hide extra labels if sequence got shorter
        self._hide_extra_labels(len(char_data))

        # Cache current data
        self.last_char_data = list(char_data)

    def _adjust_label_count(self, char_data: List[Tuple[str, str]]):
        """Ensure we have enough labels for the character data."""
        while len(self.labels) < len(char_data):
            # Add new label with default styling
            style = StyleManager.get_style("future")
            font = StyleManager.get_font_tuple(style)

            label = tk.Label(
                self.container,
                text="",
                font=font,
                bg=style.bg_color,
                fg=style.fg_color,
                width=2,
                relief="solid",
                borderwidth=style.border_width,
            )
            label.grid(row=0, column=len(self.labels), padx=2, pady=10)
            self.labels.append(label)

    def _calculate_updates(
        self, char_data: List[Tuple[str, str]]
    ) -> List[Tuple[int, str, CharacterStyle]]:
        """Calculate which labels need updating."""
        updates_needed = []

        for i, (char, status) in enumerate(char_data):
            if i >= len(self.labels):
                break

            # Check if this label needs updating
            need_update = i >= len(self.last_char_data) or self.last_char_data[
                i
            ] != (char, status)

            if need_update:
                style = StyleManager.get_style(status)
                updates_needed.append((i, char, style))

        return updates_needed

    def _apply_updates(
        self, updates_needed: List[Tuple[int, str, CharacterStyle]]
    ):
        """Apply all label updates at once."""
        for i, char, style in updates_needed:
            font = StyleManager.get_font_tuple(style)
            self.labels[i].config(
                text=char, font=font, bg=style.bg_color, fg=style.fg_color
            )

    def _hide_extra_labels(self, active_count: int):
        """Hide labels that are no longer needed."""
        for i in range(active_count, len(self.labels)):
            self.labels[i].grid_remove()

    def clear_labels(self):
        """Clear all existing labels."""
        for label in self.labels:
            label.destroy()
        self.labels.clear()
        self.last_char_data.clear()


class StatisticsPanel:
    """Manages the statistics display panel."""

    def __init__(self, parent: tk.Widget):
        """Initialize the statistics panel."""
        self.frame = ttk.LabelFrame(parent, text="Statistics", padding="10")
        self.accuracy_var = tk.StringVar(value="0.00%")
        self.npm_var = tk.StringVar(value="0.00")
        self.chars_var = tk.StringVar(value="0 / 0")
        self.time_var = tk.StringVar(value="0.00s")

        self._setup_labels()

    def _setup_labels(self):
        """Set up the statistics labels."""
        self.frame.columnconfigure(1, weight=1)

        # Accuracy
        ttk.Label(self.frame, text="Accuracy:").grid(
            row=0, column=0, sticky=tk.W, padx=(0, 10)
        )
        ttk.Label(
            self.frame,
            textvariable=self.accuracy_var,
            font=("Arial", 12, "bold"),
        ).grid(row=0, column=1, sticky=tk.W)

        # NPM
        ttk.Label(self.frame, text="NPM:").grid(
            row=1, column=0, sticky=tk.W, padx=(0, 10)
        )
        ttk.Label(
            self.frame, textvariable=self.npm_var, font=("Arial", 12, "bold")
        ).grid(row=1, column=1, sticky=tk.W)

        # Characters
        ttk.Label(self.frame, text="Characters:").grid(
            row=2, column=0, sticky=tk.W, padx=(0, 10)
        )
        ttk.Label(
            self.frame, textvariable=self.chars_var, font=("Arial", 12, "bold")
        ).grid(row=2, column=1, sticky=tk.W)

        # Time
        ttk.Label(self.frame, text="Time:").grid(
            row=3, column=0, sticky=tk.W, padx=(0, 10)
        )
        ttk.Label(
            self.frame, textvariable=self.time_var, font=("Arial", 12, "bold")
        ).grid(row=3, column=1, sticky=tk.W)

    def update_stats(self, stats):
        """Update all statistics displays."""
        self.accuracy_var.set(f"{stats.accuracy_percentage:.2f}%")
        self.npm_var.set(f"{stats.npm:.2f}")
        self.chars_var.set(f"{stats.correct_chars} / {stats.total_chars_typed}")
        self.time_var.set(f"{stats.elapsed_time:.2f}s")

    def grid(self, **kwargs):
        """Grid the statistics frame."""
        self.frame.grid(**kwargs)
