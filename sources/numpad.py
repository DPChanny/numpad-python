"""
NumPad - GUI Application

A Tkinter-based GUI application for practicing numeric keypad typing.
Supports cross-platform operation (Windows, macOS, Linux).
"""

import tkinter as tk
from tkinter import ttk
import platform
import sys
import os
from pathlib import Path

# Add the current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from core import TypingTestEngine
from characters import CharacterManager
from style import StyleManager
from widgets import DigitDisplay, StatisticsPanel


class NumPadApp:
    """Main application class for NumPad."""

    def __init__(self):
        """Initialize the application."""
        self.root = tk.Tk()
        self.engine = TypingTestEngine()
        self.digit_display = None  # Will be initialized in setup_ui
        self.stats_panel = None  # Will be initialized in setup_ui
        self.setup_ui()
        self.setup_bindings()
        self.engine.start_new_test()  # Auto-start
        self.digit_display.initialize_labels(self.engine.get_display_data()[0])
        self.update_display()

    def setup_ui(self):
        """Set up the user interface."""
        self.root.title("NumPad")
        self.root.geometry("500x500")
        self.root.resizable(True, True)
        self.root.minsize(500, 500)

        # Configure style based on OS
        self.setup_os_specific_styling()

        # Main frame with responsive layout
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights for responsive design
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)  # Make display area expandable

        # Title
        title_label = ttk.Label(
            main_frame, text="NumPad", font=("Arial", 24, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 20))

        # Display frame for numbers with individual digit labels
        self.display_frame = ttk.Frame(main_frame)
        self.display_frame.grid(
            row=1, column=0, pady=(0, 20), sticky=(tk.W, tk.E, tk.N, tk.S)
        )
        self.display_frame.columnconfigure(0, weight=1)
        self.display_frame.rowconfigure(0, weight=1)

        # Container for digit labels with fixed background to prevent flicker
        self.digits_container = tk.Frame(
            self.display_frame, bg=StyleManager.COLORS["background"]
        )
        self.digits_container.grid(row=0, column=0)

        # Initialize digit display
        self.digit_display = DigitDisplay(self.digits_container)

        # Stats panel
        self.stats_panel = StatisticsPanel(main_frame)
        self.stats_panel.grid(
            row=2, column=0, pady=(0, 20), sticky=(tk.W, tk.E)
        )

        # Reset button only
        self.reset_button = ttk.Button(
            main_frame, text="Reset (R)", command=self.reset_test
        )
        self.reset_button.grid(row=3, column=0, pady=(0, 20))

        # Instructions
        instructions = """Type the highlighted character • Press R to reset"""
        instructions_label = ttk.Label(
            main_frame, text=instructions, font=("Arial", 10), justify=tk.CENTER
        )
        instructions_label.grid(row=4, column=0)

    def setup_os_specific_styling(self):
        """Configure OS-specific styling and fonts."""
        system = platform.system()

        if system == "Darwin":  # macOS
            # macOS specific styling
            self.root.configure(bg="#f0f0f0")
        elif system == "Windows":
            # Windows specific styling
            try:
                # Use native Windows styling if available
                self.root.tk.call("source", "azure.tcl")
                ttk.Style().theme_use("azure")
            except:
                pass
        else:  # Linux and others
            # Linux specific styling
            pass

    def setup_bindings(self):
        """Set up keyboard bindings."""
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<Button-1>", lambda e: self.root.focus_set())
        self.root.focus_set()

        # Make sure the window can receive focus
        self.root.bind("<FocusIn>", lambda e: self.root.focus_set())

    def on_key_press(self, event):
        """Handle key press events."""
        if CharacterManager.is_valid_input(event.char):
            self.engine.process_input(event.char)
            # Only update display immediately for user input
            self.update_display_immediate()
        elif event.char.lower() == "r":
            self.reset_test()

    def reset_test(self):
        """Reset the current test."""
        self.engine.reset_stats()
        self.engine.generate_initial_sequence()
        self.engine.start_new_test()  # Auto-restart
        self.digit_display.initialize_labels(self.engine.get_display_data()[0])
        self.update_display_immediate()
        self.root.focus_set()

    def update_display_immediate(self):
        """Update display immediately for user input."""
        char_data, stats = self.engine.get_display_data()

        # Update digit labels efficiently
        self.digit_display.update_labels(char_data)

        # Update statistics
        self.stats_panel.update_stats(stats)

    def update_display(self):
        """Update the display with current test data (periodic update)."""
        if self.engine.is_active:
            char_data, stats = self.engine.get_display_data()

            # Only update statistics periodically (not digits, to avoid flicker)
            self.stats_panel.update_stats(stats)

            # Schedule next update with longer interval
            self.root.after(500, self.update_display)

    def run(self):
        """Start the application main loop."""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()


def main():
    """Main entry point for the application."""
    try:
        app = NumPadApp()
        app.run()
    except Exception as e:
        # Handle any startup errors gracefully
        if "tkinter" in str(e).lower():
            print("Error: Tkinter is not available. Please install tkinter.")
            if platform.system() == "Linux":
                print("On Ubuntu/Debian: sudo apt-get install python3-tk")
                print("On CentOS/RHEL: sudo yum install tkinter")
        else:
            print(f"Error starting application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
