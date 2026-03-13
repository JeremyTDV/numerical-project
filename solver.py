import numpy as np

class GaussianSolver:

    @staticmethod
    def solve(coefficients, constants):

        A = np.array(coefficients, dtype=float)
        b = np.array(constants, dtype=float)

        n = len(b)
        steps = []

        aug = np.hstack((A, b.reshape(-1,1)))

        steps.append("Initial Augmented Matrix:\n" + str(aug))

        # Forward Elimination
        for i in range(n):

            pivot = aug[i][i]

            aug[i] = aug[i] / pivot
            steps.append(f"\nDivide Row {i+1} by pivot ({pivot})\n" + str(aug))

            for j in range(i+1, n):

                factor = aug[j][i]

                aug[j] = aug[j] - factor * aug[i]
                steps.append(f"\nRow {j+1} = Row {j+1} - ({factor}) * Row {i+1}\n" + str(aug))

        # Back Substitution
        x = np.zeros(n)

        for i in range(n-1, -1, -1):
            x[i] = aug[i][-1] - np.sum(aug[i,i+1:n] * x[i+1:n])

        steps.append("\nBack Substitution Result:")
        for i,val in enumerate(x):
            steps.append(f"x{i+1} = {val}")

        return x, steps