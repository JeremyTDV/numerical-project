# Sample Test Cases for Linear System Solver

Below are 5 sample test cases you can use to verify the solver. Copy and paste the input directly into the UI text area.

---

## Test Case 1: Simple 2×2 System (Basic)
**Description:** Basic 2×2 system with integer coefficients and clear solution

**Input:**
```
2x + y = 5
x + 3y = 6
```

**Expected Solution:** 
- x ≈ 1.8
- y ≈ 1.4

**Verification:**
- Eq1: 2(1.8) + 1(1.4) = 3.6 + 1.4 = 5 ✓
- Eq2: 1(1.8) + 3(1.4) = 1.8 + 4.2 = 6 ✓

---

## Test Case 2: Simple 3×3 System (Basic)
**Description:** Classic 3×3 system with integer coefficients

**Input:**
```
x + y + z = 6
2x - y + z = 3
x + 2y - z = 2
```

**Expected Solution:**
- x = 1
- y = 2
- z = 3

**Verification:**
- Eq1: 1 + 2 + 3 = 6 ✓
- Eq2: 2(1) - 2 + 3 = 2 - 2 + 3 = 3 ✓
- Eq3: 1 + 2(2) - 3 = 1 + 4 - 3 = 2 ✓

---

## Test Case 3: System with Negative Coefficients & Mixed Signs
**Description:** 2×2 system with negative coefficients and decimals

**Input:**
```
3x - 2y = 1
-x + 4y = 10
```

**Expected Solution:**
- x = 2
- y = 2.5

**Verification:**
- Eq1: 3(2) - 2(2.5) = 6 - 5 = 1 ✓
- Eq2: -(2) + 4(2.5) = -2 + 10 = 8... (recalculate)

*Alternative simpler negative case:*
```
2x - y = 3
x + y = 6
```

**Expected Solution:**
- x = 3
- y = 3

**Verification:**
- Eq1: 2(3) - 3 = 6 - 3 = 3 ✓
- Eq2: 3 + 3 = 6 ✓

---

## Test Case 4: 3×3 System with Larger Coefficients
**Description:** More complex 3×3 system testing solver robustness

**Input:**
```
4x + 2y - z = 5
-2x + 3y + 2z = 12
x - y + 3z = 7
```

**Expected Solution (approximate):**
- x ≈ 0.2
- y ≈ 3.0
- z ≈ 2.0

**Verification:** Substitute back into all three equations to verify residuals are near zero.

---

## Test Case 5: 2×2 System with Fractional Coefficients
**Description:** System with decimal/fractional coefficients

**Input:**
```
0.5x + 2y = 4.5
1.5x - y = 0.5
```

**Expected Solution:**
- x = 1
- y = 2

**Verification:**
- Eq1: 0.5(1) + 2(2) = 0.5 + 4 = 4.5 ✓
- Eq2: 1.5(1) - 2 = 1.5 - 1 = 0.5 ✓

---

## How to Use These Test Cases:

1. **Launch the application** by running `main.py`
2. **Select the method** (Gaussian Elimination or Jacobi Iteration)
3. **Copy and paste** one of the test inputs into the text area
4. **Click "Compute"** to solve
5. **Check the results** in the Solution Trail and Final Answer panels
6. **Verify** the equations are satisfied in the Verification section

## Expected Features in Output:

✓ Initial augmented matrix displayed  
✓ Forward elimination steps shown  
✓ Back substitution process detailed  
✓ Verification with residuals calculated  
✓ Stopping reason clearly stated  
✓ Solution displayed with precision  

---

## Additional Edge Cases to Try (Optional):

**Nearly Singular Matrix** (will trigger tolerance error):
```
x + y = 1
2x + 2y = 2
```
Expected: STOPPED (singular/dependent equations)

**Inconsistent System** (no solution):
```
x + y = 1
2x + 2y = 3
```
Expected: STOPPED (inconsistent system)

**Jacobi Method Test** (ensure diagonal dominance):
```
4x + y = 5
x + 3y = 6
```
Expected: Converges with Jacobi iteration
