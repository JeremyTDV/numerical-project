# Linear System Solver v1.0

A comprehensive GUI application for solving systems of linear equations using numerical methods.

## Project Members
- Brosola, Gaines
- Capua, Anthony Lorenzo
- Valenzuela, Jeremy Terrence

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Limitations](#limitations)

---

## Overview

Linear System Solver is a desktop application designed to solve systems of linear equations step-by-step using either **Gaussian Elimination** or **Jacobi Iteration** methods. The application provides detailed step-by-step solutions with verification and the ability to export reports in HTML or plain text format.

**Current Version:** v1.0

---

## Features

### Core Functionality
- ✓ Solves 2×2 and 3×3 linear systems
- ✓ Two solving methods: Gaussian Elimination and Jacobi Iteration
- ✓ Step-by-step solution display
- ✓ Complete solution verification with residual analysis
- ✓ Comprehensive input validation
- ✓ Solution trail tracking with detailed output

### User Interface
- ✓ Clean, intuitive GUI using Tkinter
- ✓ Real-time equation input with scrollable text area
- ✓ Method selection dropdown
- ✓ Formatted solution trail with sections
- ✓ Dedicated final answer display panel
- ✓ Menu bar with Help and About dialogs

### Export Capabilities
- ✓ Export solution reports as HTML (formatted with styling)
- ✓ Export solution reports as plain text
- ✓ Timestamped filenames for easy organization
- ✓ Print-friendly HTML output

### Advanced Features
- ✓ Partial pivoting in Gaussian elimination
- ✓ Tolerance-based convergence checking
- ✓ Iteration counting with maximum iteration limits
- ✓ Equation-by-equation verification with residuals
- ✓ Numerical stability checks
- ✓ Singular matrix detection

---

## Setup Instructions

### 1. Prerequisites
Ensure you have Python 3.7+ installed. Check by running:
```bash
python --version
```

### 2. Install Dependencies

#### Windows:
```bash
pip install numpy
```

#### macOS:
```bash
pip3 install numpy
```

#### Linux:
```bash
sudo apt-get install python3-tk
pip3 install numpy
```

**Note:** Tkinter may need separate installation on Linux:
```bash
sudo apt-get install python3-tk
```

### 3. Run the Application

Navigate to the project directory and run:

#### Windows:
```bash
python main.py
```

#### macOS/Linux:
```bash
python3 main.py
```

The GUI window should open immediately.

### 4. Verify Installation

Run the included test suite:
```bash
python test.py
```

All tests should pass.

---

## Usage

1. **Launch Application:** Run `main.py`
2. **Enter Equations:** Input your system of linear equations in the input area
3. **Select Method:** Choose between "Gaussian Elimination" or "Jacobi Iteration"
4. **Click Compute:** Press the "Compute" button to solve
5. **Review Results:** Check the solution trail and final answer
6. **Export (Optional):** Click "Export Report" to save the solution

---

## Limitations

### Current Limitations

1. **System Size:**
   - Only 2×2 and 3×3 systems supported
   - Cannot solve larger systems (4×4, 5×5, etc.)

2. **Numerical Precision:**
   - Floating-point arithmetic limitations apply
   - Very large or very small coefficients may cause numerical errors
   - Coefficient range: -1×10¹⁰ to 1×10¹⁰

3. **Matrix Properties:**
   - Requires non-singular coefficient matrices for unique solutions
   - Singular or nearly-singular matrices are detected but cannot be solved
   - Jacobi method requires diagonally dominant coefficient matrix for convergence

4. **Jacobi Iteration Constraints:**
   - Default 100 iteration limit may not be sufficient for all problems
   - Requires diagonal elements to be non-zero
   - Not guaranteed to converge for all diagonally dominant systems

5. **UI Constraints:**
   - Text areas limited to practical display sizes
   - Very long solution trails may impact performance
   - Export file size depends on number of steps

6. **Input Constraints:**
   - Variables must be single letters (a-z, A-Z)
   - No multi-letter variables (e.g., "x1", "x2")
   - No support for implicit multiplication (must write `2*x`, not `2x` if unclear)

### Known Issues

- No support for complex (imaginary) solutions
- Round-off errors may accumulate in iterative methods
- Matrix rows that are exactly proportional are detected, but near-proportional rows may cause issues
- Exporting very large reports may take a moment to process