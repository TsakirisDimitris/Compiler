🇬🇷 GREEK++ Compiler
A compiler for the GREEK++ language, created for the "Compilers" course at University of Ioannina.
This project compiles .gr files written in a pseudo-Greek programming language and outputs:

Intermediate code (quadruples)
Final code in RISC-V Assembly
A symbol table with full scope and offset information
🛠️ Features
This compiler implements all major compiler phases:

✅ Lexical Analysis (tokenize())
✅ Syntax Analysis (recursive descent parser)
✅ Semantic Analysis (symbol table with scoped entries)
✅ Intermediate Code Generation (quads)
✅ Final Code Generation in RISC-V Assembly
Output Files:
output.sym → Symbol table (scoped offsets, argument lists, frame lengths)
output.asm → Final executable code in RISC-V Assembly
output.int → Intermediate code in quad format (optional)
output.c → Pseudo C-code (if enabled)
📄 Language and Grammar
Language: GREEK++
A simplified, structured Greek-language programming language with support for:

Variable declarations (δήλωση x, y;)
Procedures and functions with parameters (διαδικασία, συνάρτηση)
Control flow: εάν, τότε, αλλιώς, εάν_τέλος, όσο, επανάλαβε, μέχρι
I/O: διάβασε, γράψε
Expressions: +, -, *, /, <, <=, =, <>, και, ή
🚀 How to Run
🖥️ Requirements:
Python 3.10 or newer
📦 Usage:
python greek_5371.py sample.gr
