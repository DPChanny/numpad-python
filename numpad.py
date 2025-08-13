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


class NumPadApp:
    """Main application class for NumPad."""

    def __init__(self):
        """Initialize the application."""
        self.root = tk.Tk()
        self.engine = TypingTestEngine()
        self.digit_labels = []  # Store individual digit labels for coloring
        self.setup_ui()
        self.setup_bindings()
        self.engine.start_new_test()  # Auto-start
        self.update_display()

    def setup_ui(self):
        """Set up the user interface."""
        self.root.title("NumPad")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        self.root.minsize(400, 300)

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

        # Container for digit labels
        self.digits_container = ttk.Frame(self.display_frame)
        self.digits_container.grid(row=0, column=0)

        # Stats frame
        stats_frame = ttk.LabelFrame(
            main_frame, text="Statistics", padding="10"
        )
        stats_frame.grid(row=2, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        stats_frame.columnconfigure(1, weight=1)

        # Stats labels
        ttk.Label(stats_frame, text="Accuracy:").grid(
            row=0, column=0, sticky=tk.W, padx=(0, 10)
        )
        self.accuracy_var = tk.StringVar(value="0.00%")
        ttk.Label(
            stats_frame,
            textvariable=self.accuracy_var,
            font=("Arial", 12, "bold"),
        ).grid(row=0, column=1, sticky=tk.W)

        ttk.Label(stats_frame, text="NPM:").grid(
            row=1, column=0, sticky=tk.W, padx=(0, 10)
        )
        self.npm_var = tk.StringVar(value="0.00")
        ttk.Label(
            stats_frame, textvariable=self.npm_var, font=("Arial", 12, "bold")
        ).grid(row=1, column=1, sticky=tk.W)

        ttk.Label(stats_frame, text="Characters:").grid(
            row=2, column=0, sticky=tk.W, padx=(0, 10)
        )
        self.chars_var = tk.StringVar(value="0 / 0")
        ttk.Label(
            stats_frame, textvariable=self.chars_var, font=("Arial", 12, "bold")
        ).grid(row=2, column=1, sticky=tk.W)

        ttk.Label(stats_frame, text="Time:").grid(
            row=3, column=0, sticky=tk.W, padx=(0, 10)
        )
        self.time_var = tk.StringVar(value="0.00s")
        ttk.Label(
            stats_frame, textvariable=self.time_var, font=("Arial", 12, "bold")
        ).grid(row=3, column=1, sticky=tk.W)

        # Reset button only
        self.reset_button = ttk.Button(
            main_frame, text="Reset (R)", command=self.reset_test
        )
        self.reset_button.grid(row=3, column=0, pady=(0, 20))

        # Instructions
        instructions = """Type the highlighted number • Press R to reset"""
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
        if event.char.isdigit():
            self.engine.process_input(event.char)
            self.update_display()
        elif event.char.lower() == "r":
            self.reset_test()

    def reset_test(self):
        """Reset the current test."""
        self.engine.reset_stats()
        self.engine.generate_initial_sequence()
        self.engine.start_new_test()  # Auto-restart
        self.update_display()
        self.root.focus_set()

    def create_digit_labels(self, char_data):
        """Create individual digit labels for color highlighting."""
        # Clear existing labels
        for label in self.digit_labels:
            label.destroy()
        self.digit_labels.clear()

        # Create new labels for each digit
        for i, (char, status) in enumerate(char_data):
            # Define colors based on status
            if status == "current":
                bg_color = "#FFD700"  # Gold
                fg_color = "#000000"  # Black
                font_weight = "bold"
            elif status == "correct":
                bg_color = "#90EE90"  # Light Green
                fg_color = "#000000"  # Black
                font_weight = "normal"
            elif status == "incorrect":
                bg_color = "#FFB6C1"  # Light Pink
                fg_color = "#000000"  # Black
                font_weight = "normal"
            else:  # future
                bg_color = "#F0F0F0"  # Light Gray
                fg_color = "#000000"  # Black
                font_weight = "normal"

            label = tk.Label(
                self.digits_container,
                text=char,
                font=("Courier New", 48, font_weight),
                bg=bg_color,
                fg=fg_color,
                width=2,
                relief="solid",
                borderwidth=1,
            )
            label.grid(row=0, column=i, padx=2, pady=10)
            self.digit_labels.append(label)

    def update_display(self):
        """Update the display with current test data."""
        char_data, stats = self.engine.get_display_data()

        # Update digit labels with highlighting
        self.create_digit_labels(char_data)

        # Update statistics
        self.accuracy_var.set(f"{stats.accuracy_percentage:.2f}%")
        self.npm_var.set(f"{stats.npm:.2f}")
        self.chars_var.set(f"{stats.correct_chars} / {stats.total_chars_typed}")
        self.time_var.set(f"{stats.elapsed_time:.2f}s")

        # Schedule next update if test is active
        if self.engine.is_active:
            self.root.after(100, self.update_display)

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
