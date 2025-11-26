# Simple Expression Interpreter

A lightweight, educational expression interpreter written in Python.  
It features a hand-written lexer and recursive-descent parser capable of evaluating arithmetic expressions, comparisons, square roots, and logarithms through an interactive prompt.

## Inspiration

This project was inspired by Ruslan Spivak’s *“Let’s Build a Simple Interpreter”* series.  
After completing Part 1, the project evolved into a more fully-featured interpreter exploring parsing, evaluation, and mathematical operations.

## Features

- **Interactive REPL** with a `calc>` prompt  
- **Arithmetic operators:** `+`, `-`, `*`, `/`, `%`, `^`  
- **Parentheses** for grouping  
- **Comparison operators:** `>`, `>=`, `<`, `<=`, `==`, `!=`  
- **Square roots:** `sqrt(expr)`  
- **Logarithms:**  
  - Base-2: `log2(n)`  
  - Base-10: `log10(n)`  
- **Boolean outputs** represented as `TRUE` / `FALSE`  
- **Error handling** for invalid syntax, division by zero, and logarithm domain errors  

---

## How It Works

### 1. Lexing (Tokenization)

The interpreter scans input one character at a time and produces `Token` objects representing:

- Integer literals  
- Operators  
- Parentheses  
- Keywords (`sqrt`, `log2`, `log10`)  

Multi-character tokens such as `>=`, `<=`, `==`, `!=`, and keyword identifiers are handled explicitly.  
Each `Token` contains:

- **Type** – A symbolic category (e.g., `INT`, `PLUS`, `LOG2`)  
- **Value** – The literal text of the token  

Whitespace is ignored.

---

### 2. Parsing & Evaluation (Recursive-Descent)

Parsing and evaluation happen simultaneously (no AST construction), keeping the implementation concise.

#### `expr()`
- Top-level rule for expression evaluation  
- Handles addition and subtraction  
- Prevents further arithmetic evaluation on boolean results  

#### `comparison()`
- Evaluates a left `term()` and optionally a comparison operator + right `term()`  
- Returns `TRUE` or `FALSE` when a comparison is performed  

#### `term()`
- Handles high-precedence operators: `*`, `/`, `%`, `^`  
- Performs left-associative evaluation  
- Prevents division by zero  

#### `factor()`
- Handles:  
  - Unary `+` and `-`  
  - Integer literals  
  - Parentheses  
  - `sqrt(expr)`  
  - `log2(expr)` and `log10(expr)`  
- Logarithms use a custom natural-log implementation with change-of-base

---

### 3. Logarithm Implementation

The internal `_ln` function uses a series expansion:

- Employs the identity with `t = (x - 1) / (x + 1)`  
- Computes a finite approximation of the natural logarithm  
- Raises `ValueError` for invalid domains (`x <= 0`)

---

## Requirements

- **Python 3.10+** (uses `match` / `case` syntax)

---

## Installation & Usage

### Clone the repository

```bash
git clone git@github.com:Mixzpai/Basic-Python-Interpreter.git
cd Basic-Python-Interpreter
```

### Run the REPL

If your entry point is `main.py`:

```bash
python main.py
```

Or run the interpreter module directly:

```bash
python calc.py
```

At the `calc>` prompt, try expressions such as:

```
1 + 2 * 3
(10 - 3) * 4
sqrt(16)
log2(8)
log10(1000)
2^3^2
10 / 2 + 3
5 > 3
5 == 2 * 2
sqrt(9) >= 3
log2(8) == 3
```

Each input is immediately parsed and evaluated.

---

## Error Handling

- **Syntax errors:**  
  Unexpected characters or malformed token sequences raise parsing errors.

- **Division by zero:**  
  `10 / 0` → `ZeroDivisionError("division by zero")`

- **Logarithm domain errors:**  
  `log2(0)` or `log10(-5)` → `ValueError("Domain error: logarithm undefined for x <= 0")`

---

## Future Improvements

**Add:**
- Floating-point numbers
- Fraction operations  
- Variables and assignment  
- Logical operators
- Matrix operations
- User Manual/Documentation (REPL)
- Welcome banner (REPL)
- Basic binary operations/conversions  

**Improve:**
- Error messages with character/line position  
- Clear separation of lexer, parser, and evaluator  

**Extend:**
- Additional math functions (sin, cos, tan, etc.)  
- A small scripting syntax using this expression engine
