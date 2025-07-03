# Compiler
# 🎯 GREEK++ Compiler

A full pipeline compiler for the educational programming language **GREEK++**, developed as part of the "Compilers" course at [Your University].

## 📌 Overview

This compiler takes a `.gr` source file written in a pseudo-Greek language (GREEK++) and performs:

- Lexical Analysis
- Syntax Analysis
- Semantic Analysis (Symbol Table)
- Intermediate Code Generation (Quad format)
- Final Code Generation in RISC-V Assembly
- Optionally, writes C-like pseudocode

---

## 🔧 Features

- Support for variables, constants, procedures, functions with parameters
- Conditionals (`εάν`, `τότε`, `εάν_τέλος`, `αλλιώς`)
- Loops (`όσο`, `επανάλαβε`, `μέχρι`)
- Call-by-value and call-by-reference parameters
- Output of:
  - `output.sym`: symbol table
  - `output.asm`: final RISC-V code
  - `output.int`: intermediate quads

---

## 🚀 How to Use

### 🖥️ Requirements
- Python 3.10+

### 📦 Run the compiler

```bash
python greek_5371.py your_program.gr

