import re

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.keywords = set([
            "fn", "let", "const", "if", "else", "while", "for", "return",
            "break", "continue", "true", "false", "null", "struct", "enum",
            "import", "export", "as", "match"
        ])
        self.operators = set([
            "+", "-", "*", "/", "%", "==", "!=", "<", ">", "<=", ">=",
            "&&", "||", "!", "=", "+=", "-=", "*=", "/=", "%="
        ])
        self.delimiters = set([
            "(", ")", "{", "}", "[", "]", ";", ",", ".", ":", "::"
        ])
        self.patterns = [
            ('WHITESPACE', r'\s+'),
            ('COMMENT', r'//[^\n]*|/\*[\s\S]*?\*/'),
            ('FLOAT', r'-?\d+\.\d+'),
            ('INTEGER', r'-?\d+'),
            ('STRING', r'"(?:\\.|[^"\\])*"'),
            ('IDENTIFIER', r'[A-Za-z_][A-Za-z0-9_]*'),
        ]

    def tokenize(self):
        i = 0
        while i < len(self.code):
            matched = False
            for token_type, pattern in self.patterns:
                regex = re.compile(pattern)
                match = regex.match(self.code, i)
                if match:
                    value = match.group(0)
                    if token_type == 'IDENTIFIER':
                        if value in self.keywords:
                            self.tokens.append(('KEYWORD', value))
                        else:
                            self.tokens.append(('IDENTIFIER', value))
                    elif token_type in ['WHITESPACE', 'COMMENT']:
                        # Skip whitespace and comments
                        pass
                    else:
                        self.tokens.append((token_type, value))
                    i = match.end()
                    matched = True
                    break
            if not matched:
                # Check for operators and delimiters
                # Sort by length descending to match longer first
                all_symbols = sorted(self.operators | self.delimiters, key=len, reverse=True)
                for sym in all_symbols:
                    if self.code.startswith(sym, i):
                        if sym in self.operators:
                            self.tokens.append(('OPERATOR', sym))
                        else:
                            self.tokens.append(('DELIMITER', sym))
                        i += len(sym)
                        matched = True
                        break
            if not matched:
                # Unknown character
                raise ValueError(f"Unexpected character at position {i}: '{self.code[i]}'")
        return self.tokens

# Example usage
if __name__ == "__main__":
    code = """
    fn main() {
        let x: Int = 42;
        let y = 3.14;
        if x > 0 {
            return "positive";
        }
    }
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)
