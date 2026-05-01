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

## Core Components

### Compilation Pipeline
```
Source Code (.pej)
        ↓
    [Lexer] → Tokens
        ↓
    [Parser] → AST
        ↓
    [Analyzer] → Validated AST
        ↓
    [Codegen] → Target Code
        ↓
    [Execution]
```

### Architecture Diagram
The system orchestrates across multiple layers:

```
┌─────────────────────────────────────────────────────┐
│           PejicLang Orchestration Layer              │
├─────────────────────────────────────────────────────┤
│  Frontend (TS) │ Backend (Go) │ Database (SQL)      │
├─────────────────────────────────────────────────────┤
│         PejicX Runtime Layer (Intelligent)           │
├─────────────────────────────────────────────────────┤
│ System Layer (C/C++) │ Automation (Bash/SH/CMD)     │
└─────────────────────────────────────────────────────┘
```

### Language Processing

```
=== LEXER (lexer.py) ===
Input: Raw source code
Operations: 
  • Tokenization
  • Keyword recognition
  • Operator/delimiter identification
  • Comment/whitespace handling
Output: Token stream

=== PARSER (parser.py) ===
Input: Token stream
Operations:
  • Syntax analysis
  • AST construction
  • Operator precedence
  • Error detection
Output: Abstract Syntax Tree (AST)
```

## Files

- **language.pej** → Language specification and grammar definition
- **lexer.py** → Tokenization and lexical analysis
- **parser.py** → Syntax analysis and AST generation

## Core Concepts

### Language Features
- Variable declarations (let / const)
- Function definitions with type annotations
- Control flow (if/else, while, for, match)
- Struct and Enum types
- Import/Export declarations
- Pattern matching

### Type System
- Primitive types: Int, Float, String, Boolean
- Composite types: Struct, Enum, Array
- Type annotations with optional generics

## PejicX Layer
PejicX is the intelligent execution/runtime layer of the system.
It replaces traditional AI terminology and serves the same functional role.

## Status
stable v1.0.0

## Quick Start

### Lexing
```python
from lexer import Lexer

code = "fn main() { let x: Int = 42; }"
lexer = Lexer(code)
tokens = lexer.tokenize()
```

### Parsing
```python
from lexer import Lexer
from parser import Parser

lexer = Lexer(code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()
```
