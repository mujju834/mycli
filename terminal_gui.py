import tkinter as tk
from tkinter import scrolledtext
import os
import subprocess
import threading
import click
from cli import cli  # Import your CLI commands

class TerminalApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Mujju Command Terminal")
        self.geometry("900x600")

        # Initialize the current directory
        self.current_directory = os.getcwd()

        # Define custom styles
        self.font = ("Consolas", 12)  # A modern font like used in terminals
        self.bg_color = "#1e1e1e"  # Dark background for the terminal
        self.fg_color = "#00ff00"  # Green text, similar to classic terminals
        self.error_color = "#ff5555"  # Red text for errors

        # Scrolled text widget for output with custom styles
        self.output_text = scrolledtext.ScrolledText(
            self, wrap=tk.WORD, state=tk.DISABLED, font=self.font,
            bg=self.bg_color, fg=self.fg_color, insertbackground="white", relief=tk.FLAT
        )
        self.output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Entry widget for user input with matching styles
        self.command_entry = tk.Entry(self, font=self.font, bg=self.bg_color,
                                      fg="white", insertbackground="white", relief=tk.FLAT)
        self.command_entry.pack(fill=tk.X, padx=10, pady=5)
        self.command_entry.bind("<Return>", self.run_command)  # Run command on Enter key
        self.command_entry.focus()  # Set focus on the entry field at startup

        # Display welcome message and initial directory
        self.show_output(f"Welcome to the Mujju Command Terminal!\n", "info")
        self.show_output(f"Current Directory: {self.current_directory}\n", "info")
        self.show_output("Type 'exit' to quit.\n", "info")

    def run_command(self, event=None):
        """Handle the user's command input."""
        command = self.command_entry.get().strip()
        if not command:
            return

        # Clear the entry field
        self.command_entry.delete(0, tk.END)

        # Display the command in the output area
        self.show_output(f"{self.current_directory}> {command}\n", "command")

        # Handle the 'exit' command
        if command.lower() == "exit":
            self.show_output("Exiting the terminal...\n", "info")
            self.quit()
            return

        # Handle the 'cd' command to change directories
        if command.startswith("cd "):
            self.change_directory(command)
            return

        # Run the command asynchronously in a separate thread
        threading.Thread(target=self.execute_system_command, args=(command,), daemon=True).start()

    def change_directory(self, command):
        """Change the current working directory."""
        try:
            path = command.split(" ", 1)[1].strip()  # Extract the path from 'cd' command
            os.chdir(path)
            self.current_directory = os.getcwd()
            self.show_output(f"Changed directory to: {self.current_directory}\n", "info")
        except IndexError:
            self.show_output("Usage: cd <directory>\n", "error")
        except FileNotFoundError:
            self.show_output(f"Directory not found: {path}\n", "error")
        except Exception as e:
            self.show_output(f"Error: {e}\n", "error")

    def execute_system_command(self, command):
        """Execute a system command and display the output."""
        try:
            result = subprocess.run(
                command, capture_output=True, text=True, shell=True, cwd=self.current_directory
            )

            # Display stdout and stderr output
            if result.stdout:
                self.show_output(result.stdout, "info")
            if result.stderr:
                self.show_output(result.stderr, "error")

            # If no output, display a success message for certain commands
            if not result.stdout and not result.stderr:
                if command.startswith("mkdir"):
                    folder_name = command.split(" ", 1)[1].strip()
                    self.show_output(f"Folder '{folder_name}' created successfully.\n", "info")
                elif command.startswith("rmdir"):
                    folder_name = command.split(" ", 1)[1].strip()
                    self.show_output(f"Folder '{folder_name}' removed successfully.\n", "info")
                elif command.startswith("del") or command.startswith("rm"):
                    self.show_output("File deleted successfully.\n", "info")

        except Exception as e:
            self.show_output(f"Error: {e}\n", "error")

    def show_output(self, text, tag):
        """Display output in the scrolled text widget with color coding."""
        self.output_text.config(state=tk.NORMAL)  # Enable editing to insert text
        self.output_text.insert(tk.END, text, tag)  # Insert text at the end
        self.output_text.config(state=tk.DISABLED)  # Disable editing again
        self.output_text.see(tk.END)  # Scroll to the end

    def setup_tags(self):
        """Setup color tags for different types of output."""
        self.output_text.tag_config("info", foreground=self.fg_color)
        self.output_text.tag_config("error", foreground=self.error_color)
        self.output_text.tag_config("command", foreground="white")


if __name__ == "__main__":
    app = TerminalApp()
    app.setup_tags()  # Set up color tags for styled output
    app.mainloop()
