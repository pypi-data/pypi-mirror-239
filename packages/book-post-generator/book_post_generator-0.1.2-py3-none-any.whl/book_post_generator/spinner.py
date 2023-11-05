import threading
import itertools
import sys


class Spinner:
    """Class to show a spinner in the command line to indicate a process is running."""

    def __init__(self, message="..."):
        """Initialize the spinner with a custom message.

        Args:
            message (str, optional): The message to display next to the spinner. Defaults to "...".
        """
        self.signal = threading.Event()
        self.message = message
        self.thread = threading.Thread(target=self.spin)
        self.thread.daemon = True  # Ensure thread is stopped if the program exits.

    def spin(self):
        """Spin the spinner in the command line until stopped."""
        write, flush = sys.stdout.write, sys.stdout.flush
        for char in itertools.cycle("|/-\\"):  # Cycle through spinner states
            status = f"{char} {self.message}"
            write(status)
            flush()
            write("\x08" * len(status))  # Move cursor back to start of line
            if self.signal.wait(0.1):  # Briefly wait for a stop signal
                break
        write(" " * len(status) + "\x08" * len(status))  # Clear the spinner

    def start(self):
        """Start the spinner in a separate thread."""
        self.signal.clear()  # Clear any existing stop signals
        self.thread.start()  # Start the spinner thread

    def stop(self):
        """Stop the spinner and wait for the spinner thread to finish."""
        self.signal.set()  # Send stop signal to spinner thread
        self.thread.join()  # Wait for the spinner thread to finish

    def __enter__(self):
        """Start the spinner when used as a context manager."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Stop the spinner when exiting the context manager scope."""
        self.stop()
        # If an exception occurred within the context, re-raise it.
        if exc_type:
            raise exc_value
