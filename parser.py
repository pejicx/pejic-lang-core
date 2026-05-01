from dataclasses import dataclass
from typing import List, Optional, Union, Any
from enum import Enum


class TokenType(Enum):
    """Token types matching lexer output"""
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    OPERATOR = "OPERATOR"
    DELIMITER = "DELIMITER"
    EOF = "EOF"


@dataclass
class Token:
    """Represents a single token"""
    type: TokenType
    value: str
    position: int = 0


# AST Node Classes
class ASTNode:
    """Base class for all AST nodes"""
    pass


@dataclass
class Program(ASTNode):
    statements: List[ASTNode]


@dataclass
class VariableDeclaration(ASTNode):
    kind: str  # "let" or "const"
    name: str
    type_annotation: Optional['TypeAnnotation'] = None
    value: Optional['Expression'] = None


@dataclass
class FunctionDeclaration(ASTNode):
    name: str
    parameters: List['Parameter']
    return_type: Optional['TypeAnnotation'] = None
    body: Optional['Block'] = None


@dataclass
class Parameter(ASTNode):
    name: str
    type_annotation: Optional['TypeAnnotation'] = None


@dataclass
class TypeAnnotation(ASTNode):
    type_name: str
    generics: List['TypeAnnotation'] = None

    def __post_init__(self):
        if self.generics is None:
            self.generics = []


@dataclass
class StructDeclaration(ASTNode):
    name: str
    fields: List['Field']


@dataclass
class Field(ASTNode):
    name: str
    type_annotation: 'TypeAnnotation'


@dataclass
class EnumDeclaration(ASTNode):
    name: str
    members: List['EnumMember']


@dataclass
class EnumMember(ASTNode):
    name: str
    value: Optional[int] = None


@dataclass
class ImportDeclaration(ASTNode):
    module: str
    alias: Optional[str] = None


@dataclass
class ExportDeclaration(ASTNode):
    declaration: ASTNode


@dataclass
class Block(ASTNode):
    statements: List[ASTNode]


@dataclass
class IfStatement(ASTNode):
    condition: 'Expression'
    then_branch: ASTNode
    else_branch: Optional[ASTNode] = None


@dataclass
class WhileStatement(ASTNode):
    condition: 'Expression'
    body: ASTNode


@dataclass
class ForStatement(ASTNode):
    init: Optional[ASTNode]
    condition: Optional['Expression']
    update: Optional['Expression']
    body: ASTNode


@dataclass
class ReturnStatement(ASTNode):
    value: Optional['Expression'] = None


@dataclass
class BreakStatement(ASTNode):
    pass


@dataclass
class ContinueStatement(ASTNode):
    pass


@dataclass
class MatchStatement(ASTNode):
    expression: 'Expression'
    cases: List['MatchCase']


@dataclass
class MatchCase(ASTNode):
    pattern: 'Expression'
    body: ASTNode


@dataclass
class ExpressionStatement(ASTNode):
    expression: 'Expression'


# Expression Classes
class Expression(ASTNode):
    """Base class for expressions"""
    pass


@dataclass
class BinaryOp(Expression):
    left: Expression
    operator: str
    right: Expression


@dataclass
class UnaryOp(Expression):
    operator: str
    operand: Expression


@dataclass
class CallExpression(Expression):
    callee: Expression
    arguments: List[Expression]


@dataclass
class MemberAccess(Expression):
    object: Expression
    member: str


@dataclass
class IndexAccess(Expression):
    object: Expression
    index: Expression


@dataclass
class Literal(Expression):
    value: Any
    type: str  # "integer", "float", "string", "boolean", "null"


@dataclass
class Identifier(Expression):
    name: str


@dataclass
class ArrayLiteral(Expression):
    elements: List[Expression]


@dataclass
class StructLiteral(Expression):
    name: str
    fields: dict  # field_name -> Expression


@dataclass
class AssignmentExpression(Expression):
    target: Expression
    operator: str  # "=", "+=", "-=", etc.
    value: Expression


