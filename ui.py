import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from validator import InputValidator
from solver import GaussianSolver


class GaussianSolverGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("Linear System Solver")
        self.root.geometry("900x700")
        
        # Create menu bar
        self.create_menu()
        
        # Add keyboard shortcut for About (F1)
        self.root.bind('<F1>', lambda e: self.show_about())

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
            # Log error to trail before showing message box
            self.trail_output.insert(tk.END, "=== VALIDATION ERROR ===\n")
            self.trail_output.insert(tk.END, f"Error: {error}\n")
            self.trail_output.insert(tk.END, "\n=== INPUT RECEIVED ===\n")
            if equations_text.strip():
                for line in equations_text.splitlines():
                    if line.strip():
                        self.trail_output.insert(tk.END, line.strip() + "\n")
            else:
                self.trail_output.insert(tk.END, "[No input provided]\n")
            
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

        # Solve with error handling
        try:
            if method == "Gaussian Elimination":
                solution, steps, stopping_reason = GaussianSolver.solve(coefficients, constants)
            else:
                solution, steps, stopping_reason = GaussianSolver.jacobi_solve(coefficients, constants)

            for idx, step in enumerate(steps, start=1):
                self.trail_output.insert(tk.END, f"Step {idx}: {step}\n")
                
        except Exception as e:
            self.trail_output.insert(tk.END, f"ERROR: Failed to solve system.\n")
            self.trail_output.insert(tk.END, f"Error details: {str(e)}\n")
            self.trail_output.insert(tk.END, f"This may indicate a singular matrix or numerical instability.\n")
            
            # Set default values for failed computation
            solution = [0.0] * system_size
            stopping_reason = f"STOPPED: Computational error - {str(e)}"
            
            # Show error in final answer panel
            self.final_output.insert(tk.END, "ERROR: Computation failed!\n")
            self.final_output.insert(tk.END, f"Reason: {str(e)}\n")
            return
        
        # STOPPING REASON
        self.trail_output.insert(tk.END, f"\n=== STOPPING REASON ===\n{stopping_reason}\n")

        # FINAL
        self.trail_output.insert(tk.END, "\n=== FINAL ===\n")
        variables = ["x", "y", "z"]
        for i, val in enumerate(solution):
            self.trail_output.insert(tk.END, f"{variables[i]} = {val:.4f}\n")

        # VERIFICATION
        self.trail_output.insert(tk.END, "\n=== VERIFICATION ===\n")
        
        verification_result = GaussianSolver.verify_solution(coefficients, constants, solution)
        
        # Verification summary
        self.trail_output.insert(tk.END, f"{verification_result['summary']}\n")
        self.trail_output.insert(tk.END, f"Tolerance: {1e-6:.0e}\n\n")
        
        # Detailed equation verification
        self.trail_output.insert(tk.END, "Equation-by-Equation Analysis:\n")
        self.trail_output.insert(tk.END, "-" * 70 + "\n")
        
        for eq_info in verification_result['equation_results']:
            eq_num = eq_info['equation_idx']
            lhs = eq_info['lhs']
            rhs = eq_info['rhs']
            residual = eq_info['residual']
            abs_residual = eq_info['abs_residual']
            passed = eq_info['passed']
            
            status = "✓ PASS" if passed else "✗ FAIL"
            self.trail_output.insert(tk.END, f"Eq {eq_num}: {status}\n")
            self.trail_output.insert(tk.END, f"  LHS = {lhs:12.8f}  RHS = {rhs:12.8f}\n")
            self.trail_output.insert(tk.END, f"  Residual = {residual:12.8f}  |Residual| = {abs_residual:.2e}\n")
        
        self.trail_output.insert(tk.END, "-" * 70 + "\n")
        
        # Verification metrics
        self.trail_output.insert(tk.END, "Verification Metrics:\n")
        self.trail_output.insert(tk.END, f"  Maximum Residual: {verification_result['max_residual']:.2e}\n")
        self.trail_output.insert(tk.END, f"  Average Residual: {verification_result['avg_residual']:.2e}\n")
        passed_count = sum(1 for eq in verification_result['equation_results'] if eq['passed'])
        self.trail_output.insert(tk.END, f"  Equations Satisfied: {passed_count}/{len(verification_result['equation_results'])}\n")
        
        # Overall result
        self.trail_output.insert(tk.END, "\nOverall Verification Result:\n")
        if verification_result['is_verified']:
            self.trail_output.insert(tk.END, "✓ Solution VERIFIED - All equations satisfied within tolerance.\n")
        else:
            self.trail_output.insert(tk.END, "✗ Solution NOT VERIFIED - Some equations exceed tolerance.\n")
            self.trail_output.insert(tk.END, f"  {len(verification_result['equation_results']) - passed_count} equation(s) failed verification.\n")

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
            
            # Add verification status to final answer
            self.final_output.insert(tk.END, "\n" + "-" * 40 + "\n")
            if verification_result['is_verified']:
                self.final_output.insert(tk.END, "✓ VERIFIED\n")
            else:
                self.final_output.insert(tk.END, "✗ NOT VERIFIED\n")
            self.final_output.insert(tk.END, f"Max Residual: {verification_result['max_residual']:.2e}\n")

    def clear(self):

        self.eq_input.delete("1.0", tk.END)
        self.trail_output.delete("1.0", tk.END)
        self.final_output.delete("1.0", tk.END)

    def create_menu(self):
        """Create the menu bar with Help menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About (F1)", command=self.show_about)
        help_menu.add_separator()
        help_menu.add_command(label="Exit", command=self.root.quit)

    def show_about(self):
        """Show About dialog with project information"""
        about_text = """Linear System Solver
Version 1.0


Project Members:
 Brosola, Gaines
    Capua, Anthony Lorenzo
    Valenzuela, Jeremy Terrence


A simple calculator that solves systems of linear equations 
using Gaussian Elimination step-by-step.


Features:
• Solves 2x2 and 3x3 systems
• Step-by-step solution display
• Input validation
• Solution verification

"""
        
        messagebox.showinfo("About Linear System Solver", about_text)