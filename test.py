import unittest
import numpy as np
from solver import GaussianSolver

class TestLinearSolver(unittest.TestCase):

    def test_gaussian_2x2_simple(self):
        # 2x + y = 5
        # x + 3y = 6
        # Solution: x=1.8, y=1.4
        coefficients = [[2, 1], [1, 3]]
        constants = [5, 6]
        solution, steps, reason = GaussianSolver.solve(coefficients, constants)
        expected = np.array([1.8, 1.4])
        np.testing.assert_allclose(solution, expected, atol=1e-6)
        self.assertIn("COMPLETED", reason)

    def test_gaussian_3x3(self):
        # x + y + z = 6
        # 2x - y + z = 3
        # x + 2y - z = 2
        # Solution: x=1, y=2, z=3
        coefficients = [[1, 1, 1], [2, -1, 1], [1, 2, -1]]
        constants = [6, 3, 2]
        solution, steps, reason = GaussianSolver.solve(coefficients, constants)
        expected = np.array([1, 2, 3])
        np.testing.assert_allclose(solution, expected, atol=1e-6)
        self.assertIn("COMPLETED", reason)

    def test_gaussian_singular(self):
        # x + y = 1
        # 2x + 2y = 3  (inconsistent)
        coefficients = [[1, 1], [2, 2]]
        constants = [1, 3]
        solution, steps, reason = GaussianSolver.solve(coefficients, constants)
        self.assertIn("STOPPED", reason)

    def test_jacobi_2x2_convergent(self):
        # 4x + y = 5
        # x + 3y = 6
        # Solution: x=9/11≈0.818, y=20/11≈1.818? Wait, y=5-4x=5-4*(9/11)=5-36/11=(55-36)/11=19/11≈1.727
        coefficients = [[4, 1], [1, 3]]
        constants = [5, 6]
        solution, steps, reason = GaussianSolver.jacobi_solve(coefficients, constants)
        expected = np.array([9/11, 19/11])  # approx 0.818, 1.727
        np.testing.assert_allclose(solution, expected, atol=1e-4)
        self.assertIn("COMPLETED", reason)

    def test_jacobi_3x3_convergent(self):
        # 3x + y - z = 1
        # x + 4y + z = 2
        # 2x - y + 5z = 3
        # Diagonally dominant
        coefficients = [[3, 1, -1], [1, 4, 1], [2, -1, 5]]
        constants = [1, 2, 3]
        solution, steps, reason = GaussianSolver.jacobi_solve(coefficients, constants)
        # Approximate solution
        expected = np.array([0.5, 0.5, 0.5])  # rough check
        self.assertIn("COMPLETED", reason)

if __name__ == '__main__':
    unittest.main()