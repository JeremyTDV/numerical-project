# Linear System Solver

A simple calculator that solves systems of linear equations step-by-step. Perfect for learning how computers solve math problems!

## What It Does

- Solves 2x2 and 3x3 systems of equations
- Shows you every step of the solution
- Uses Gaussian Elimination method
- Easy-to-use graphical interface

## How to Use

### Step 1: Install What You Need
```bash
pip install numpy
```

### Step 2: Run the Program
```bash
python main.py
```

### Step 3: Solve Your Equations
1. Type your equations like this:
   ```
   2x + y = 5
   x + 3y = 6
   ```
2. Choose solving method:
   - **Gaussian Elimination** (recommended for most systems)
   - **Jacobi Iteration** (best for diagonally dominant systems)
3. Click "Compute"
4. Watch the step-by-step solution appear!

## Equation Examples

**Simple 2x2 System:**
```
2x + y = 5
x + 3y = 6
```

**3x3 System:**
```
x + y + z = 6
2x - y + z = 3
x + 2y - z = 2
```

**Jacobi Test System (Diagonally Dominant):**
```
4x + y = 5
x + 3y = 6
```

## Solving Methods Available

### Gaussian Elimination (Recommended)
- Works for any system of equations
- Gives exact answers
- Shows all the matrix operations step-by-step
- Eliminates variables one by one to find the solution

### Jacobi Iteration
- Works best for diagonally dominant systems
- Uses iterative guessing and improving
- Shows convergence process step-by-step
- Good for large systems where exact methods are slow

## What the Program Shows

- **Given**: Your original equations
- **Steps**: Every calculation step-by-step
- **Stopping Reason**: Why the program stopped solving
- **Final Answer**: The solution for x, y, z...
- **Verification**: Checks if the answer is correct

## Files in the Project

```
numerical-project-Week-6/
|-- main.py      # Starts the program
|-- solver.py    # Does the math calculations
|-- ui.py        # Creates the buttons and windows
|-- validator.py # Checks if your equations are correct
|-- test.py      # Tests to make sure everything works
|-- README.md    # This file
```

## Common Problems & Solutions

**"GUI not showing up"** - Make sure you have Python 3.6 or higher

**"Import error"** - Run `pip install numpy`

**"Equation not valid"** - Check your format:
- Use `=` sign
- Use single letters for variables (x, y, z)
- Numbers can be whole or decimal

**"No solution found"** - Your equations might not have a unique solution

## Testing the Program

Run the tests to see examples:
```bash
python test.py
```

This will test different types of equations and show you how they work.

## System Requirements

- Python 3.6 or higher
- Windows, Mac, or Linux
- About 100MB of memory
- Screen resolution of 900x700 or higher

## Quick Tips

- Use simple variable names (x, y, z)
- Check your equation format if you get errors
- Watch the step-by-step solution to learn the process
- The program uses Gaussian Elimination automatically

---
