import numpy as np

class GaussianSolver:

    @staticmethod
    def solve(coefficients, constants, tolerance=1e-10, max_iterations=None):
        """
        Solve a linear system using Gaussian elimination with stopping rules.
        
        Args:
            coefficients: Coefficient matrix
            constants: Constants vector
            tolerance: Tolerance for pivot (if below this, matrix may be singular)
            max_iterations: Maximum iterations allowed (default: n*(n+1)/2)
        
        Returns:
            (solution_vector, steps_list, stopping_reason)
        """

        A = np.array(coefficients, dtype=float)
        b = np.array(constants, dtype=float)

        n = len(b)
        steps = []
        stopping_reason = ""

        # Set default max iterations
        if max_iterations is None:
            max_iterations = n * (n + 1) // 2
        
        iteration_count = 0

        aug = np.hstack((A, b.reshape(-1,1)))

        steps.append("Initial Augmented Matrix:\n" + str(aug))
        steps.append(f"Stopping Rules: Tolerance={tolerance}, Max Iterations={max_iterations}")

        # Forward Elimination with stopping rules
        for i in range(n):
            iteration_count += 1
            
            if iteration_count > max_iterations:
                stopping_reason = f"STOPPED: Maximum iterations ({max_iterations}) reached during forward elimination at row {i+1}."
                steps.append(f"⚠ {stopping_reason}")
                x = np.zeros(n)
                return x, steps, stopping_reason

            # Partial pivoting: swap with the row that has the largest absolute pivot
            max_row = i + np.argmax(np.abs(aug[i:, i]))
            if max_row != i:
                aug[[i, max_row]] = aug[[max_row, i]]
                steps.append(f"Swap Row {i+1} with Row {max_row+1} (partial pivoting):\n" + str(aug))

            pivot = aug[i][i]

            # Check if pivot is too small (tolerance check)
            if abs(pivot) < tolerance:
                stopping_reason = f"STOPPED: Pivot element ({pivot}) at row {i+1} is below tolerance ({tolerance}). Matrix may be singular or ill-conditioned."
                steps.append(f"⚠ {stopping_reason}")
                x = np.zeros(n)
                return x, steps, stopping_reason

            aug[i] = aug[i] / pivot
            steps.append(f"Divide Row {i+1} by pivot ({pivot}):\n" + str(aug))

            for j in range(i+1, n):
                iteration_count += 1
                
                if iteration_count > max_iterations:
                    stopping_reason = f"STOPPED: Maximum iterations ({max_iterations}) reached during elimination at row {j+1}."
                    steps.append(f"⚠ {stopping_reason}")
                    x = np.zeros(n)
                    return x, steps, stopping_reason

                factor = aug[j][i]

                # Skip if factor is already near zero
                if abs(factor) < tolerance:
                    steps.append(f"Row {j+1} already has zero in column {i+1} (factor={factor}), skipping elimination.")
                    continue

                aug[j] = aug[j] - factor * aug[i]
                steps.append(f"Eliminate Row {j+1} using Row {i+1} (factor = {factor}):\n" + str(aug))

        # Check if row echelon form is reached
        steps.append(f"✓ Forward elimination complete: Row echelon form reached.")

        # Back Substitution
        x = np.zeros(n)

        for i in range(n-1, -1, -1):
            x[i] = aug[i][-1] - np.sum(aug[i,i+1:n] * x[i+1:n])

        steps.append("Back Substitution Result:")
        for i,val in enumerate(x):
            steps.append(f"x{i+1} = {val}")

        # Determine final stopping reason
        stopping_reason = "COMPLETED: System solved successfully using Gaussian elimination. Exact row echelon form reached."
        steps.append(f"✓ {stopping_reason}")

        return x, steps, stopping_reason

    @staticmethod
    def jacobi_solve(coefficients, constants, tolerance=1e-10, max_iterations=100):
        """
        Solve a linear system using Jacobi iteration with stopping rules.
        
        Args:
            coefficients: Coefficient matrix
            constants: Constants vector
            tolerance: Tolerance for convergence (max difference between iterations)
            max_iterations: Maximum iterations allowed
        
        Returns:
            (solution_vector, steps_list, stopping_reason)
        """
        A = np.array(coefficients, dtype=float)
        b = np.array(constants, dtype=float)
        n = len(b)
        x = np.zeros(n)
        steps = []
        stopping_reason = ""

        steps.append("Initial guess: x = " + str(x))
        steps.append(f"Stopping Rules: Tolerance={tolerance}, Max Iterations={max_iterations}")

        # Check for zero diagonal elements before iterating (would cause division by zero)
        for i in range(n):
            if abs(A[i, i]) < 1e-14:
                stopping_reason = f"STOPPED: Zero diagonal element at row {i+1}. Jacobi iteration requires non-zero diagonal. Rearrange equations so each diagonal is non-zero."
                steps.append(f"⚠ {stopping_reason}")
                return x, steps, stopping_reason

        for iteration in range(max_iterations):
            x_new = np.zeros(n)
            for i in range(n):
                sum_ax = 0.0
                for j in range(n):
                    if j != i:
                        sum_ax += A[i, j] * x[j]
                x_new[i] = (b[i] - sum_ax) / A[i, i]

            # Check convergence
            diff = np.abs(x_new - x)
            max_diff = np.max(diff)
            steps.append(f"Iteration {iteration + 1}: x = {x_new}, max diff = {max_diff}")

            if max_diff < tolerance:
                stopping_reason = f"COMPLETED: Converged after {iteration + 1} iterations."
                steps.append(f"✓ {stopping_reason}")
                return x_new, steps, stopping_reason

            x = x_new.copy()

        stopping_reason = f"STOPPED: Maximum iterations ({max_iterations}) reached without convergence."
        steps.append(f"⚠ {stopping_reason}")
        return x, steps, stopping_reason

    @staticmethod
    def verify_solution(coefficients, constants, solution, tolerance=1e-6):
        """
        Verify a solution to a linear system with detailed auditing.
        
        Args:
            coefficients: Coefficient matrix
            constants: Constants vector
            solution: Solution vector to verify
            tolerance: Tolerance for considering equation as satisfied
        
        Returns:
            Dictionary with detailed verification information:
            {
                'is_verified': bool,
                'residuals': list of residuals,
                'max_residual': max absolute residual,
                'avg_residual': average absolute residual,
                'equation_results': list of {equation_idx, lhs, rhs, residual, passed},
                'all_passed': bool,
                'summary': str
            }
        """
        try:
            A = np.array(coefficients, dtype=float)
            x = np.array(solution, dtype=float)
            b = np.array(constants, dtype=float)
            
            # Check for dimension mismatch before computing
            if A.shape[1] != x.shape[0]:
                raise ValueError(
                    f"Solution vector length ({x.shape[0]}) does not match "
                    f"number of variables ({A.shape[1]})."
                )
            
            # Calculate residuals: r = Ax - b
            ax = A.dot(x)
            residuals = ax - b
            abs_residuals = np.abs(residuals)
            
            max_residual = np.max(abs_residuals)
            avg_residual = np.mean(abs_residuals)
            
            # Check each equation
            equation_results = []
            all_passed = True
            
            for i in range(len(b)):
                lhs = float(ax[i])
                rhs = float(b[i])
                residual = float(residuals[i])
                passed = abs(residual) < tolerance
                
                if not passed:
                    all_passed = False
                
                equation_results.append({
                    'equation_idx': i + 1,
                    'lhs': lhs,
                    'rhs': rhs,
                    'residual': residual,
                    'abs_residual': abs(residual),
                    'passed': passed
                })
            
            # Determine overall verification status
            is_verified = np.allclose(ax, b, atol=tolerance, rtol=1e-10)
            
            summary = f"{'✓ VERIFIED' if is_verified else '✗ NOT VERIFIED'}: {sum(1 for eq in equation_results if eq['passed'])}/{len(b)} equations satisfied"
            
            return {
                'is_verified': is_verified,
                'all_passed': all_passed,
                'residuals': residuals.tolist(),
                'max_residual': float(max_residual),
                'avg_residual': float(avg_residual),
                'equation_results': equation_results,
                'summary': summary
            }
            
        except Exception as e:
            return {
                'is_verified': False,
                'all_passed': False,
                'residuals': [],
                'max_residual': None,
                'avg_residual': None,
                'equation_results': [],
                'summary': f'✗ VERIFICATION ERROR: {str(e)}'
            }