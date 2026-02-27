import tkinter as tk
from tkinter import messagebox, scrolledtext
from validator import InputValidator


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

        # Final Answer
        answer_frame = tk.LabelFrame(root, text="Final Answer")
        answer_frame.pack(fill="x", padx=10, pady=5)

        self.final_output = tk.Text(answer_frame, height=4)
        self.final_output.pack(fill="x")

    # Placeholder for solution trail
    def compute_placeholder(self):
        equations_text = self.eq_input.get("1.0", tk.END).strip()
        
        self.trail_output.delete("1.0", tk.END)
        self.final_output.delete("1.0", tk.END)
        
        # Validate equations
        is_valid, error_msg, parsed_data = InputValidator.validate_equations(equations_text)
        
        # Log validation status
        self.trail_output.insert(tk.END, "=== INPUT VALIDATION ===\n")
        
        if not is_valid:
            self.trail_output.insert(tk.END, f"Status: FAIL\n\n")
            self.trail_output.insert(tk.END, f"Validation Errors:\n")
            self.trail_output.insert(tk.END, f"  ✗ {error_msg}\n")
            self.trail_output.insert(tk.END, f"\nValidation Checks:\n")
            
            # Determine which checks failed
            if "No equations provided" in error_msg:
                self.trail_output.insert(tk.END, f"  ✗ Required fields present\n")
                self.trail_output.insert(tk.END, f"  ○ Correct system size (2x2 or 3x3)\n")
                self.trail_output.insert(tk.END, f"  ○ Equation format valid\n")
                self.trail_output.insert(tk.END, f"  ○ All coefficients are numeric\n")
                self.trail_output.insert(tk.END, f"  ○ All constants are numeric\n")
                self.trail_output.insert(tk.END, f"  ○ Coefficient ranges acceptable\n")
                self.trail_output.insert(tk.END, f"  ○ No zero rows detected\n")
                self.trail_output.insert(tk.END, f"  ○ No linearly dependent equations\n")
            elif "Only 2x2 and 3x3 systems are supported" in error_msg:
                self.trail_output.insert(tk.END, f"  ✓ Required fields present\n")
                self.trail_output.insert(tk.END, f"  ✗ Correct system size (2x2 or 3x3)\n")
                self.trail_output.insert(tk.END, f"  ○ Equation format valid\n")
                self.trail_output.insert(tk.END, f"  ○ All coefficients are numeric\n")
                self.trail_output.insert(tk.END, f"  ○ All constants are numeric\n")
                self.trail_output.insert(tk.END, f"  ○ Coefficient ranges acceptable\n")
                self.trail_output.insert(tk.END, f"  ○ No zero rows detected\n")
                self.trail_output.insert(tk.END, f"  ○ No linearly dependent equations\n")
            elif "Equation" in error_msg and ("Missing '='" in error_msg or "Right side must be" in error_msg or "No variables found" in error_msg or "Invalid term" in error_msg or "appears multiple times" in error_msg):
                self.trail_output.insert(tk.END, f"  ✓ Required fields present\n")
                self.trail_output.insert(tk.END, f"  ✓ Correct system size (2x2 or 3x3)\n")
                self.trail_output.insert(tk.END, f"  ✗ Equation format valid\n")
                self.trail_output.insert(tk.END, f"  ○ All coefficients are numeric\n")
                self.trail_output.insert(tk.END, f"  ○ All constants are numeric\n")
                self.trail_output.insert(tk.END, f"  ○ Coefficient ranges acceptable\n")
                self.trail_output.insert(tk.END, f"  ○ No zero rows detected\n")
                self.trail_output.insert(tk.END, f"  ○ No linearly dependent equations\n")
            elif "out of acceptable range" in error_msg:
                self.trail_output.insert(tk.END, f"  ✓ Required fields present\n")
                self.trail_output.insert(tk.END, f"  ✓ Correct system size (2x2 or 3x3)\n")
                self.trail_output.insert(tk.END, f"  ✓ Equation format valid\n")
                self.trail_output.insert(tk.END, f"  ✓ All coefficients are numeric\n")
                self.trail_output.insert(tk.END, f"  ✓ All constants are numeric\n")
                self.trail_output.insert(tk.END, f"  ✗ Coefficient ranges acceptable\n")
                self.trail_output.insert(tk.END, f"  ○ No zero rows detected\n")
                self.trail_output.insert(tk.END, f"  ○ No linearly dependent equations\n")
            elif "Expected" in error_msg and "variable(s)" in error_msg:
                self.trail_output.insert(tk.END, f"  ✓ Required fields present\n")
                self.trail_output.insert(tk.END, f"  ✓ Correct system size (2x2 or 3x3)\n")
                self.trail_output.insert(tk.END, f"  ✓ Equation format valid\n")
                self.trail_output.insert(tk.END, f"  ✓ All coefficients are numeric\n")
                self.trail_output.insert(tk.END, f"  ✓ All constants are numeric\n")
                self.trail_output.insert(tk.END, f"  ✓ Coefficient ranges acceptable\n")
                self.trail_output.insert(tk.END, f"  ✗ No zero rows detected\n")
                self.trail_output.insert(tk.END, f"  ○ No linearly dependent equations\n")
            elif "zero rows" in error_msg or "singular" in error_msg or "linearly dependent" in error_msg:
                self.trail_output.insert(tk.END, f"  ✓ Required fields present\n")
                self.trail_output.insert(tk.END, f"  ✓ Correct system size (2x2 or 3x3)\n")
                self.trail_output.insert(tk.END, f"  ✓ Equation format valid\n")
                self.trail_output.insert(tk.END, f"  ✓ All coefficients are numeric\n")
                self.trail_output.insert(tk.END, f"  ✓ All constants are numeric\n")
                self.trail_output.insert(tk.END, f"  ✓ Coefficient ranges acceptable\n")
                if "zero rows" in error_msg:
                    self.trail_output.insert(tk.END, f"  ✗ No zero rows detected\n")
                    self.trail_output.insert(tk.END, f"  ○ No linearly dependent equations\n")
                else:
                    self.trail_output.insert(tk.END, f"  ✓ No zero rows detected\n")
                    self.trail_output.insert(tk.END, f"  ✗ No linearly dependent equations\n")
            
            self.final_output.insert(tk.END, "Validation failed. Please check your input.")
            messagebox.showerror("Validation Error", error_msg)
            return
        
        self.trail_output.insert(tk.END, f"Status: PASS\n")
        
        system_size, coefficients, constants = parsed_data
        
        # Display validation details
        self.trail_output.insert(tk.END, f"System Size: {system_size}x{system_size}\n")
        self.trail_output.insert(tk.END, f"Equations: {system_size}\n")
        self.trail_output.insert(tk.END, f"Variables: {system_size}\n")
        self.trail_output.insert(tk.END, f"\nValidation Checks Passed:\n")
        self.trail_output.insert(tk.END, f"  ✓ Required fields present\n")
        self.trail_output.insert(tk.END, f"  ✓ Correct system size (2x2 or 3x3)\n")
        self.trail_output.insert(tk.END, f"  ✓ Equation format valid\n")
        self.trail_output.insert(tk.END, f"  ✓ All coefficients are numeric\n")
        self.trail_output.insert(tk.END, f"  ✓ All constants are numeric\n")
        self.trail_output.insert(tk.END, f"  ✓ Coefficient ranges acceptable\n")
        self.trail_output.insert(tk.END, f"  ✓ No zero rows detected\n")
        self.trail_output.insert(tk.END, f"  ✓ No linearly dependent equations\n")
        
        # Display the parsed system
        self.trail_output.insert(tk.END, f"\n=== PARSED SYSTEM ===\n")
        self.trail_output.insert(tk.END, "\nCoefficient Matrix:\n")
        
        for i, row in enumerate(coefficients):
            row_str = "  [" + ", ".join(f"{val:8.3f}" for val in row) + "]"
            self.trail_output.insert(tk.END, row_str + "\n")
        
        self.trail_output.insert(tk.END, "\nConstants Vector:\n")
        const_str = "  [" + ", ".join(f"{val:8.3f}" for val in constants) + "]"
        self.trail_output.insert(tk.END, const_str + "\n")
        
        self.trail_output.insert(tk.END, "\n=== SOLUTION TRAIL ===\n")
        self.trail_output.insert(tk.END, "Gaussian elimination steps coming soon...\n")

        self.final_output.insert(tk.END, "System is valid and ready to solve!")

    # Clear button
    def clear(self):
        self.eq_input.delete("1.0", tk.END)
        self.trail_output.delete("1.0", tk.END)
        self.final_output.delete("1.0", tk.END)