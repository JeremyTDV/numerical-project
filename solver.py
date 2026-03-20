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
        steps.append(f"\nStopping Rules: Tolerance={tolerance}, Max Iterations={max_iterations}")

        # Forward Elimination with stopping rules
        for i in range(n):
            iteration_count += 1
            
            if iteration_count > max_iterations:
                stopping_reason = f"STOPPED: Maximum iterations ({max_iterations}) reached during forward elimination at row {i+1}."
                steps.append(f"\n⚠ {stopping_reason}")
                x = np.zeros(n)
                return x, steps, stopping_reason

            pivot = aug[i][i]

            # Check if pivot is too small (tolerance check)
            if abs(pivot) < tolerance:
                stopping_reason = f"STOPPED: Pivot element ({pivot}) at row {i+1} is below tolerance ({tolerance}). Matrix may be singular or ill-conditioned."
                steps.append(f"\n⚠ {stopping_reason}")
                x = np.zeros(n)
                return x, steps, stopping_reason

            aug[i] = aug[i] / pivot
            steps.append(f"\nDivide Row {i+1} by pivot ({pivot})\n" + str(aug))

            for j in range(i+1, n):
                iteration_count += 1
                
                if iteration_count > max_iterations:
                    stopping_reason = f"STOPPED: Maximum iterations ({max_iterations}) reached during elimination at row {j+1}."
                    steps.append(f"\n⚠ {stopping_reason}")
                    x = np.zeros(n)
                    return x, steps, stopping_reason

                factor = aug[j][i]

                # Skip if factor is already near zero
                if abs(factor) < tolerance:
                    steps.append(f"\nRow {j+1} already has zero in column {i+1} (factor={factor}), skipping elimination.")
                    continue

                aug[j] = aug[j] - factor * aug[i]
                steps.append(f"\nRow {j+1} = Row {j+1} - ({factor}) * Row {i+1}\n" + str(aug))

        # Check if row echelon form is reached
        steps.append(f"\n✓ Forward elimination complete: Row echelon form reached.")

        # Back Substitution
        x = np.zeros(n)

        for i in range(n-1, -1, -1):
            x[i] = aug[i][-1] - np.sum(aug[i,i+1:n] * x[i+1:n])

        steps.append("\nBack Substitution Result:")
        for i,val in enumerate(x):
            steps.append(f"x{i+1} = {val}")

        # Determine final stopping reason
        stopping_reason = "COMPLETED: System solved successfully using Gaussian elimination. Exact row echelon form reached."
        steps.append(f"\n✓ {stopping_reason}")

        return x, steps, stopping_reason