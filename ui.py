import tkinter as tk
from tkinter import messagebox, scrolledtext
from validator import InputValidator


class TrailLogger:
    """
    Simple helper that writes a numbered, sectioned solution trail
    into a tkinter text widget.

    Usage:
        logger = TrailLogger(text_widget)
        logger.clear()
        logger.heading("GIVEN")
        logger.add_step("some text")
        logger.add_step("next step")
    """
    def __init__(self, text_widget: tk.Text):
        self.text_widget = text_widget
        self.step_counter = 0

    def clear(self):
        """Erase the widget and reset numbering."""
        self.text_widget.delete("1.0", tk.END)
        self.step_counter = 0

    def heading(self, name: str):
        """Insert an un‑numbered heading.  The name is upper‑cased."""
        self.text_widget.insert(tk.END, f"\n=== {name.upper()} ===\n")

    def add_step(self, text: str):
        """
        Add a new step to the trail.  The step number is maintained
        automatically.  A multi‑line string will be indented on subsequent
        lines.
        """
        self.step_counter += 1
        lines = text.splitlines()
        # first line with number
        self.text_widget.insert(tk.END, f"{self.step_counter}. {lines[0]}\n")
        for line in lines[1:]:
            self.text_widget.insert(tk.END, f"    {line}\n")


class GaussianSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gaussian Elimination Solver (Placeholder)")
        self.root.geometry("900x700")

        # INPUT PANEL
        input_frame = tk.LabelFrame(root, text="Inputs", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Enter equations (2x2 or 3x3):").pack()
        tk.Label(input_frame, text="Press enter to add another equation").pack()
        self.eq_input = scrolledtext.ScrolledText(input_frame, height=6)
        self.eq_input.pack(fill="x")

        btn_frame = tk.Frame(input_frame)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Compute", command=self.compute_placeholder).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Clear", command=self.clear).pack(side="left", padx=5)

        # Solution Trail
        trail_frame = tk.LabelFrame(root, text="Solution Trail")
        trail_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.trail_output = scrolledtext.ScrolledText(trail_frame)
        self.trail_output.pack(fill="both", expand=True)

        # create the logger after the widget exists
        self.trail_logger = TrailLogger(self.trail_output)

        # Final Answer
        answer_frame = tk.LabelFrame(root, text="Final Answer")
        answer_frame.pack(fill="x", padx=10, pady=5)

        self.final_output = tk.Text(answer_frame, height=4)
        self.final_output.pack(fill="x")

    # Placeholder for solution trail
    def compute_placeholder(self):
        equations_text = self.eq_input.get("1.0", tk.END).strip()

        # start with a clean trail
        self.trail_logger.clear()
        self.final_output.delete("1.0", tk.END)

        # --- GIVEN ---
        self.trail_logger.heading("GIVEN")
        if equations_text:
            self.trail_logger.add_step("Equations entered by user:")
            # display the raw lines as a single multiline step
            self.trail_logger.add_step(equations_text)
        else:
            self.trail_logger.add_step("No equations were entered.")

        # --- METHOD ---
        self.trail_logger.heading("METHOD")
        self.trail_logger.add_step("Validate input and parse into matrix form.")

        # Validate equations
        is_valid, error_msg, parsed_data = InputValidator.validate_equations(equations_text)

        if not is_valid:
            self.trail_logger.add_step(f"Validation failed: {error_msg}")
            # summary of what happened
            self.trail_logger.heading("SUMMARY")
            self.trail_logger.add_step("Input did not pass validation.  See error message above.")
            self.final_output.insert(tk.END, "Validation failed. Please check your input.")
            messagebox.showerror("Validation Error", error_msg)
            return

        self.trail_logger.add_step("Input validation succeeded.")

        # --- STEPS ---
        self.trail_logger.heading("STEPS")
        system_size, coefficients, constants = parsed_data
        self.trail_logger.add_step(f"System size determined to be {system_size}x{system_size}.")

        # show the parsed matrix/vector as a single step
        lines = ["Coefficients and constants extracted:"]
        for row in coefficients:
            lines.append("  [" + ", ".join(f"{val:8.3f}" for val in row) + "]")
        lines.append("Constants:")
        lines.append("  [" + ", ".join(f"{val:8.3f}" for val in constants) + "]")
        self.trail_logger.add_step("\n".join(lines))

        self.trail_logger.add_step("Gaussian elimination steps coming soon...")

        # --- FINAL ---
        self.trail_logger.heading("FINAL")
        self.trail_logger.add_step("System is valid and ready to solve!")

        # --- VERIFICATION ---
        self.trail_logger.heading("VERIFICATION")
        self.trail_logger.add_step("Verification placeholder (not yet implemented).")

        # --- SUMMARY ---
        self.trail_logger.heading("SUMMARY")
        self.trail_logger.add_step("All input checks passed. Ready for further computation.")

        self.final_output.insert(tk.END, "System is valid and ready to solve!")

    # Clear button
    def clear(self):
        self.eq_input.delete("1.0", tk.END)
        # let the logger clear its own widget and reset numbering
        self.trail_logger.clear()
        self.final_output.delete("1.0", tk.END)