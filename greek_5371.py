#Τσακίρης Δημήτρης ΑΜ 5371
import sys
from write_to_c import write_to_c

if len(sys.argv) < 2: 
    print("Σφάλμα. Παρακαλώ κάντε εισαγωγή ξανά.")
    sys.exit(1)

input_file = sys.argv[1]

try:
    with open(input_file, "r", encoding="utf-8") as f:
        source_code = f.read()
except FileNotFoundError:
    print(f"Σφάλμα: Το αρχείο '{input_file}' δεν βρέθηκε.")
    sys.exit(1)
 
print(f"Διαβάστηκε το αρχείο: {input_file}")

KEYWORDS = ['πρόγραμμα', 'δήλωση', 'σταθερές', 'εάν', 'τότε', 'αλλιώς', 'εάν_τέλος',
            'επανάλαβε', 'μέχρι', 'όσο', 'όσο_τέλος', 'για', 'έως', 'με_βήμα',
            'για_τέλος', 'διάβασε', 'γράψε', 'συνάρτηση', 'διαδικασία',
            'διαπροσωπεία', 'είσοδος', 'έξοδος', 'αρχή_συνάρτησης', 'τέλος_συνάρτησης',
            'αρχή_διαδικασίας', 'τέλος_διαδικασίας', 'αρχή_προγράμματος', 'τέλος_προγράμματος',
            'ή', 'και','επιστροφή', 'εκτέλεσε']
 
ARITHMETIC_OPERATORS = ['+', '-', '*', '/']
COMPARISON_OPERATORS = ['<', '>', '<=', '>=', '<>', '=']
ASSIGNMENT_OPERATOR = ':='
SEPARATORS = [';', ',', ':']
GROUPING_SYMBOLS = ['(', ')', '[', ']', '"']
COMMENT_SYMBOLS = ['{', '}']
REFERENCE_PARAMETERS = ['%']
GREEK_ALPHABET = "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψωΆΈΉΊΌΎΏάέήίόύώ"
ENGLISH_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
DIGITS = "0123456789"
VALID_IDENTIFIER_CHARS = GREEK_ALPHABET + ENGLISH_ALPHABET + DIGITS

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.i = 0

    def is_identifier(self, word):
        if word in KEYWORDS:
            return False
        
        if word[0] not in (GREEK_ALPHABET + ENGLISH_ALPHABET):
            return False
        
        if len(word) > 30:
            return False
        
        if word[0] == "_" or word[-1] == "_":
            return False
        
        for char in word:
            if char not in (VALID_IDENTIFIER_CHARS + "_"):
                return False
        return True

    def tokenize(self):
        while self.i < len(self.source_code):
            char = self.source_code[self.i]

            if char.isspace():
                self.i += 1
                continue

            elif char == '{':
                while self.i < len(self.source_code) and self.source_code[self.i] != '}':
                    self.i += 1
                
                if self.i == len(self.source_code):  
                    print("Σφάλμα: Μη κλειστό σχόλιο { ... ")
                    sys.exit(1)
                self.i += 1 
                
            elif char.isdigit():
                num = char
                self.i += 1
                while self.i < len(self.source_code) and self.source_code[self.i].isdigit():
                    num += self.source_code[self.i]
                    self.i += 1
                self.tokens.append(("NUMBER", num))

            elif char.isalpha():
                word = char
                self.i += 1
                while self.i < len(self.source_code) and (self.source_code[self.i].isalnum() or self.source_code[self.i] == "_"):
                    word += self.source_code[self.i]
                    self.i += 1
                
                if word in KEYWORDS:
                    self.tokens.append(("KEYWORD", word))
                
                elif self.is_identifier(word):
                    self.tokens.append(("IDENTIFIER", word))
                
                else:
                    print(f"Σφάλμα: Μη έγκυρο αναγνωριστικό '{word}'")

            elif self.source_code[self.i:self.i + 2] in COMPARISON_OPERATORS:
                self.tokens.append(("COMPARISON_OPERATOR", self.source_code[self.i:self.i + 2]))
                self.i += 2
            
            elif char in COMPARISON_OPERATORS:
                self.tokens.append(("COMPARISON_OPERATOR", char))
                self.i += 1 
            
            elif self.source_code[self.i:self.i + 2] == ":=":
                self.tokens.append(("ASSIGNMENT_OPERATOR", ":="))
                self.i += 2
            
            elif char in ARITHMETIC_OPERATORS:
                self.tokens.append(("ARITHMETIC_OPERATOR", char))
                self.i += 1
            
            elif char in SEPARATORS:
                self.tokens.append(("SEPARATOR", char))
                self.i += 1
            
            elif char in GROUPING_SYMBOLS:
                self.tokens.append(("GROUPING_SYMBOLS", char))
                self.i += 1
            
            elif char in REFERENCE_PARAMETERS:
                self.tokens.append(("REFERENCE_SYMBOL", char))
                self.i += 1
            
            else:
                print(f"Σφάλμα: Άγνωστο σύμβολο '{char}'")
                self.i += 1

        return self.tokens

lexer = Lexer(source_code)
tokens = lexer.tokenize()

for token in tokens:
    print(token)

class Symbol:
    def __init__(self, name, kind, scope, offset=None, entity=None, parMode=None):
        self.name = name
        self.kind = kind
        self.scope = scope
        self.offset = offset
        self.entity = entity
        self.parMode = parMode  
        self.argument = []    
        
        self.framelength = 0       
        self.startQuad = None      

    def __repr__(self):
         return (f"Symbol(name={self.name}, kind={self.kind}, scope={self.scope}, "
                f"offset={self.offset}, parMode={self.parMode}, "
                f"args={self.argument}, frame={self.framelength}, "
                f"startQuad={self.startQuad})")

