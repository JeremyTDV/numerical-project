"""
Input validation module for linear system solving.
Validates equations and parses them into coefficient matrices and constants vectors.
"""

import re
from typing import Tuple, List, Optional


class InputValidator:
    """Validates input for linear system solving."""
    
    # Regex pattern to match linear equations like "2x + 3y = 5" or "x - 2y + z = 10"
    EQUATION_PATTERN = r'^([+-]?\s*\d*\.?\d*\s*[a-zA-Z](?:\s*[+-]\s*\d*\.?\d*\s*[a-zA-Z])*)\s*=\s*([+-]?\d+\.?\d*)$'
    
    # Maximum allowable coefficient/constant magnitude for numerical stability
    MAX_VALUE = 1e10
    MIN_VALUE = -1e10
    
    @staticmethod
    def validate_equations(equations_text: str) -> Tuple[bool, Optional[str], Optional[Tuple]]:
        """
        Validate input equations.
        
        Returns:
            (is_valid, error_message, parsed_data)
            where parsed_data = (system_size, coefficient_matrix, constants_vector)
        """
        # Check if input is empty
        equations = equations_text.strip().splitlines()
        equations = [eq.strip() for eq in equations if eq.strip()]
        
        if not equations:
            return False, "Error: No equations provided. Please enter at least one equation.", None
        
        # Check system size
        num_equations = len(equations)
        if num_equations not in [2, 3]:
            return False, f"Error: Only 2x2 and 3x3 systems are supported. You provided {num_equations} equation(s).", None
        
        try:
            # Parse equations
            parsed = InputValidator._parse_equations(equations, num_equations)
            if not parsed[0]:
                return False, parsed[1], None
            
            system_size, coefficients, constants = parsed[1:]
            
            # Validate coefficients and constants
            valid, msg = InputValidator._validate_values(coefficients, constants)
            if not valid:
                return False, msg, None
            
            # Check for zero rows or singular matrix indicators
            valid, msg = InputValidator._check_solvability(coefficients)
            if not valid:
                return False, msg, None
            
            return True, None, (system_size, coefficients, constants)
            
        except Exception as e:
            return False, f"Error: {str(e)}", None
    
    @staticmethod
    def _parse_equations(equations: List[str], system_size: int) -> Tuple:
        """Parse equations into coefficient matrix and constants vector."""
        coefficients = []
        constants = []
        variable_names = set()
        
        for eq_idx, equation in enumerate(equations):
            # Check equation format
            if '=' not in equation:
                return False, f"Equation {eq_idx + 1}: Missing '=' sign. Format should be 'ax + by = c'."
            
            left, right = equation.split('=', 1)
            left = left.strip()
            right = right.strip()
            
            # Parse right side (constant)
            try:
                constant = float(right)
                if constant < InputValidator.MIN_VALUE or constant > InputValidator.MAX_VALUE:
                    return False, f"Equation {eq_idx + 1}: Constant {constant} is out of acceptable range."
                constants.append(constant)
            except ValueError:
                return False, f"Equation {eq_idx + 1}: Right side must be a number. Got '{right}'."
            
            # Parse left side (coefficients)
            row_coeffs = {}
            terms = InputValidator._split_terms(left)
            
            if not terms:
                return False, f"Equation {eq_idx + 1}: No variables found. Expected {system_size} variable(s)."
            
            for term in terms:
                var, coeff = InputValidator._parse_term(term)
                if var is None:
                    return False, f"Equation {eq_idx + 1}: Invalid term '{term}'."
                
                variable_names.add(var)
                
                if var in row_coeffs:
                    return False, f"Equation {eq_idx + 1}: Variable '{var}' appears multiple times."
                
                if coeff < InputValidator.MIN_VALUE or coeff > InputValidator.MAX_VALUE:
                    return False, f"Equation {eq_idx + 1}: Coefficient {coeff} for '{var}' is out of acceptable range."
                
                row_coeffs[var] = coeff
            
            coefficients.append(row_coeffs)
        
        # Validate variable count
        if len(variable_names) != system_size:
            return False, f"Error: Expected {system_size} variable(s) but found {len(variable_names)}. Variables: {', '.join(sorted(variable_names))}"
        
        # Sort variables and create coefficient matrix
        sorted_vars = sorted(list(variable_names))
        coefficient_matrix = []
        
        for row_coeffs in coefficients:
            row = []
            for var in sorted_vars:
                row.append(row_coeffs.get(var, 0.0))
            coefficient_matrix.append(row)
        
        return True, system_size, coefficient_matrix, constants
    
    @staticmethod
    def _split_terms(expression: str) -> List[str]:
        """Split equation left side into terms."""
        # Handle leading sign
        if expression.startswith('-'):
            expression = expression[1:]
            first_term_negative = True
        else:
            first_term_negative = False
        
        # Replace + and - with delimiters
        expression = expression.replace('+', '|+').replace('-', '|-')
        terms = [t for t in expression.split('|') if t.strip()]
        
        if first_term_negative and terms:
            terms[0] = '-' + terms[0]
        
        return terms
    
    @staticmethod
    def _parse_term(term: str) -> Tuple[Optional[str], Optional[float]]:
        """Parse a single term like '2x' or '-3y' into variable and coefficient."""
        term = term.strip()
        
        # Find variable (letter)
        var_match = re.search(r'[a-zA-Z]', term)
        if not var_match:
            return None, None
        
        var_pos = var_match.start()
        var = term[var_pos]
        
        # Extract coefficient
        coeff_str = term[:var_pos].strip()
        
        # Handle parentheses around coefficient
        if coeff_str.startswith('(') and coeff_str.endswith(')'):
            coeff_str = coeff_str[1:-1].strip()
        
        # Remove spaces from coefficient string
        coeff_str = ''.join(coeff_str.split())
        
        try:
            if coeff_str == '' or coeff_str == '+':
                coeff = 1.0
            elif coeff_str == '-':
                coeff = -1.0
            else:
                coeff = float(coeff_str)
            return var, coeff
        except ValueError:
            return None, None
    
    @staticmethod
    def _validate_values(coefficients: List[List[float]], constants: List[float]) -> Tuple[bool, Optional[str]]:
        """Validate coefficient and constant ranges."""
        # Check for zero coefficients
        all_zero = True
        for row in coefficients:
            for coeff in row:
                if coeff != 0:
                    all_zero = False
                    break
        
        if all_zero:
            return False, "Error: All coefficients are zero. System is singular."
        
        return True, None
    
    @staticmethod
    def _check_solvability(coefficients: List[List[float]]) -> Tuple[bool, Optional[str]]:
        """Check for obvious singular matrix indicators."""
        # Check for all-zero rows
        for row_idx, row in enumerate(coefficients):
            if all(coeff == 0 for coeff in row):
                return False, f"Error: Equation {row_idx + 1} has all zero coefficients. System may be singular or inconsistent."
        
        # Check for duplicate rows (linearly dependent)
        for i in range(len(coefficients)):
            for j in range(i + 1, len(coefficients)):
                if InputValidator._rows_proportional(coefficients[i], coefficients[j]):
                    return False, f"Error: Equations {i + 1} and {j + 1} are linearly dependent. System may not have a unique solution."
        
        return True, None
    
    @staticmethod
    def _rows_proportional(row1: List[float], row2: List[float]) -> bool:
        """Check if two rows are proportional (linearly dependent)."""
        # Find first non-zero element to determine ratio
        ratio = None
        for v1, v2 in zip(row1, row2):
            if v1 != 0 or v2 != 0:
                if v1 == 0 or v2 == 0:
                    return False  # One is zero, other isn't
                current_ratio = v2 / v1
                if ratio is None:
                    ratio = current_ratio
                elif abs(ratio - current_ratio) > 1e-10:  # Allow small floating point error
                    return False
        return True