class Parser:
    """Recursive descent parser for PejicLang"""

    def __init__(self, tokens: List[tuple]):
        """
        Initialize parser with tokens from lexer.
        Tokens should be tuples of (token_type, value)
        """
        self.tokens = self._convert_tokens(tokens)
        self.current = 0

    def _convert_tokens(self, tokens: List[tuple]) -> List[Token]:
        """Convert lexer output tuples to Token objects"""
        converted = []
        for token_type, value in tokens:
            # Map string token types to TokenType enum
            try:
                type_enum = TokenType[token_type]
            except KeyError:
                type_enum = TokenType.IDENTIFIER
            converted.append(Token(type=type_enum, value=value))
        converted.append(Token(type=TokenType.EOF, value=""))
        return converted

    def parse(self) -> Program:
        """Parse tokens into an AST"""
        statements = []
        while not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements=statements)

    # Token manipulation methods
    def _current_token(self) -> Token:
        """Get current token"""
        return self.tokens[self.current]

    def _peek_token(self, offset: int = 0) -> Token:
        """Peek at token ahead"""
        idx = self.current + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]

    def _is_at_end(self) -> bool:
        """Check if we've reached end of tokens"""
        return self._current_token().type == TokenType.EOF

    def _advance(self) -> Token:
        """Consume and return current token"""
        token = self._current_token()
        if not self._is_at_end():
            self.current += 1
        return token

    def _match(self, *values: str) -> bool:
        """Check if current token matches any of the given values"""
        token = self._current_token()
        return token.value in values

    def _consume(self, value: str, message: str = "") -> Token:
        """Consume a token with expected value"""
        if self._current_token().value == value:
            return self._advance()
        raise SyntaxError(f"Expected '{value}' but got '{self._current_token().value}'. {message}")

    # Parsing methods
    def _parse_statement(self) -> Optional[ASTNode]:
        """Parse a statement"""
        token = self._current_token()

        if self._match("let", "const"):
            return self._parse_variable_declaration()
        elif self._match("fn"):
            return self._parse_function_declaration()
        elif self._match("struct"):
            return self._parse_struct_declaration()
        elif self._match("enum"):
            return self._parse_enum_declaration()
        elif self._match("import"):
            return self._parse_import_declaration()
        elif self._match("export"):
            return self._parse_export_declaration()
        elif self._match("if"):
            return self._parse_if_statement()
        elif self._match("while"):
            return self._parse_while_statement()
        elif self._match("for"):
            return self._parse_for_statement()
        elif self._match("return"):
            return self._parse_return_statement()
        elif self._match("break"):
            self._advance()
            self._consume(";", "Expected ';' after break")
            return BreakStatement()
        elif self._match("continue"):
            self._advance()
            self._consume(";", "Expected ';' after continue")
            return ContinueStatement()
        elif self._match("match"):
            return self._parse_match_statement()
        elif self._match("{"):
            return self._parse_block()
        else:
            return self._parse_expression_statement()

    def _parse_variable_declaration(self) -> VariableDeclaration:
        """Parse let/const declaration"""
        kind = self._advance().value  # "let" or "const"
        name = self._consume_identifier()

        type_annotation = None
        if self._match(":"):
            self._advance()
            type_annotation = self._parse_type_annotation()

        value = None
        if self._match("="):
            self._advance()
            value = self._parse_expression()

        self._consume(";", "Expected ';' after variable declaration")
        return VariableDeclaration(
            kind=kind,
            name=name,
            type_annotation=type_annotation,
            value=value
        )

    def _parse_function_declaration(self) -> FunctionDeclaration:
        """Parse function declaration"""
        self._consume("fn")
        name = self._consume_identifier()

        self._consume("(")
        parameters = self._parse_parameter_list()
        self._consume(")")

        return_type = None
        if self._match("->"):
            self._advance()
            return_type = self._parse_type_annotation()

        body = self._parse_block()

        return FunctionDeclaration(
            name=name,
            parameters=parameters,
            return_type=return_type,
            body=body
        )

    def _parse_parameter_list(self) -> List[Parameter]:
        """Parse function parameter list"""
        parameters = []
        if not self._match(")"):
            while True:
                name = self._consume_identifier()
                type_annotation = None
                if self._match(":"):
                    self._advance()
                    type_annotation = self._parse_type_annotation()
                parameters.append(Parameter(name=name, type_annotation=type_annotation))

                if not self._match(","):
                    break
                self._advance()
        return parameters

    def _parse_type_annotation(self) -> TypeAnnotation:
        """Parse type annotation"""
        type_name = self._consume_identifier()
        generics = []
        # Could be extended to support generics like List<Int>
        return TypeAnnotation(type_name=type_name, generics=generics)

    def _parse_struct_declaration(self) -> StructDeclaration:
        """Parse struct declaration"""
        self._consume("struct")
        name = self._consume_identifier()
        self._consume("{")

        fields = []
        if not self._match("}"):
            while True:
                field_name = self._consume_identifier()
                self._consume(":")
                type_annotation = self._parse_type_annotation()
                fields.append(Field(name=field_name, type_annotation=type_annotation))

                if not self._match(","):
                    break
                self._advance()

        self._consume("}")
        self._consume(";")

        return StructDeclaration(name=name, fields=fields)

    def _parse_enum_declaration(self) -> EnumDeclaration:
        """Parse enum declaration"""
        self._consume("enum")
        name = self._consume_identifier()
        self._consume("{")

        members = []
        if not self._match("}"):
            while True:
                member_name = self._consume_identifier()
                value = None
                if self._match("="):
                    self._advance()
                    value = int(self._advance().value)
                members.append(EnumMember(name=member_name, value=value))

                if not self._match(","):
                    break
                self._advance()

        self._consume("}")
        self._consume(";")

        return EnumDeclaration(name=name, members=members)

    def _parse_import_declaration(self) -> ImportDeclaration:
        """Parse import declaration"""
        self._consume("import")
        module = self._consume_string()
        alias = None
        if self._match("as"):
            self._advance()
            alias = self._consume_identifier()
        self._consume(";")
        return ImportDeclaration(module=module, alias=alias)

    def _parse_export_declaration(self) -> ExportDeclaration:
        """Parse export declaration"""
        self._consume("export")
        declaration = self._parse_statement()
        return ExportDeclaration(declaration=declaration)

    def _parse_if_statement(self) -> IfStatement:
        """Parse if/else statement"""
        self._consume("if")
        self._consume("(")
        condition = self._parse_expression()
        self._consume(")")

        then_branch = self._parse_statement()
        else_branch = None

        if self._match("else"):
            self._advance()
            else_branch = self._parse_statement()

        return IfStatement(
            condition=condition,
            then_branch=then_branch,
            else_branch=else_branch
        )

    def _parse_while_statement(self) -> WhileStatement:
        """Parse while statement"""
        self._consume("while")
        self._consume("(")
        condition = self._parse_expression()
        self._consume(")")
        body = self._parse_statement()
        return WhileStatement(condition=condition, body=body)

    def _parse_for_statement(self) -> ForStatement:
        """Parse for statement"""
        self._consume("for")
        self._consume("(")

        init = None
        if not self._match(";"):
            if self._match("let", "const"):
                init = self._parse_variable_declaration()
                # Remove the semicolon requirement from var decl for for loop
                if init.value is not None:
                    pass  # Already consumed
            else:
                init = self._parse_expression()
                self._consume(";")
        else:
            self._advance()

        condition = None
        if not self._match(";"):
            condition = self._parse_expression()
        self._consume(";")

        update = None
        if not self._match(")"):
            update = self._parse_expression()
        self._consume(")")

        body = self._parse_statement()
        return ForStatement(init=init, condition=condition, update=update, body=body)

    def _parse_return_statement(self) -> ReturnStatement:
        """Parse return statement"""
        self._consume("return")
        value = None
        if not self._match(";"):
            value = self._parse_expression()
        self._consume(";")
        return ReturnStatement(value=value)

    def _parse_match_statement(self) -> MatchStatement:
        """Parse match statement"""
        self._consume("match")
        expression = self._parse_expression()
        self._consume("{")

        cases = []
        while not self._match("}"):
            pattern = self._parse_expression()
            self._consume("=>")
            body = self._parse_statement()
            cases.append(MatchCase(pattern=pattern, body=body))

        self._consume("}")
        return MatchStatement(expression=expression, cases=cases)

    def _parse_block(self) -> Block:
        """Parse block of statements"""
        self._consume("{")
        statements = []
        while not self._match("}"):
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        self._consume("}")
        return Block(statements=statements)

    def _parse_expression_statement(self) -> ExpressionStatement:
        """Parse expression statement"""
        expr = self._parse_expression()
        self._consume(";")
        return ExpressionStatement(expression=expr)

    def _parse_expression(self) -> Expression:
        """Parse expression (handles assignment)"""
        return self._parse_assignment()

    def _parse_assignment(self) -> Expression:
        """Parse assignment expression"""
        expr = self._parse_logical_or()

        if self._match("=", "+=", "-=", "*=", "/=", "%="):
            operator = self._advance().value
            value = self._parse_assignment()
            return AssignmentExpression(target=expr, operator=operator, value=value)

        return expr

    def _parse_logical_or(self) -> Expression:
        """Parse logical OR expression"""
        expr = self._parse_logical_and()

        while self._match("||"):
            operator = self._advance().value
            right = self._parse_logical_and()
            expr = BinaryOp(left=expr, operator=operator, right=right)

        return expr

    def _parse_logical_and(self) -> Expression:
        """Parse logical AND expression"""
        expr = self._parse_equality()

        while self._match("&&"):
            operator = self._advance().value
            right = self._parse_equality()
            expr = BinaryOp(left=expr, operator=operator, right=right)

        return expr

    def _parse_equality(self) -> Expression:
        """Parse equality expression"""
        expr = self._parse_relational()

        while self._match("==", "!="):
            operator = self._advance().value
            right = self._parse_relational()
            expr = BinaryOp(left=expr, operator=operator, right=right)

        return expr

    def _parse_relational(self) -> Expression:
        """Parse relational expression"""
        expr = self._parse_additive()

        while self._match("<", ">", "<=", ">="):
            operator = self._advance().value
            right = self._parse_additive()
            expr = BinaryOp(left=expr, operator=operator, right=right)

        return expr

    def _parse_additive(self) -> Expression:
        """Parse additive expression"""
        expr = self._parse_multiplicative()

        while self._match("+", "-"):
            operator = self._advance().value
            right = self._parse_multiplicative()
            expr = BinaryOp(left=expr, operator=operator, right=right)

        return expr

    def _parse_multiplicative(self) -> Expression:
        """Parse multiplicative expression"""
        expr = self._parse_unary()

        while self._match("*", "/", "%"):
            operator = self._advance().value
            right = self._parse_unary()
            expr = BinaryOp(left=expr, operator=operator, right=right)

        return expr

    def _parse_unary(self) -> Expression:
        """Parse unary expression"""
        if self._match("!", "-", "+"):
            operator = self._advance().value
            expr = self._parse_unary()
            return UnaryOp(operator=operator, operand=expr)

        return self._parse_postfix()

    def _parse_postfix(self) -> Expression:
        """Parse postfix expressions (call, member access, index)"""
        expr = self._parse_primary()

        while True:
            if self._match("("):
                self._advance()
                arguments = []
                if not self._match(")"):
                    while True:
                        arguments.append(self._parse_expression())
                        if not self._match(","):
                            break
                        self._advance()
                self._consume(")")
                expr = CallExpression(callee=expr, arguments=arguments)
            elif self._match("."):
                self._advance()
                member = self._consume_identifier()
                expr = MemberAccess(object=expr, member=member)
            elif self._match("["):
                self._advance()
                index = self._parse_expression()
                self._consume("]")
                expr = IndexAccess(object=expr, index=index)
            else:
                break

        return expr

    def _parse_primary(self) -> Expression:
        """Parse primary expression"""
        token = self._current_token()

        # Literals
        if token.type == TokenType.INTEGER:
            self._advance()
            return Literal(value=int(token.value), type="integer")

        elif token.type == TokenType.FLOAT:
            self._advance()
            return Literal(value=float(token.value), type="float")

        elif token.type == TokenType.STRING:
            self._advance()
            # Remove quotes
            value = token.value[1:-1]
            return Literal(value=value, type="string")

        elif self._match("true"):
            self._advance()
            return Literal(value=True, type="boolean")

        elif self._match("false"):
            self._advance()
            return Literal(value=False, type="boolean")

        elif self._match("null"):
            self._advance()
            return Literal(value=None, type="null")

        # Array literal
        elif self._match("["):
            self._advance()
            elements = []
            if not self._match("]"):
                while True:
                    elements.append(self._parse_expression())
                    if not self._match(","):
                        break
                    self._advance()
            self._consume("]")
            return ArrayLiteral(elements=elements)

        # Identifier or struct literal
        elif token.type == TokenType.IDENTIFIER:
            name = self._consume_identifier()
            # Check for struct literal
            if self._match("{"):
                self._advance()
                fields = {}
                if not self._match("}"):
                    while True:
                        field_name = self._consume_identifier()
                        self._consume(":")
                        field_value = self._parse_expression()
                        fields[field_name] = field_value
                        if not self._match(","):
                            break
                        self._advance()
                self._consume("}")
                return StructLiteral(name=name, fields=fields)
            else:
                return Identifier(name=name)

        # Grouped expression
        elif self._match("("):
            self._advance()
            expr = self._parse_expression()
            self._consume(")")
            return expr

        else:
            raise SyntaxError(f"Unexpected token: {token.value}")

    # Helper methods
    def _consume_identifier(self) -> str:
        """Consume and return an identifier"""
        token = self._current_token()
        if token.type != TokenType.IDENTIFIER:
            raise SyntaxError(f"Expected identifier but got '{token.value}'")
        self._advance()
        return token.value

    def _consume_string(self) -> str:
        """Consume and return a string (without quotes)"""
        token = self._current_token()
        if token.type != TokenType.STRING:
            raise SyntaxError(f"Expected string but got '{token.value}'")
        self._advance()
        return token.value[1:-1]  # Remove quotes


# Example usage
if __name__ == "__main__":
    from lexer import Lexer

    code = """
    fn main() {
        let x: Int = 42;
        let y = 3.14;
        if x > 0 {
            return "positive";
        }
    }
    """

    # Lex the code
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    print("Tokens:")
    for token in tokens:
        print(f"  {token}")

    # Parse the tokens
    parser = Parser(tokens)
    ast = parser.parse()
    print("\nAST:")
    print(ast)
