import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk, filedialog
from validator import InputValidator
from solver import GaussianSolver
from datetime import datetime


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
        input_frame.columnconfigure(0, weight=1)

        tk.Label(input_frame, text="Enter equations (2x2 or 3x3):").grid(row=0, column=0, sticky="w", pady=(0,2))
        tk.Label(input_frame, text="Example: 2x + y = 5").grid(row=1, column=0, sticky="w", pady=(0,10))

        # Method selection
        method_frame = tk.Frame(input_frame)
        method_frame.grid(row=2, column=0, sticky="w", pady=(0,5))
        tk.Label(method_frame, text="Select Method:").pack(side="left")
        self.method_var = tk.StringVar(value="Gaussian Elimination")
        self.method_combo = ttk.Combobox(method_frame, textvariable=self.method_var, 
                                         values=["Gaussian Elimination", "Jacobi Iteration"], 
                                         state="readonly", width=20)
        self.method_combo.pack(side="left", padx=(5,0))

        self.eq_input = scrolledtext.ScrolledText(input_frame, height=6)
        self.eq_input.grid(row=3, column=0, sticky="ew", pady=(0,10))

        btn_frame = tk.Frame(input_frame)
        btn_frame.grid(row=4, column=0, sticky="w")
        tk.Button(btn_frame, text="Compute", command=self.compute).pack(side="left", padx=(0,5))
        tk.Button(btn_frame, text="Clear", command=self.clear).pack(side="left", padx=(0,5))
        tk.Button(btn_frame, text="Export Report", command=self.export_report).pack(side="left")

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
        self.trail_output.insert(tk.END, "\n\n")

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
                self.trail_output.insert(tk.END, f"Step {idx}: {step}\n\n")
                
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
        self.trail_output.insert(tk.END, "\n\n=== STOPPING REASON ===\n")
        self.trail_output.insert(tk.END, f"{stopping_reason}\n\n")

        # FINAL
        self.trail_output.insert(tk.END, "=== FINAL ===\n")
        variables = ["x", "y", "z"]
        for i, val in enumerate(solution):
            self.trail_output.insert(tk.END, f"{variables[i]} = {val:.4f}\n")

        # VERIFICATION
        self.trail_output.insert(tk.END, "\n\n=== VERIFICATION ===\n")
        
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
        self.trail_output.insert(tk.END, "\n\n=== SUMMARY ===\n")
        if method == "Gaussian Elimination":
            self.trail_output.insert(tk.END, "Solved system using Gaussian elimination.\n")
        else:
            self.trail_output.insert(tk.END, "Solved system using Jacobi iteration.\n")
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

    def export_report(self):
        """Export the solution trail as a report (TXT or HTML)"""
        trail_content = self.trail_output.get("1.0", tk.END).strip()
        
        if not trail_content:
            messagebox.showwarning("Export Report", "No solution to export. Please compute a solution first.")
            return
        
        # Ask user for file format
        format_choice = messagebox.askyesnocancel(
            "Export Format",
            "Choose export format:\nYes = HTML (formatted)\nNo = TXT (plain text)\nCancel = Cancel export"
        )
        
        if format_choice is None:  # Cancel was clicked
            return
        
        file_extension = ".html" if format_choice else ".txt"
        file_types = [("HTML files", "*.html"), ("All files", "*.*")] if format_choice else [("Text files", "*.txt"), ("All files", "*.*")]
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=file_extension,
            filetypes=file_types,
            initialfile=f"solution_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}"
        )
        
        if not file_path:
            return
        
        try:
            if format_choice:  # HTML
                self._save_html_report(file_path, trail_content)
            else:  # TXT
                self._save_txt_report(file_path, trail_content)
            
            messagebox.showinfo("Export Successful", f"Report exported successfully to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export report:\n{str(e)}")
    
    def _save_txt_report(self, file_path: str, content: str):
        """Save report as plain text file"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("LINEAR SYSTEM SOLVER - SOLUTION REPORT\n")
            f.write("=" * 70 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 70 + "\n\n")
            f.write(content)
            f.write("\n\n" + "=" * 70 + "\n")
            f.write("END OF REPORT\n")
            f.write("=" * 70 + "\n")
    
    def _save_html_report(self, file_path: str, content: str):
        """Save report as HTML file with formatting"""
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Linear System Solver - Solution Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: white;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        
        .header {{
            border-bottom: 3px solid #2c3e50;
            padding-bottom: 15px;
            margin-bottom: 20px;
        }}
        
        .header h1 {{
            color: #2c3e50;
            margin-bottom: 5px;
        }}
        
        .timestamp {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        
        .content {{
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: 'Courier New', monospace;
            background-color: #f8f9fa;
            padding: 15px;
            border-left: 4px solid #3498db;
            border-radius: 4px;
            overflow-x: auto;
        }}
        
        .section {{
            margin-bottom: 20px;
        }}
        
        .section-title {{
            color: #2c3e50;
            font-weight: bold;
            margin: 15px 0 10px 0;
        }}
        
        .footer {{
            border-top: 2px solid #ecf0f1;
            margin-top: 30px;
            padding-top: 15px;
            text-align: center;
            color: #95a5a6;
            font-size: 0.85em;
        }}
        
        @media print {{
            body {{
                background-color: white;
            }}
            .container {{
                box-shadow: none;
                max-width: 100%;
                margin: 0;
                padding: 0;
            }}
            .content {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Linear System Solver - Solution Report</h1>
            <div class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
        
        <div class="content">
{self._escape_html(content)}
        </div>
        
        <div class="footer">
            <p>Linear System Solver v1.0 | Solution Report</p>
            <p>For questions or issues, please contact the development team.</p>
        </div>
    </div>
</body>
</html>"""
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    @staticmethod
    def _escape_html(text: str) -> str:
        """Escape HTML special characters"""
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))


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