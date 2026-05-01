# PejicLang Core

PejicLang (.pej) is a declarative multi-target orchestration language.

## Purpose
Define and control distributed systems across:
- backend (Go)
- PejicX (.pej)
- frontend (TypeScript)
- database (SQL)
- system layer (C/C++)
- automation (Bash / SH / CMD)

## 📊 Compilation Pipeline

The PejicLang compilation process follows a multi-stage pipeline:

```
┌─────────────────────┐
│  Source Code (.pej) │
│  let x = 42;        │
└──────────┬──────────┘
           │
           ▼
    ┌─────────────┐
    │   LEXER     │ (lexer.py)
    │ Tokenization│
    └──────┬──────┘
           │
      Tokens: [LET, ID(x), ASSIGN, INT(42), SEMI]
           │
           ▼
    ┌──────────────┐
    │   PARSER     │ (parser.py)
    │ Syntax Parse │
    └──────┬───────┘
           │
      AST: VariableDeclaration(x, IntLiteral(42))
           │
           ▼
    ┌──────────────┐
    │  ANALYZER    │
    │ Type Check & │
    │  Validation  │
    └──────┬───────┘
           │
      Validated AST
           │
           ▼
    ┌──────────────┐
    │   CODEGEN    │
    │  Code Gen    │
    └──────┬───────┘
           │
      Target: Go/TS/SQL/C++/Bash
           │
           ▼
    ┌──────────────┐
    │  EXECUTION   │
    │  PejicX Runtime
    └──────────────┘
```

## 🏗️ System Architecture

PejicLang orchestrates across a multi-layered distributed system:

```
╔═════════════════════════════════════════════════════════════╗
║              ORCHESTRATION LAYER (PejicLang)                ║
╠═════════════════════════════════════════════════════════════╣
║                                                              ║
║  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     ║
║  │  Frontend    │  │   Backend    │  │   Database   │     ║
║  │ (TypeScript) │  │     (Go)     │  │    (SQL)     │     ║
║  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     ║
║         │                  │                  │              ║
║         └──────────────────┼──────────────────┘              ║
║                            │                                ║
╠════════════════════════════════════════════════════════════╣
║                v v v   PEJICX RUNTIME   v v v               ║
║     Intelligent Execution & Orchestration Engine            ║
╠════════════════════════════════════════════════════════════╣
║                                                              ║
║  ┌──────────────┐                    ┌──────────────┐      ║
║  │ System Layer │                    │  Automation  │      ║
║  │   (C/C++)    │                    │ (Bash/SH/CMD)│      ║
║  └──────┬───────┘                    └──────┬───────┘      ║
║         │                                    │               ║
║         └────────────────┬───────────────────┘               ║
║                          │                                   ║
║              ┌───────────▼───────────┐                      ║
║              │  Resource Management   │                     ║
║              │  Event Processing      │                     ║
║              │  State Coordination    │                     ║
║              └───────────────────────┘                      ║
║                                                              ║
╚═════════════════════════════════════════════════════════════╝
```

**Layer Responsibilities:**
- **Orchestration**: Define system structure and behavior
- **PejicX Runtime**: Intelligent coordination, scheduling, monitoring
- **Target Platforms**: Execute specialized code for each environment

## 📝 Lexer/Parser Documentation

### Lexer (lexer.py)

The **Lexer** performs lexical analysis - converting raw source code into a stream of tokens.

**Input:** Raw PejicLang source code string

**Tokenization Process:**
1. Pattern matching against predefined regex patterns
2. Whitespace and comment removal
3. Keyword vs identifier classification
4. Operator and delimiter recognition
5. Number and string literal parsing

**Token Types Produced:**
- `KEYWORD`: Reserved words (fn, let, if, etc.)
- `IDENTIFIER`: Variable/function names
- `INTEGER`: Numeric literals (e.g., 42, -10)
- `FLOAT`: Decimal numbers (e.g., 3.14, -2.5)
- `STRING`: String literals with escape sequences
- `OPERATOR`: Arithmetic/logical operators
- `DELIMITER`: Brackets, parentheses, semicolons

**Example:**
```python
from lexer import Lexer

code = "let x: Int = 42;"
lexer = Lexer(code)
tokens = lexer.tokenize()

# Output:
# ('KEYWORD', 'let')
# ('IDENTIFIER', 'x')
# ('DELIMITER', ':')
# ('IDENTIFIER', 'Int')
# ('OPERATOR', '=')
# ('INTEGER', '42')
# ('DELIMITER', ';')
```

