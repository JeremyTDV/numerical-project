# Linear System Solver v1.0 - User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Interface Overview](#interface-overview)
3. [Step-by-Step Examples](#step-by-step-examples)

---

## Getting Started

### Installation Checklist
- [ ] Python 3.7+ is installed
- [ ] NumPy is installed (`pip install numpy`)
- [ ] Tkinter is available (bundled with Python on Windows/macOS)
- [ ] Project files are in a folder

### Launching the Application

**Windows:**
```bash
python main.py
```

**macOS/Linux:**
```bash
python3 main.py
```

A window titled "Linear System Solver" should appear.

---

## Interface Overview

### UI Components

**Input Area:**
- Text field for entering equations
- Method selector dropdown
- Buttons: Compute, Clear, Export Report

**Solution Trail:**
- Scrollable text area showing all steps
- Organized into sections: GIVEN, METHOD, STEPS, STOPPING REASON, FINAL, VERIFICATION, SUMMARY

**Final Answer:**
- Quick reference display of solution values

**Menu Bar:**
- Help menu with About and Exit options
- Keyboard shortcut: F1 for About

---

## Step-by-Step Examples

### Example 1: Solving a 2×2 System with Gaussian Elimination

**Problem:** Solve the system
```
2x + y = 5
x + 3y = 6
```

**Steps:**

1. **Launch the application**

2. **Enter the equations**
   - Click in the input text area
   - Type:
     ```
     2x + y = 5
     x + 3y = 6
     ```

3. **Select method**
   - Verify "Gaussian Elimination" is selected (default)

4. **Click Compute**
   - Button is located below the input area

5. **Review results**

   **Solution Trail shows:**
   - **GIVEN:** Your input equations
   - **METHOD:** Gaussian elimination with back substitution
   - **STEPS:** Shows the augmented matrix transformation:
     ```
     Initial: [2, 1 | 5]    Pivot row
              [1, 3 | 6]
     
     After swap: [2, 1 | 5]
                 [1, 3 | 6]
     
     After elimination: [1, 0.5 | 2.5]
                        [0, 2.5 | 3.5]
     ```
   - **FINAL:** x = 1.8, y = 1.4
   - **VERIFICATION:** Confirms both equations are satisfied

6. **Export (optional)**
   - Click "Export Report"
   - Choose HTML (formatted) or TXT (plain text)
   - Select save location
   - File is saved with timestamp

---

### Example 2: Solving a 3×3 System with Jacobi Iteration

**Problem:** Solve using Jacobi method
```
4x + y - z = 12
x + 5y + 2z = 18
2x + 2y + 5z = 20
```

**Steps:**

1. **Enter equations**
   ```
   4x + y - z = 12
   x + 5y + 2z = 18
   2x + 2y + 5z = 20
   ```

2. **Select Jacobi Iteration**
   - Click the method dropdown
   - Select "Jacobi Iteration"

3. **Click Compute**

4. **Review results**

   **Solution Trail shows:**
   - **GIVEN:** Your equations (note: system is diagonally dominant ✓)
   - **METHOD:** Jacobi iteration
   - **STEPS:** Shows iterations:
     ```
     Iteration 1: x = [3.0, 3.6, 4.0], max diff = 3.0
     Iteration 2: x = [2.43, 3.04, 3.52], max diff = 0.57
     Iteration 3: x = [2.28, 3.08, 3.56], max diff = 0.15
     ...
     Iteration N: max diff = 0.0000... (converged)
     ```
   - **FINAL:** Converged solution
   - **VERIFICATION:** Confirms solution accuracy

5. **Convergence Notes**
   - Jacobi iteration refines the solution iteratively
   - Shows each iteration's progress
   - Stops when convergence criterion is met or max iterations reached

**Expected Behavior:** Converges in 10-20 iterations

---

### Example 3: Handling an Invalid System

**Problem:** Try to solve an inconsistent system
```
x + y = 5
2x + 2y = 8
```

**What Happens:**

1. **Input validation fails**
   - Error message appears: "Equations 1 and 2 are linearly dependent"
   - Solution trail shows: "VALIDATION ERROR"

2. **Why it fails:**
   - The second equation is not a valid multiple of the first
   - 2(x + y) = 2(5) → 2x + 2y = 10 (not 8)
   - System is inconsistent

3. **What to do:**
   - Check your equations for typos
   - Click "Clear" to reset
   - Enter corrected equations
   - Try again

---