class SymbolTable:
    def __init__(self):
        self.scopes = []
        self.scope_level = -1   # τρέχον επίπεδο
        self.offset_stack = []
        self.all_symbols = []   # νέα λίστα για όλα τα σύμβολα

    def openscope(self):
        self.scope_level += 1
        self.scopes.append([])
        self.offset_stack.append(12)

    def closescope(self):
        if self.scope_level < 0:
            return

        current_scope = self.scopes[-1]
        current_level = self.scope_level

        framelength = self.offset_stack[-1]

        for sym in current_scope:
            if sym.kind in ["function", "procedure"]:
                sym.framelength = framelength

        mode = "w" if self.scope_level == 0 else "a"
        with open("output.sym", mode, encoding="utf-8") as f:
            f.write(self.dump_scope(current_level))

        self.all_symbols.extend(current_scope)
        self.scopes.pop()
        self.scope_level -= 1
        self.offset_stack.pop()

    def insert(self, name, kind, parMode=None):
        print(f"DEBUG: insert({name}, {kind})")
        offset = self.offset_stack[-1]
        symbol = Symbol(name, kind, self.scope_level, offset=offset, parMode=parMode)

        if kind in ["variable", "parameter", "temp"]:
            self.offset_stack[-1] += 4 

        self.scopes[-1].append(symbol)

        if kind == "parameter":
            for sym in reversed(self.scopes[-1]):
                if sym.kind in ["function", "procedure"]:
                    sym.argument.append({'name': name, 'parMode': parMode})
                    break

        return symbol

    def lookup(self, name):
        for scope in reversed(self.scopes):
            for symbol in scope:
                if symbol.name == name:
                    return symbol
  
        for symbol in self.all_symbols:
            if symbol.name == name:
                return symbol
        return None

    def dump_scope(self, level):
        if level < 0 or level >= len(self.scopes):
            return f"Σφάλμα: Δεν υπάρχει επίπεδο {level}\n"

        output = f"--- Scope Level {level} ---\n" + "-" * 50 + "\n"
        for symbol in self.scopes[level]:
            if symbol.kind == "program":
                output += f"{symbol.name} / {symbol.offset}\n"
            
            elif symbol.kind == "variable":
                output += f"{symbol.name} / {symbol.offset}\n"
            
            elif symbol.kind == "constant":
                value = getattr(symbol, "value", "?")
                output += f"{symbol.name} = {value}\n"
            
            elif symbol.kind == "parameter":
                mode = "cv" if symbol.parMode == "cv" else "ref"
                output += f"{symbol.name} / {symbol.offset} / {mode}\n"
            
            elif symbol.kind == "function":
                output += f"{symbol.name} / {len(symbol.argument)} / {symbol.framelength}\n"
            
            elif symbol.kind == "procedure":
                output += f"{symbol.name} / {len(symbol.argument)} / {symbol.framelength}\n"
            
            elif symbol.kind == "temp":
                output += f"{symbol.name} / {symbol.offset}\n"

        output += "-" * 50 + "\n\n"
        return output

    def get_frame_length(self):
        return self.offset_stack[-1] if self.offset_stack else 0

class IntermediateCode:
        def __init__(self,symtab):
            self.code = []
            self.temp_counter = 0
            self.line_number = 1 
            self.label_counter = 0
            self.symtab = symtab
            self.cg = CodeGenerator(symtab)
            
        def new_temp(self):
            self.temp_counter += 1
            return f"t@{self.temp_counter}"
        
        def new_label(self):
            self.label_counter += 1
            return f"L{self.label_counter}"
            
        def emit(self,op,arg1,arg2,result):
            self.code.append((self.line_number, op, arg1, arg2, result))
            self.line_number += 1
        
        def backpatch(self, list_of_quads, label):
            for quad_index in list_of_quads:
                quad_index = int(quad_index)  
                if 1 <= quad_index <= len(self.code):
                    quad = self.code[quad_index - 1]
                    self.code[quad_index - 1] = (quad[0], quad[1], quad[2], label)

                else:
                    print(f"DEBUG: Προσπάθεια backpatch σε λάθος θέση {quad_index}")

        def nextquad(self):
            return self.line_number
   
        def __str__(self):
            output = ""
            label_to_line = {}
            for instr in self.code:
                if isinstance(instr, tuple) and len(instr) == 5:
                    _, op, _, _, res = instr

                    if op == "label" and isinstance(res, str):
                        label_to_line[res] = None 

            current_line = 1
            for instr in self.code:

                if isinstance(instr, tuple) and len(instr) == 5:
                    _, op, _, _, res = instr

                    if op == "label" and isinstance(res, str):
                        label_to_line[res] = current_line  # δίνουμε αριθμό στο label

                    else:
                        current_line += 1  # μόνο για μη-label εντολές
      
            display_line = 1
            for instr in self.code:
                if len(instr) != 5:
                    continue

                _, op, arg1, arg2, result = instr

                if op == "label":
                    continue 

                if isinstance(result, str) and result in label_to_line:
                    result = label_to_line[result]

                if isinstance(arg1, str) and arg1 in label_to_line:
                    arg1 = label_to_line[arg1]

                if isinstance(arg2, str) and arg2 in label_to_line:
                    arg2 = label_to_line[arg2]

                arg1 = arg1 if arg1 is not None else "_"
                arg2 = arg2 if arg2 is not None else "_"
                result = result if result is not None else "_"

                output += f"{display_line} : {op} , {arg1} , {arg2} , {result}\n"
                display_line += 1

            return output
    
        def generate_final_code(self, symtab):
            symtab.scope_level = 0
            codegen = CodeGenerator(symtab)
            output_lines = []
            par_index = 0

            first_label = None
            for quad in self.code:
                _, op, x, _, _ = quad
                if op == "begin_block":
                    first_label = x
                    break

            last_endblock_label = None
            for quad in reversed(self.code):
                if quad[1] == "end_block":
                    last_endblock_label = quad[0]
                    break

            if first_label:
                output_lines.append("L0:")
                output_lines.append(f"# 0: jump, _, _, {first_label}")
                output_lines.append(f"\tj L{first_label}")

            for quad in self.code:
                label = quad[0]
                op, x, y, z = quad[1:]

                x_dbg = x if x is not None else "_"
                y_dbg = y if y is not None else "_"
                z_dbg = z if z is not None else "_"

                if op != "begin_block":
                    output_lines.append(f"L{label}:")
                    output_lines.append(f"# {label}: {op}, {x_dbg}, {y_dbg}, {z_dbg}")

                if op == ":=":
                    codegen.loadvr(x, "t1", output_lines)
                    codegen.storerv("t1", z, output_lines)
 
                elif op in {"+", "-", "*", "/"}:
                    codegen.loadvr(x, "t1", output_lines)
                    codegen.loadvr(y, "t2", output_lines)
                    output_lines.append(f"{ {'+':'add','-':'sub','*':'mul','/':'div'}[op] } t1, t1, t2")
                    codegen.storerv("t1", z, output_lines)

                elif op == "jump":
                    output_lines.append(f"j {z}")

                elif op in ["<", "<=", ">", ">=", "=", "<>"]:
                    codegen.loadvr(x, "t1", output_lines)
                    codegen.loadvr(y, "t2", output_lines)
                    relop_map = {"<":"blt","<=":"ble",">":"bgt",">=":"bge","=":"beq","<>":"bne"}
                    output_lines.append(f"{relop_map[op]} t1, t2, {z}")

                elif op == "call":
                    output_lines.append("sw ra, 0(sp)")
                    
                    symbol = symtab.lookup(x)
                    if symbol is None:
                        raise Exception(f"Undeclared function: {x}")
                    if symbol.startQuad is None:
                        raise Exception(f"Function '{x}' does not have a startQuad assigned.")

                    output_lines.append(f"jal L{symbol.startQuad}")
                    output_lines.append("lw ra, 0(sp)")
                    par_index = 0

                elif op == "par":
                    if z == "RET":
                        symbol = symtab.lookup(x)

                        if symbol is None:
                            raise Exception(f"Undeclared variable: {x}")
                        output_lines.append(f"addi t0, sp, -{symbol.offset}")
                        output_lines.append("sw t0, -8(sp)")

                    else:
                        symbol = symtab.lookup(x)

                        if symbol is None:
                            raise Exception(f"Undeclared parameter {x}")
                        offset = 12 + par_index * 4

                        if symbol.parMode == "cv":
                            codegen.loadvr(x, "t0", output_lines)
                            output_lines.append(f"sw t0, -{offset}(sp)")

                        elif symbol.parMode == "ref":

                            if symbol.scope == symtab.scope_level:
                                output_lines.append(f"addi t0, sp, -{symbol.offset}")

                            else:
                                codegen.gnlvcode(x, output_lines)
                            output_lines.append(f"sw t0, -{offset}(sp)")

                        par_index += 1

                elif op == "retv":
                    codegen.loadvr(x, "t1", output_lines)
                    output_lines.append("lw t0, -8(sp)")
                    output_lines.append("sw t1, 0(t0)")

                elif op == "begin_block":
                    
                    if x == "Main":
                        output_lines.append("LMain:")
                        output_lines.append(f"L{label}:")

                    else:
                        output_lines.append(f"L{x}:")
                        output_lines.append(f"L{label}:")

                    output_lines.append("sw ra, -0(sp)")

                elif op == "end_block":

                    if label != last_endblock_label:
                        output_lines.append("lw ra, 0(sp)")
                        output_lines.append("jr ra")

                elif op == "out":
                    symbol = symtab.lookup(x)

                    if symbol is None:
                        raise Exception(f"Undeclared variable: {x}")

                    offset = symbol.offset
                    reg_number = (offset - 12) // 4
                    reg = f"t{reg_number + 1}"

                    output_lines.append(f"lw {reg}, -{offset}(sp)")
                    output_lines.append("\t...")

                elif op == "in":
                    output_lines.append("li a7, 5")
                    output_lines.append("ecall")
                    codegen.storerv("a0", x, output_lines)

                elif op == "halt":
                    output_lines.append("li a7, 10")
                    output_lines.append("ecall")

            with open("output.asm", "w", encoding="utf-8") as f:
                for line in output_lines:

                    if line.startswith("L") and line.endswith(":"):
                        f.write(f"{line}\n")

                    elif line.startswith("#"):
                        f.write(f"{line}\n")

                    else:
                        f.write(f"\t{line}\n")