**Supported Keywords:**
fn, let, const, if, else, while, for, return, break, continue, true, false, null, struct, enum, import, export, as, match

**Supported Operators:**
+, -, *, /, %, ==, !=, <, >, <=, >=, &&, ||, !, =, +=, -=, *=, /=, %=

### Parser (parser.py)

The **Parser** performs syntax analysis - converting a token stream into an Abstract Syntax Tree (AST).

**Input:** Token sequence from Lexer

**Parsing Strategy:** Recursive descent parser with operator precedence climbing

**AST Node Types:**
- **Declarations**: Variable, Function, Struct, Enum, Import, Export
- **Statements**: If, While, For, Match, Return, Break, Continue, Block
- **Expressions**: Binary ops, Unary ops, Calls, Member access, Literals
- **Types**: Type annotations, Generics

**Operator Precedence (Low to High):**
1. Assignment (=, +=, -=, etc.)
2. Logical OR (||)
3. Logical AND (&&)
4. Equality (==, !=)
5. Relational (<, >, <=, >=)
6. Additive (+, -)
7. Multiplicative (*, /, %)
8. Unary (!, -, +)
9. Postfix (call, member access, indexing)

**Example:**
```python
from lexer import Lexer
from parser import Parser

code = """
fn add(a: Int, b: Int) -> Int {
    return a + b;
}
"""

lexer = Lexer(code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

# AST structure:
# Program(
#   statements=[
#     FunctionDeclaration(
#       name='add',
#       parameters=[Parameter(name='a', ...), Parameter(name='b', ...)],
#       return_type=TypeAnnotation(type_name='Int'),
#       body=Block(statements=[...])
#     )
#   ]
# )
```

### Integration Flow

```
Source Code
    ↓
[Lexer.tokenize()]  → Produces token stream
    ↓
[Parser.parse()]    → Produces AST
    ↓
[Analyzer]          → Performs type checking & validation (future)
    ↓
[Codegen]           → Generates target platform code (future)
```

## Files

- **language.pej** → Language specification and formal grammar
- **lexer.py** → Tokenization and lexical analysis engine
- **parser.py** → Syntax analysis and AST generation

## Core Concepts

### Language Design Philosophy
PejicLang combines:
- **Declarative syntax** for clear intent
- **Multi-target compilation** for platform flexibility
- **Strong type system** for safety and optimization
- **Orchestration focus** for distributed systems

### Key Principles
1. **Explicitness**: Clear, unambiguous code structure
2. **Composability**: Modular system design
3. **Determinism**: Predictable execution
4. **Scalability**: Handles large distributed systems

## 📋 Language Features Overview

### Core Language Constructs

**Variable Declarations:**
```pejic
let x: Int = 42;
const name: String = "PejicLang";
let data = 3.14;  // Type inference supported
```

**Function Definitions:**
```pejic
fn add(a: Int, b: Int) -> Int {
    return a + b;
}

fn greet(name: String) {
    print("Hello, " + name);
}
```

**Control Flow:**
```pejic
// Conditional
if x > 0 {
    return "positive";
} else if x < 0 {
    return "negative";
} else {
    return "zero";
}

// Loops
while count < 10 {
    count += 1;
}

for (let i = 0; i < 5; i += 1) {
    print(i);
}

// Pattern matching
match status {
    "active" => print("Running"),
    "inactive" => print("Stopped"),
}
```

**Type Definitions:**
```pejic
struct Point {
    x: Int,
    y: Int
};

enum Color {
    Red = 0,
    Green = 1,
    Blue = 2
};
```

**Module System:**
```pejic
import "core/utils" as utils;
export fn calculate() { ... }
```

### Type System

| Category | Types | Examples |
|----------|-------|----------|
| **Primitive** | Int, Float, String, Boolean | `42`, `3.14`, `"text"`, `true` |
| **Collection** | Array, Struct | `[1, 2, 3]`, `Point { x: 5, y: 10 }` |
| **Enum** | User-defined | `Color::Red`, `Status::Active` |
| **Generic** | Type parameters | `List<Int>`, `Map<String, Value>` |

## 🚀 Quick Start Code Examples

