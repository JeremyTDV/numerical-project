import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from validator import InputValidator
from solver import GaussianSolver


class GaussianSolverGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("Linear System Solver")
        self.root.geometry("900x700")

        # INPUT AREA
        input_frame = tk.LabelFrame(root, text="Inputs", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Enter equations (2x2 or 3x3):").pack()
        tk.Label(input_frame, text="Example: 2x + y = 5").pack()

        # Method selection
        method_frame = tk.Frame(input_frame)
        method_frame.pack(pady=5)
        tk.Label(method_frame, text="Select Method:").pack(side="left")
        self.method_var = tk.StringVar(value="Gaussian Elimination")
        self.method_combo = ttk.Combobox(method_frame, textvariable=self.method_var, 
                                         values=["Gaussian Elimination", "Jacobi Iteration"], 
                                         state="readonly", width=20)
        self.method_combo.pack(side="left")

        self.eq_input = scrolledtext.ScrolledText(input_frame, height=6)
        self.eq_input.pack(fill="x")

        btn_frame = tk.Frame(input_frame)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Compute", command=self.compute).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Clear", command=self.clear).pack(side="left", padx=5)

        # SOLUTION TRAIL
        trail_frame = tk.LabelFrame(root, text="Solution Trail")
        trail_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.trail_output = scrolledtext.ScrolledText(trail_frame)
        self.trail_output.pack(fill="both", expand=True)

        # FINAL ANSWER
        answer_frame = tk.LabelFrame(root, text="Final Answer")
        answer_frame.pack(fill="x", padx=10, pady=5)

        self.final_output = tk.Text(answer_frame, height=4)
        self.final_output.pack(fill="x")

    def compute(self):

        equations_text = self.eq_input.get("1.0", tk.END).strip()

        self.trail_output.delete("1.0", tk.END)
        self.final_output.delete("1.0", tk.END)

        # Validate input
        valid, error, parsed = InputValidator.validate_equations(equations_text)

        if not valid:
            messagebox.showerror("Validation Error", error)
            return

        system_size, coefficients, constants = parsed

        method = self.method_var.get()

        # GIVEN
        self.trail_output.insert(tk.END, "=== GIVEN ===\n")
        self.trail_output.insert(tk.END, "Equations:\n")
        for line in equations_text.splitlines():
            if line.strip():
                self.trail_output.insert(tk.END, line.strip() + "\n")
        self.trail_output.insert(tk.END, "\n")

        # METHOD
        self.trail_output.insert(tk.END, "=== METHOD ===\n")
        if method == "Gaussian Elimination":
            self.trail_output.insert(tk.END, "Gaussian elimination (forward elimination + back substitution)\n\n")
        else:
            self.trail_output.insert(tk.END, "Jacobi iteration\n\n")

        # STEPS
        self.trail_output.insert(tk.END, "=== STEPS ===\n")

        # Solve
        if method == "Gaussian Elimination":
            solution, steps, stopping_reason = GaussianSolver.solve(coefficients, constants)
        else:
            solution, steps, stopping_reason = GaussianSolver.jacobi_solve(coefficients, constants)

        for idx, step in enumerate(steps, start=1):
            self.trail_output.insert(tk.END, f"Step {idx}: {step}\n")
        
        # STOPPING REASON
        self.trail_output.insert(tk.END, f"\n=== STOPPING REASON ===\n{stopping_reason}\n")

        # FINAL
        self.trail_output.insert(tk.END, "\n=== FINAL ===\n")
        variables = ["x", "y", "z"]
        for i, val in enumerate(solution):
            self.trail_output.insert(tk.END, f"{variables[i]} = {val:.4f}\n")

        # VERIFICATION
        self.trail_output.insert(tk.END, "\n=== VERIFICATION ===\n")
        try:
            import numpy as np

            A = np.array(coefficients, dtype=float)
            x = np.array(solution, dtype=float)
            b = np.array(constants, dtype=float)
            verified = np.allclose(A.dot(x), b, atol=1e-6, rtol=1e-6)

            for i in range(len(b)):
                lhs = float(np.dot(A[i], x))
                self.trail_output.insert(tk.END, f"Eq {i+1}: LHS={lhs:.6f}  RHS={b[i]:.6f}\n")

            self.trail_output.insert(tk.END, f"Verification: {'PASS' if verified else 'FAIL'}\n")
        except Exception:
            self.trail_output.insert(tk.END, "Verification: Unable to compute verification (numpy error).\n")

        # SUMMARY
        self.trail_output.insert(tk.END, "\n=== SUMMARY ===\n")
        self.trail_output.insert(tk.END, "Solved system using Gaussian elimination.\n")
        self.trail_output.insert(tk.END, "Solution is unique if the coefficient matrix is non-singular.\n")

        # Also show final answer in the dedicated panel
        self.final_output.insert(tk.END, "Solution:\n")
        if "STOPPED" in stopping_reason:
            self.final_output.insert(tk.END, f"⚠ Process did not complete normally.\n")
            self.final_output.insert(tk.END, f"Reason: {stopping_reason.replace('STOPPED: ', '')}\n\n")
            self.final_output.insert(tk.END, f"Variables: {', '.join([variables[i] for i in range(system_size)])}\n")
        else:
            for i, val in enumerate(solution):
                self.final_output.insert(tk.END, f"{variables[i]} = {val:.4f}\n")

    def clear(self):

        self.eq_input.delete("1.0", tk.END)
        self.trail_output.delete("1.0", tk.END)
        self.final_output.delete("1.0", tk.END)