class CodeGenerator:
    def __init__(self, symtab):
        self.symtab = symtab
        self.symtab.scope_level = 0
        
    def gnlvcode(self, id_name, output_lines):
        symbol = self.symtab.lookup(id_name)
        if symbol is None:
            raise Exception(f"Undeclared variable: {id_name}")
        
        nesting_diff = self.symtab.scope_level - symbol.scope
        output_lines.append("lw t0, -4(sp)")  # αρχικό static link

        for _ in range(nesting_diff - 1):
            output_lines.append("lw t0, -4(t0)")

        output_lines.append(f"addi t0, t0, -{symbol.offset}")

    def loadvr(self, v, r, output_lines):
        symbol = self.symtab.lookup(v)
        if symbol is None:

            if v.isdigit():
                output_lines.append(f"li {r}, {v}")
                return

            else:
                raise Exception(f"Undeclared variable: {v}")

        if symbol.kind in ["variable", "temp"]:

            if symbol.scope == self.symtab.scope_level:
                output_lines.append(f"lw {r}, -{symbol.offset}(sp)")

            else:
                self.gnlvcode(v, output_lines)
                output_lines.append(f"lw {r}, 0(t0)")

        elif symbol.kind == "parameter":

            if symbol.parMode == "cv":

                if symbol.scope == self.symtab.scope_level:
                    output_lines.append(f"lw {r}, -{symbol.offset}(sp)")

                else:
                    self.gnlvcode(v, output_lines)
                    output_lines.append(f"lw {r}, 0(t0)")

            elif symbol.parMode == "ref":

                if symbol.scope == self.symtab.scope_level:
                    output_lines.append(f"lw t0, -{symbol.offset}(sp)")

                else:
                    self.gnlvcode(v, output_lines)
                    output_lines.append(f"lw t0, 0(t0)")
                output_lines.append(f"lw {r}, 0(t0)")

    def storerv(self, r, v, output_lines):
        symbol = self.symtab.lookup(v)
        print(f"[DEBUG storerv] storing to: {v}, kind: {symbol.kind}, scope: {symbol.scope}, current_scope: {self.symtab.scope_level}")
        if symbol is None:
            raise Exception(f"Undeclared variable: {v}")

        if symbol.kind in ["variable", "temp"]:

            if symbol.scope == self.symtab.scope_level:
                output_lines.append(f"sw {r}, -{symbol.offset}(sp)")

            else:
                self.gnlvcode(v, output_lines)
                output_lines.append(f"sw {r}, 0(t0)")

        elif symbol.kind == "parameter":

            if symbol.parMode == "cv":

                if symbol.scope == self.symtab.scope_level:
                    output_lines.append(f"sw {r}, -{symbol.offset}(sp)")

                else:
                    self.gnlvcode(v, output_lines)
                    output_lines.append(f"sw {r}, 0(t0)")

            elif symbol.parMode == "ref":

                if symbol.scope == self.symtab.scope_level:
                    output_lines.append(f"lw t0, -{symbol.offset}(sp)")

                else:
                    self.gnlvcode(v, output_lines)
                    output_lines.append(f"lw t0, 0(t0)")
                output_lines.append(f"sw {r}, 0(t0)")

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens 
        self.current_token_index = 0  
        self.current_token = self.tokens[self.current_token_index] if self.tokens else None 
        self.symtab = SymbolTable()
        self.ic = IntermediateCode(self.symtab)

    def advance(self):
        self.current_token_index += 1
        while self.current_token_index < len(self.tokens) and not self.tokens[self.current_token_index]:
            self.current_token_index += 1

        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]        

        else:
            self.current_token = None  # Τέλος αρχείου

    def match(self, expected_type, expected_value=None):
        if self.current_token and self.current_token[0] == expected_type:            

            if expected_value is None or self.current_token[1] == expected_value:
                self.advance()            

            else:
                self.error(f"Αναμενόταν {expected_value}, αλλά βρέθηκε {self.current_token[1]}")        

        else:
            self.error(f"Αναμενόταν τύπος {expected_type}, αλλά βρέθηκε {self.current_token}")
            
    def backpatch(self, list_of_lines, label):
        for line in list_of_lines:

            if 1 <= line <= len(self.code):
                old_instr = self.code[line - 1]  # το line ξεκινάει από 1
                new_instr = (old_instr[0], old_instr[1], old_instr[2], old_instr[3], label)
                self.code[line - 1] = new_instr

            else:
                print(f"Σφάλμα: Προσπάθεια backpatch σε μη έγκυρη γραμμή {line}")

    def error(self, message):
        print(f"Σφάλμα Σύνταξης: {message}")
        exit(1)
        
    def parse_program(self):
        if self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] == "πρόγραμμα":
            self.advance()

            if self.current_token and self.current_token[0] == "IDENTIFIER":
                program_name = self.current_token[1]
                self.advance()
                self.symtab.openscope()
                self.symtab.insert(program_name,"program")
                self.ic.emit("begin_block",program_name,None,None)
                self.parse_programblock()
                self.ic.emit("halt",None,None,None)
                self.ic.emit("end_block",program_name,None,None)
                self.symtab.closescope()

            else:
                self.error("Αναμενόταν όνομα προγράμματος μετά το 'πρόγραμμα'.")

        else:
            self.error("Αναμενόταν η λέξη-κλειδί 'πρόγραμμα' στην αρχή του αρχείου.")

    def parse_programblock(self):
        self.parse_constants()
        self.parse_declarations()
        self.parse_subprograms()
        if self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] == "αρχή_προγράμματος":
            self.advance()
            self.parse_sequence()
            print("DEBUG: Τελικό token:", self.current_token)

            if self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] == "τέλος_προγράμματος":
                self.advance()

            else:
                self.error("Αναμενόταν η λέξη-κλειδί 'τέλος_προγράμματος' στο τέλος του αρχείου.")
    
    def parse_constants(self):
        while self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] == "σταθερές":
            self.advance()

            while self.current_token and self.current_token[0] == "IDENTIFIER":
                const_name = self.current_token[1]
                self.advance()

                if self.current_token and self.current_token == ("ASSIGNMENT_OPERATOR", "="):
                    self.advance()

                    if self.current_token and self.current_token[0] == "NUMBER":
                        const_value = self.current_token[1]
                        symbol = Symbol(const_name, "constant", self.symtab.scope_level)
                        symbol.value = const_value
                        self.symtab.scopes[-1].append(symbol)
                        self.advance()

                        if self.current_token and self.current_token == ("SEPARATOR", ";"):
                            self.advance()

                        else:
                            self.error("Αναμενόταν ';' μετά από δήλωση σταθεράς")

                    else:
                        self.error("Αναμενόταν αριθμός για την τιμή της σταθεράς")

                else:
                    self.error("Αναμενόταν '=' στη δήλωση σταθεράς")


    def parse_declarations(self):
        while self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] == "δήλωση":
            self.advance()
            self.parse_varlist("variable")

    def parse_varlist(self, kind="variable"):
        if self.current_token and self.current_token[0] == "IDENTIFIER":  
            var_name = self.current_token[1]
            self.symtab.insert(var_name, kind)
            self.advance()            

            while self.current_token and self.current_token == ("SEPARATOR", ","):
                self.advance()

                if self.current_token and self.current_token[0] == "IDENTIFIER": 
                    var_name = self.current_token[1]
                    self.symtab.insert(var_name, kind)
                    self.advance()

                else:
                    self.error("Αναμενόταν αναγνωριστικό (IDENTIFIER) μετά το ','")

        else:
            self.error("Αναμενόταν τουλάχιστον ένα αναγνωριστικό (IDENTIFIER) στην αρχή της λίστας μεταβλητών")

    def parse_subprograms(self):
        while self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] in ["συνάρτηση","διαδικασία"]:

            if self.current_token[1] == "συνάρτηση":
                self.parse_func()

            elif self.current_token[1] == "διαδικασία":
                self.parse_proc()
                       
    def parse_func(self):
        if self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] == "συνάρτηση":
            self.advance()

            if self.current_token and self.current_token[0] == "IDENTIFIER":
                func_name = self.current_token[1]
                self.advance()

                if self.current_token and self.current_token[0] == "GROUPING_SYMBOLS" and self.current_token[1] == '(':
                    symbol = self.symtab.insert(func_name, "function")
                    symbol.startQuad = self.ic.nextquad()
                    self.symtab.openscope()
                    self.advance()
                    self.parse_formalparlist()

                    if self.current_token and self.current_token[0] == "GROUPING_SYMBOLS" and self.current_token[1] == ')':
                        self.advance()
                        self.parse_funcblock()
                        self.symtab.closescope()
                    
                    else:
                        self.error("Αναμενόταν ')' μετά την formalparlist")
                
                else:
                    self.error("Αναμενόταν '(' μετά το όνομα συνάρτησης")
            
            else:
                self.error("Αναμενόταν όνομα συνάρτησης (IDENTIFIER)")
                
    def parse_proc(self):
        if self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] == "διαδικασία":
            self.advance()

            if self.current_token and self.current_token[0] == "IDENTIFIER":
                proc_name = self.current_token[1]
                self.advance()

                if self.current_token and self.current_token[0] == "GROUPING_SYMBOLS" and self.current_token[1] == '(':
                    self.advance()
                    self.symtab.openscope()
                    self.symtab.insert(proc_name, "procedure")
                    self.parse_formalparlist()

                    if self.current_token and self.current_token[0] == "GROUPING_SYMBOLS" and self.current_token[1] == ')':
                        self.advance()
                        self.parse_procblock()
                        self.symtab.closescope()

                    else:
                        self.error("Αναμενόταν ')' μετά την λίστα παραμέτρων στη διαδικασία")

                else:
                    self.error("Αναμενόταν '(' μετά το όνομα διαδικασίας")

            else:
                self.error("Αναμενόταν όνομα (IDENTIFIER) μετά τη λέξη-κλειδί 'διαδικασία'")
    
    def parse_formalparlist(self):
        while self.current_token and (self.current_token[0] == "REFERENCE_SYMBOL" or self.current_token[0] == "IDENTIFIER"):
            parMode = "cv"

            if self.current_token[0] == "REFERENCE_SYMBOL":
                parMode = "ref"
                self.advance()

            if self.current_token and self.current_token[0] == "IDENTIFIER":
                param_name = self.current_token[1]
                self.symtab.insert(param_name, "parameter", parMode=parMode)
                self.advance()

                if self.current_token and self.current_token[0] == "SEPARATOR" and self.current_token[1] == ",":
                    self.advance()

                else:
                    break
        
    def parse_funcblock(self):
        self.match("KEYWORD","διαπροσωπεία")
        self.parse_funcinput()
        self.parse_funcoutput()
        self.parse_declarations()
        self.parse_subprograms()
        if self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] == "αρχή_συνάρτησης":
            self.advance()
            self.parse_sequence()

            if self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] == "τέλος_συνάρτησης":
                self.advance()

        else:
            self.error("Αναμενόταν το KEYWORD 'αρχή_συνάρτησης' μετά το subprograms")
        
    def parse_procblock(self):
        self.match("KEYWORD","διαπροσωπεία")
        self.parse_funcinput()
        self.parse_funcoutput()
        self.parse_declarations()
        self.parse_subprograms()
        if self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] == "αρχή_διαδικασίας":
            self.advance()
            self.parse_sequence()    

            if self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] == "τέλος_διαδικασίας":
                self.advance()

            else:
                    self.error("Αναμενόταν το KEYWORD 'τέλος_διαδικασίας' μετά την sequence")

        else:
                self.error("Αναμενόταν το KEYWORD 'αρχή_διαδικασίας' μετά το subprograms")
   
    def parse_funcinput(self):
        if self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] == 'είσοδος':
            self.advance()
            self.parse_varlist("parameter")
            
    def parse_funcoutput(self):
        if self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] == 'έξοδος':
            self.advance()
            self.parse_varlist("parameter")
            
    def parse_sequence(self):
        while self.current_token:

            if self.current_token in [
                ("KEYWORD", "αλλιώς"),
                ("KEYWORD", "εάν_τέλος"),
                ("KEYWORD", "όσο_τέλος"),
                ("KEYWORD", "τέλος_προγράμματος"),
                ("KEYWORD", "τέλος_συνάρτησης"),
                ("KEYWORD", "τέλος_διαδικασίας"),
                ("KEYWORD", "μέχρι"),
            ]:
                break

            if self.current_token[0] == "IDENTIFIER":
                self.parse_statement()

            elif self.current_token[0] == "KEYWORD" and self.current_token[1] not in [
                "μέχρι", "εάν_τέλος", "όσο_τέλος", "τέλος_προγράμματος",
                "τέλος_συνάρτησης", "τέλος_διαδικασίας"
            ]:
                self.parse_statement()

            else:
                break

            if self.current_token == ("SEPARATOR", ";"):
                self.advance()


    def parse_statement(self):
        if self.current_token[0] == "IDENTIFIER":  
            self.parse_assignment_stat()        

        elif self.current_token[0] == "KEYWORD":

            if self.current_token[1] == "εάν":
                self.parse_if_stat()

            elif self.current_token[1] == "όσο":
                self.parse_while_stat()

            elif self.current_token[1] == "επανάλαβε":
                self.parse_do_stat()

            elif self.current_token[1] == "για":
                self.parse_for_stat()

            elif self.current_token[1] == "με_βήμα":
                self.parse_step()

            elif self.current_token[1] == "διάβασε":
                self.parse_input_stat()

            elif self.current_token[1] == "γράψε":
                self.parse_print_stat()

            elif self.current_token[1] == "εκτέλεσε":
                self.parse_call_stat()

        else:
            self.error(f"Άγνωστη εντολή: {self.current_token[1]}")
                
    def parse_assignment_stat(self):
        if self.current_token and self.current_token[0] == "IDENTIFIER":
            var_name = self.current_token[1]
            print("DEBUG: Ανάθεση σε μεταβλητή:", var_name)
            self.advance()
            print("DEBUG: Περιμένω := , έχω:", self.current_token)

            if self.current_token and self.current_token == ("ASSIGNMENT_OPERATOR", ":="):
                self.advance()
                print("DEBUG: Ξεκινάει expression από:", self.current_token)
                result = self.parse_expression()
                print("DEBUG: Τιμή επιστρεφόμενης έκφρασης:", result)
                self.ic.emit(":=",result,None,var_name)   

            else:
                self.error("Αναμενόταν το ASSIGNMENT_OPERATOR ':=' πριν το expression")

        else:
            self.error("Αναμενόταν το 'IDENTIFIER' στην αρχή της συνάρτησης")

    def parse_if_stat(self):
        print("DEBUG: Ξεκινάει IF statement")

        if self.current_token == ("KEYWORD", "εάν"):
            self.advance()
            condition = self.parse_condition()

            if len(condition) == 3:
                left, operator, right = condition
                label_true = self.ic.new_label()
                label_false = self.ic.new_label()
                self.ic.emit(operator, left, right, label_true)
                self.ic.emit("jump", None, None, label_false)

                if self.current_token == ("KEYWORD", "τότε"):
                    self.advance()

                else:
                    self.error("Αναμενόταν 'τότε' μετά το εάν")

                self.ic.emit("label", None, None, label_true)
                self.parse_sequence()

                if self.current_token and self.current_token == ("KEYWORD", "αλλιώς"):
                    self.advance()
                    label_end = self.ic.new_label()
                    self.ic.emit("jump", None, None, label_end)
                    self.ic.emit("label", None, None, label_false)
                    self.parse_sequence()
                    self.ic.emit("label", None, None, label_end)

                else:
                    self.ic.emit("label", None, None, label_false)

                if self.current_token and self.current_token == ("KEYWORD", "εάν_τέλος"):
                    self.advance()

                else:
                    self.error("Αναμενόταν 'εάν_τέλος'")

            elif len(condition) == 2:
                true_list, false_list = condition

                if self.current_token == ("KEYWORD", "τότε"):
                    self.advance()

                else:
                    self.error("Αναμενόταν 'τότε' μετά το εάν")

                self.ic.backpatch(true_list, self.ic.nextquad())
                self.parse_sequence()

                if self.current_token and self.current_token == ("KEYWORD", "αλλιώς"):
                    self.advance()
                    label_end = self.ic.new_label()
                    self.ic.emit("jump", None, None, label_end)
                    self.ic.backpatch(false_list, self.ic.nextquad())
                    self.parse_sequence()
                    self.ic.emit("label", None, None, label_end)

                else:
                    self.ic.backpatch(false_list, self.ic.nextquad())

                if self.current_token and self.current_token == ("KEYWORD", "εάν_τέλος"):
                    self.advance()

                else:
                    self.error("Αναμενόταν 'εάν_τέλος'")

            else:
                self.error("Λάθος μέγεθος επιστροφής από parse_condition")

    def parse_elsepart(self, label_else):
        if self.current_token == ("KEYWORD", "αλλιώς"):
            self.ic.emit("label", None, None, label_else)  # else label
            self.advance()
            self.parse_sequence()

        else:
            self.ic.emit("label", None, None, label_else)  # αν δεν έχει αλλιώς
    
    def parse_while_stat(self):
        if self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] == "όσο":
            self.advance()

            label_start = self.ic.new_label()
            label_body = self.ic.new_label()
            label_end = self.ic.new_label()

            self.ic.emit("label", None, None, label_start)

            condition = self.parse_condition()

            if len(condition) == 3:
                left, operator, right = condition
                self.ic.emit(operator, left, right, label_body)
                self.ic.emit("jump", None, None, label_end)         

                self.ic.emit("label", None, None, label_body)

            elif len(condition) == 2:
                true_list, false_list = condition
                self.ic.backpatch(true_list, self.ic.nextquad())
            else:
                self.error("Λάθος μέγεθος επιστροφής από parse_condition")

            if self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] == "επανάλαβε":
                self.advance()

                self.parse_sequence()

                self.ic.emit("jump", None, None, label_start)

                if len(condition) == 2:
                    self.ic.backpatch(false_list, self.ic.nextquad())

                self.ic.emit("label", None, None, label_end)

                if self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] == "όσο_τέλος":
                    self.advance()
                else:
                    self.error("Αναμενόταν 'όσο_τέλος'")
            else:
                self.error("Αναμενόταν 'επανάλαβε' μετά τη συνθήκη")
        else:
            self.error("Αναμενόταν 'όσο'")

    def parse_do_stat(self):
        if self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] == "επανάλαβε":
                    self.advance()
                    label_start = self.ic.new_label()
                    label_exit = self.ic.new_label()
                    self.ic.emit("label", None, None, label_start)
                    self.parse_sequence()

                    if self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] == "μέχρι":
                        self.advance()
                        left, operator, right = self.parse_condition()
                        self.ic.emit(operator, left, right, label_exit)
                        self.ic.emit("jump", None, None, label_start)
                        self.ic.emit("label", None, None, label_exit)

                        if self.current_token == ("SEPARATOR", ";"):
                            self.advance()

                        else:
                            self.error("Αναμενόταν ';' μετά τη συνθήκη του 'μέχρι'")

                    else:
                        self.error("Αναμενόταν το KEYWORD 'μέχρι' στο τέλος της συνάρτησης")

        else:
            self.error("Αναμενόταν το KEYWORD 'επανάλαβε' μετά την condition")
          
    def parse_for_stat(self):
        if self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] == "για":
                self.advance()

                if self.current_token and self.current_token[0] == "IDENTIFIER":
                    self.advance()

                    if self.current_token and self.current_token[0] == "ASSIGNMENT_OPERATOR" and self.current_token[1] == ":=":
                        self.advance()
                        self.parse_expression()

                        if self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] == "έως":
                            self.advance()
                            self.parse_expression()
                            self.parse_step()

                            if self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] == "επανάλαβε":
                                self.advance()
                                self.parse_sequence()                                

                                if self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] == "για_τέλος":
                                    self.advance()

                                else:
                                    self.error("Αναμενόταν το KEYWORD 'για_τέλος' στο τέλος της συνάρτησης")

                            else:
                                self.error("Αναμενόταν το KEYWORD 'επανάλαβε' μετά την step")

                        else:
                            self.error("Αναμενόταν το KEYWORD 'έως' μετά την expression")

                    else:
                        self.error("Αναμενόταν το σωστό IDENTIFIER")

                else:
                    self.error("Αναμενόταν το KEYWORD 'για' στην αρχή της συνάρτησης")
            
    def parse_step(self):
        if self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] == 'με_βήμα':
            self.advance()
            self.parse_exception()
                    
    def parse_print_stat(self):
        if self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] == 'γράψε':
            self.advance()
            result = self.parse_expression()
            self.ic.emit("out", result, None, None)
        
    def parse_input_stat(self):
        if self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] == 'διάβασε':
            self.advance()

            if self.current_token and self.current_token[0] == "IDENTIFIER":
                var_name = self.current_token[1]
                self.ic.emit("in", var_name, None, None)
                self.advance()

            else:
                self.error("Αναμενόταν το σωστό 'IDENTIFIER'")
                
    def parse_call_stat(self):
        if self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] == 'εκτέλεσε':
            self.advance()

            if self.current_token and self.current_token[0] == "IDENTIFIER":
                self.advance()
                self.parse_idtail()

            else:
                self.error("Αναμενόταν το σωστό 'IDENTIFIER'")
                
    def parse_idtail(self):
        if self.current_token and self.current_token[0] == "GROUPING_SYMBOLS" and self.current_token[1] == '(':
            self.parse_actualpars()
            
    def parse_actualpars(self):
        if self.current_token and self.current_token[0] == "GROUPING_SYMBOLS" and self.current_token[1] == '(':
            self.advance()
            self.parse_actualparlist()

            if self.current_token and self.curret_token[0] == "GROUPING_SYMBOLS" and self.current_token[1] == ')':
                self.advance()

            else:
                self.error("Αναμενόταν το GROUPING_SYMBOLS ')'")
                
    def parse_actualparlist(self):
        self.parse_actualparitem()
        while self.current_token and self.current_token == ("SEPARATOR", ","):  # ✅ Επιτρέπουμε πολλές μεταβλητές
            self.advance()
            self.parse_actualparitem()
            
    def parse_actualparitem(self):
        if self.current_token and self.current_token[0] == ("REFERENCE_PARAMETERS") and self.current_token[1] == "%":
            self.advance()

            if self.current_token and self.current_token[0] == ("IDENTIFIER"):
                self.advance()

            else:
                self.error("Αναμενόταν το σωστό 'IDENTIFIER'")

        else:
            self.parse_expression()
    
    def parse_condition(self):
        print("DEBUG: Ξεκινάει condition από:", self.current_token)

        if self.current_token and self.current_token[0] == "GROUPING_SYMBOLS" and self.current_token[1] == "[":
            print("DEBUG: Άνοιγμα σύνθετης συνθήκης '['")
            self.advance()

            true_list, false_list = self.parse_boolterm()

            while self.current_token and self.current_token == ("KEYWORD", "ή"):
                self.advance()
                t2, f2 = self.parse_boolterm()

                self.ic.backpatch(false_list, self.ic.nextquad())
                true_list = true_list + t2
                false_list = f2

            if self.current_token and self.current_token[0] == "GROUPING_SYMBOLS" and self.current_token[1] == "]":
                self.advance()
                return true_list, false_list
            
            else:
                self.error("Αναμενόταν ']' μετά από σύνθετη συνθήκη")

        else:
            print("DEBUG: Ξεκινάει απλή συνθήκη έξω από [ ]")
            left = self.parse_expression()

            if self.current_token and self.current_token[0] == "COMPARISON_OPERATOR":
                operator = self.current_token[1]
                print("DEBUG: Βρέθηκε τελεστής σύγκρισης:", operator)
                self.advance()
            
            else:
                self.error("Αναμενόταν τελεστής σύγκρισης")

            right = self.parse_expression()
            print("DEBUG: Condition parsed:", left, operator, right)

            return left, operator, right

    def parse_boolterm(self):
        print("DEBUG: Ξεκινάει boolterm")

        true_list, false_list = self.parse_boolfactor()

        while self.current_token and self.current_token == ("KEYWORD", "και"):
            print("DEBUG: Βρέθηκε 'και'")
            self.advance()
            t2, f2 = self.parse_boolfactor()

            self.ic.backpatch(true_list, self.ic.nextquad())
            true_list = t2
            false_list = false_list + f2

        return true_list, false_list
            
    def parse_boolfactor(self):
        if self.current_token and self.current_token == ("KEYWORD", "όχι"):
            print("DEBUG: Βρέθηκε 'όχι'")
            self.advance()

            if self.current_token and self.current_token == ("GROUPING_SYMBOLS", "["):
                print("DEBUG: Άνοιγμα μετά το 'όχι'")
                self.advance()
                true_list, false_list = self.parse_condition()

                if self.current_token and self.current_token == ("GROUPING_SYMBOLS", "]"):
                    print("DEBUG: Κλείσιμο μετά το 'όχι'")
                    self.advance()
                    return false_list, true_list
                
                else:
                    self.error("Αναμενόταν ']' μετά το 'όχι'")
            
            else:
                self.error("Αναμενόταν '[' μετά το 'όχι'")

        elif self.current_token and self.current_token == ("GROUPING_SYMBOLS", "["):
            print("DEBUG: Νέα εσωτερική σύνθετη συνθήκη '[' μέσα σε boolfactor")
            self.advance()
            true_list, false_list = self.parse_boolterm()
            
            while self.current_token and self.current_token == ("KEYWORD", "ή"):
                print("DEBUG: Βρέθηκε 'ή' σε nested boolfactor")
                self.advance()
                t2, f2 = self.parse_boolterm()

                self.ic.backpatch(false_list, self.ic.nextquad())
                true_list = true_list + t2
                false_list = f2

            if self.current_token and self.current_token == ("GROUPING_SYMBOLS", "]"):
                print("DEBUG: Κλείσιμο εσωτερικής σύνθετης συνθήκης ']'")
                self.advance()
                return true_list, false_list
            
            else:
                self.error("Αναμενόταν ']' μετά από nested σύνθετη συνθήκη")

        else:
            print("DEBUG: Ξεκινάει απλή συνθήκη μέσα σε boolfactor")
            left = self.parse_expression()
            
            if self.current_token and self.current_token[0] == "COMPARISON_OPERATOR":
                operator = self.current_token[1]
                print("DEBUG: Βρέθηκε τελεστής σύγκρισης:", operator)
                self.advance()
            
            else:
                self.error("Αναμενόταν τελεστής σύγκρισης")

            right = self.parse_expression()
            print(f"DEBUG: boolfactor condition parsed: {left} {operator} {right}")

            label_true = self.ic.new_label()
            label_false = self.ic.new_label()

            self.ic.emit(operator, left, right, label_true)
            self.ic.emit("jump", None, None, label_false)

            return [label_true], [label_false]

    def parse_expression(self):
        print("DEBUG: Ξεκινάει expression από:", self.current_token)        
        sign = self.parse_optional_sign()
        left = self.parse_term()

        if sign == '-':
            temp = self.ic.new_temp()
            self.symtab.insert(temp, "temp")

            self.ic.emit("-", '0', left, temp)
            left = temp

        elif sign == '+':
            pass 

        while self.current_token and self.current_token[0] == "ARITHMETIC_OPERATOR" and self.current_token[1] in ["+", "-"]:
            op = self.parse_add_oper()
            right = self.parse_term()
            temp = self.ic.new_temp()
            self.symtab.insert(temp, "temp")
            self.ic.emit(op, left, right, temp)
            left = temp
        return left
            
    def parse_term(self):
        left = self.parse_factor()
        while self.current_token and self.current_token[0] == "ARITHMETIC_OPERATOR" and self.current_token[1] in ["*", "/"]:
            op = self.parse_mul_oper()
            right = self.parse_factor()
            temp = self.ic.new_temp()
            self.symtab.insert(temp, "temp")

            self.ic.emit(op, left, right, temp)
            left = temp
        return left
        
    def parse_factor(self):
        sign = self.parse_optional_sign()

        if self.current_token[0] == "NUMBER":
            num = self.current_token[1]
            self.advance()

            if sign == '-':
                temp = self.ic.new_temp()
                self.symtab.insert(temp, "temp")
                self.ic.emit("-", '0', num, temp)
                return temp
            else:
                return num

        elif self.current_token[0] == "IDENTIFIER":
            func_or_var_name = self.current_token[1]
            self.advance()

            if self.current_token == ("GROUPING_SYMBOLS", "("):
                self.advance()
                arg = self.parse_expression()
                self.match("GROUPING_SYMBOLS", ")")

                temp = self.ic.new_temp()
                self.symtab.insert(temp, "temp")

                self.ic.emit("par", arg, None, "CV")
                self.ic.emit("par", temp, None, "RET")
                self.ic.emit("call", func_or_var_name, None, None)

                if sign == '-':
                    neg_temp = self.ic.new_temp()
                    self.symtab.insert(neg_temp, "temp")
                    self.ic.emit("-", '0', temp, neg_temp)
                    return neg_temp
                else:
                    return temp

            else:
                if sign == '-':
                    temp = self.ic.new_temp()
                    self.symtab.insert(temp, "temp")
                    self.ic.emit("-", '0', func_or_var_name, temp)
                    return temp
                else:
                    return func_or_var_name

        elif self.current_token == ("GROUPING_SYMBOLS", "("):
            self.advance()
            expr = self.parse_expression()
            self.match("GROUPING_SYMBOLS", ")")

            if sign == '-':
                temp = self.ic.new_temp()
                self.symtab.insert(temp, "temp")
                self.ic.emit("-", '0', expr, temp)
                return temp
            else:
                return expr

        else:
            self.error(f"Μη αναμενόμενο token: {self.current_token}")
            
    def parse_relational_oper(self):
        if self.current_token and self.current_token[0] == "COMPARISON_OPERATOR" and self.current_token[1] in ["=", "<=", ">=", "<>", "<", ">"]:
            op = self.current_token[1]
            self.advance()
            return op
        
        else:
            self.error(f"Αναμενόταν τελεστής σύγκρισης, βρέθηκε: {self.current_token}")
            
    def parse_add_oper(self):
        if self.current_token and self.current_token[0] == "ARITHMETIC_OPERATOR" and self.current_token[1] in ["+", "-"]:
            op = self.current_token[1]
            self.advance()
            return op
        
        else:
            self.error(f"Αναμενόταν '+' ή '-' αλλά βρέθηκε: {self.current_token}")

    def parse_mul_oper(self):
        if self.current_token and self.current_token[0] == "ARITHMETIC_OPERATOR" and self.current_token[1] in ["*", "/"]:
            op = self.current_token[1]
            self.advance()
            return op
        
        else:
            self.error(f"Αναμενόταν '*' ή '/' αλλά βρέθηκε: {self.current_token}")

    def parse_optional_sign(self):
        if self.current_token and self.current_token[0] == "ARITHMETIC_OPERATOR":
            
            if self.current_token[1] == "+":
                self.advance()
                return "+"
            
            elif self.current_token[1] == "-":
                self.advance()
                return "-"
        return None
    
    def parse_logic_expr(self):
        left = self.parse_comparison_expr()
        while self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] in ["και", "ή"]:
            op = self.current_token
            self.advance()
            right = self.parse_comparison_expr()
            left = ("BINARY_OP", op[1], left, right)
        return left

    def parse_comparison_expr(self):
        left = self.parse_add_sub_expr()
        if self.current_token and self.current_token[0] == "COMPARISON_OPERATOR":
            op = self.current_token
            self.advance()
            right = self.parse_add_sub_expr()
            return ("BINARY_OP", op[1], left, right)
        return left

    def parse_add_sub_expr(self):
        left = self.parse_mul_div_expr()
        while self.current_token and self.current_token[0] == "ARITHMETIC_OPERATOR" and self.current_token[1] in ["+", "-"]:
            op = self.current_token
            self.advance()
            right = self.parse_mul_div_expr()
            left = ("BINARY_OP", op[1], left, right)
        return left

    def parse_mul_div_expr(self):
        left = self.parse_unary_expr()
        while self.current_token and self.current_token[0] == "ARITHMETIC_OPERATOR" and self.current_token[1] in ["*", "/"]:
            op = self.current_token
            self.advance()
            right = self.parse_unary_expr()
            left = ("BINARY_OP", op[1], left, right)
        return left

    def parse_unary_expr(self):
        if self.current_token and self.current_token[0] == "ARITHMETIC_OPERATOR" and self.current_token[1] in ["+", "-"]:
            op = self.current_token
            self.advance()
            expr = self.parse_not_expr()
            return ("UNARY_OP", op[1], expr)
        return self.parse_not_expr()

    def parse_not_expr(self):
        if self.current_token and self.current_token[0] == "KEYWORD" and self.current_token[1] == "όχι":
            op = self.current_token
            self.advance()
            expr = self.parse_comparison_expr()
            return ("UNARY_OP", "όχι", expr)
        return self.parse_primary()

    def parse_primary(self):
        if self.current_token[0] == "NUMBER":
            num = self.current_token
            self.advance()
            return ("NUMBER", num[1])
        
        elif self.current_token[0] == "IDENTIFIER":
            var = self.current_token
            self.advance()
            return ("IDENTIFIER", var[1])
        
        elif self.current_token[0] == "GROUPING_SYMBOL" and self.current_token[1] == "(":
            self.advance()
            expr = self.parse_logic_expr()
            
            if self.current_token[0] == "GROUPING_SYMBOL" and self.current_token[1] == ")":
                self.advance()
                return expr
            
            else:
                self.error("Αναμενόταν ')'")
        
        else:
            self.error("Μη έγκυρη πρωτεύουσα έκφραση")
    
    def parse(self):
        self.parse_program()
        print("Το πρόγραμμα είναι συντακτικά σωστό!")
        
        with open("output.int", "w", encoding="utf-8") as f:
            f.write(str(self.ic))
                 
        write_to_c("output.int", "output.c")
        print("Ο ενδιάμεσος κώδικας μετατράπηκε σε C στο αρχείο 'output.c'")
 
parser = Parser(tokens)
parser.parse()
parser.ic.generate_final_code(parser.symtab)
print("Τελικός κώδικας γράφτηκε στο output.asm")