### Basic Setup
```python
from lexer import Lexer
from parser import Parser

# Read your PejicLang code
with open("program.pej", "r") as f:
    code = f.read()
```

### Step 1: Tokenization (Lexing)
```python
lexer = Lexer(code)
tokens = lexer.tokenize()

# Print tokens
for token_type, value in tokens:
    print(f"{token_type}: {value}")
```

### Step 2: Parsing to AST
```python
parser = Parser(tokens)
ast = parser.parse()

# Inspect AST structure
print(ast)
print(f"Number of statements: {len(ast.statements)}")
```

### Complete Example
```python
from lexer import Lexer
from parser import Parser

code = """
fn fibonacci(n: Int) -> Int {
    if n <= 1 {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

let result: Int = fibonacci(10);
"""

# Lex and parse
lexer = Lexer(code)
tokens = lexer.tokenize()
print(f"✓ Tokenized: {len(tokens)} tokens")

parser = Parser(tokens)
ast = parser.parse()
print(f"✓ Parsed: {len(ast.statements)} statements")
print("\nAST:", ast)
```

### Error Handling
```python
from lexer import Lexer
from parser import Parser

code = "let x = 42"  # Missing semicolon

try:
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
except SyntaxError as e:
    print(f"Parse Error: {e}")
except ValueError as e:
    print(f"Lexer Error: {e}")
```

## File Structure

- **language.pej** → Language specification and formal grammar
- **lexer.py** → Tokenization and lexical analysis engine
- **parser.py** → Syntax analysis and AST generation

## PejicX Runtime Layer

PejicX is the intelligent execution/runtime coordinator of the system.
- Replaces traditional "AI" terminology with domain-specific orchestration
- Manages cross-platform execution (Go, TypeScript, SQL, C++, Bash)
- Coordinates distributed system components
- Handles state management and event processing

## Project Status

**Current Version:** stable v1.0.0

**Completed:**
- ✅ Lexical analyzer (lexer.py)
- ✅ Syntax parser (parser.py)
- ✅ AST node definitions
- ✅ Core language specification

**In Development:**
- 🔄 Semantic analyzer (type checking)
- 🔄 Code generation backends
- 🔄 Runtime optimizer

## 🔀 Pull Request Guidelines

### Before Creating a PR

1. **Branch Naming Convention:**
   - `feature/*` - New features
   - `bugfix/*` - Bug fixes
   - `docs/*` - Documentation updates
   - `refactor/*` - Code refactoring
   - `enhance/*` - Enhancements

   Example: `feature/add-analyzer` or `docs/update-readme`

2. **Commit Standards:**
   - Use clear, descriptive commit messages
   - Reference issue numbers when applicable
   - Use present tense: "Add" not "Added"

3. **Code Quality:**
   - Follow PEP 8 for Python code
   - Test your changes locally
   - Ensure no syntax errors

### PR Merge Template

```markdown
## Description
Brief description of what this PR accomplishes.

## Type of Change
- [ ] New feature (non-breaking)
- [ ] Bug fix (non-breaking)
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement

## Related Issue
Closes #issue_number

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Tested locally
- [ ] No errors or warnings
- [ ] Verified compatibility with lexer.py / parser.py

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No breaking changes
```

### PR Review & Merge Process

1. **Create Pull Request:**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create PR on GitHub

2. **Expectations:**
   - ✅ Automated tests pass
   - ✅ Code review approval required
   - ✅ No merge conflicts

3. **Merge Strategy:**
   - Use "Squash and merge" for feature branches
   - Use "Create a merge commit" for major releases
   - Delete branch after merge

### Example PR Creation

```bash
# Create and switch to feature branch
git checkout -b feature/add-error-messages

# Make changes
# ... edit files ...

# Commit changes
git add .
git commit -m "Add comprehensive error messages

- Implement detailed error reporting
- Add error codes for debugging
- Include error recovery suggestions"

# Push to remote
git push origin feature/add-error-messages

# Create PR with descriptive title and body
# On GitHub: Compare & pull request
```

### Continuous Integration

All PRs must pass:
- ✅ Python syntax check
- ✅ Code style validation
- ✅ Parser functionality tests
- ✅ Integration tests with lexer

### Contact & Discussion

For questions about PRs or contributions:
- Open an issue with label `question`
- Join discussions in PR comments
- Check existing PRs for similar work
