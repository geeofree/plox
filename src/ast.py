from .grammar import BinaryExpr, Expr, ExprElem, LiteralExpr, UnaryExpr, GroupExpr
from .token import TokenType

class AstParser(Expr):
    @staticmethod
    def print(expr: ExprElem):
        _AstPrinter(expr).print()


class _AstPrinter(Expr):
    def __init__(self, expr: ExprElem) -> None:
        self.expr = expr
        self.indent_level = 0
        self.print_string = ""


    def print(self):
        self.visit_expressions(self.expr)
        print(self.print_string)


    def add_indent(self, indent_level: int | None=None):
        indent_level = indent_level if indent_level is not None else self.indent_level
        if self.indent_level > 1:
            self.print_string += "┣" + ("━" * (indent_level - 1))
        elif self.indent_level == 1:
            self.print_string += "┣"


    def visit_expressions(self, expr):
        self.add_indent()
        self.indent_level += 1
        match expr:
            case _bin if isinstance(expr, BinaryExpr):
                self.print_string += "[BINARY]\n"
                self.visit_binary(_bin)
                self.indent_level -= 1
            case _group if isinstance(expr, GroupExpr):
                self.print_string += "[GROUP]\n"
                self.visit_group(_group)
                self.indent_level -= 1
            case _unary if isinstance(expr, UnaryExpr):
                self.print_string += "[UNARY] "
                self.visit_unary(_unary)
                self.indent_level -= 1
            case _literal if isinstance(expr, LiteralExpr):
                self.print_string += "[LITERAL] "
                self.visit_literal(_literal)


    def visit_binary(self, expr):
        self.visit_expressions(expr.left)
        self.print_string += "\n"
        self.add_indent(self.indent_level - 1)
        self.print_string += "[OPERATOR] "
        match expr.operator:
            case TokenType.EQUAL_EQUAL:
                self.print_string += "=="
            case TokenType.BANG_EQUAL:
                self.print_string += "!="
            case TokenType.GT:
                self.print_string += ">"
            case TokenType.LT:
                self.print_string += "<"
            case TokenType.GT_EQUAL:
                self.print_string += ">="
            case TokenType.LT_EQUAL:
                self.print_string += "<="
            case TokenType.PLUS:
                self.print_string += "+"
            case TokenType.MINUS:
                self.print_string += "-"
            case TokenType.STAR:
                self.print_string += "*"
            case TokenType.STAR_STAR:
                self.print_string += "**"
            case TokenType.SLASH:
                self.print_string += "/"
            case TokenType.SLASH_SLASH:
                self.print_string += "//"
        self.print_string += "\n"
        self.indent_level -= 1
        self.visit_expressions(expr.right)


    def visit_group(self, expr):
        self.visit_expressions(expr.group)


    def visit_unary(self, expr):
        match expr.symbol:
            case TokenType.NOT:
                self.print_string += "not"
            case TokenType.MINUS:
                self.print_string += "-"
        self.print_string += "\n"
        self.visit_expressions(expr.unary)


    def visit_literal(self, expr):
        if expr.literal is None:
            self.print_string += "nil"
        else:
            self.print_string += str(expr.literal)


    def visit_not_implemented_expr(self, expr):
        print("Not implemented")
