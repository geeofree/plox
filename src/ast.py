from typing import Any, List
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
        self.print_expr_list: List[tuple[str, int, Any]] = []


    def print(self):
        self.visit_expressions(self.expr)
        print(self.get_print_str())


    def get_print_str(self):
        print_str = ""
        total_list = len(self.print_expr_list) - 1
        for index, item in enumerate(self.print_expr_list):
            token, indent_level, value = item
            if indent_level > 1:
                start_prefix = "┣" if index < total_list else "┗"
                print_str += start_prefix
                print_str += "━" * (indent_level - 1)
            print_str += token
            if value is not None:
                print_str += f" {value}"
            if index < total_list:
                print_str += "\n"
        return print_str


    def add_print_expr_item(self, expr: str, value: Any = None):
        self.print_expr_list.append((expr, self.indent_level, value))


    def visit_expressions(self, expr):
        self.indent_level += 1
        match expr:
            case _bin if isinstance(expr, BinaryExpr):
                self.visit_binary(_bin)
                self.indent_level -= 1
            case _group if isinstance(expr, GroupExpr):
                self.visit_group(_group)
                self.indent_level -= 1
            case _unary if isinstance(expr, UnaryExpr):
                self.visit_unary(_unary)
                self.indent_level -= 1
            case _literal if isinstance(expr, LiteralExpr):
                self.visit_literal(_literal)


    def visit_binary(self, expr):
        self.add_print_expr_item('BINARY')
        self.visit_expressions(expr.left)
        operator = ""
        match expr.operator:
            case TokenType.EQUAL_EQUAL:
                operator += "=="
            case TokenType.BANG_EQUAL:
                operator += "!="
            case TokenType.GT:
                operator += ">"
            case TokenType.LT:
                operator += "<"
            case TokenType.GT_EQUAL:
                operator += ">="
            case TokenType.LT_EQUAL:
                operator += "<="
            case TokenType.PLUS:
                operator += "+"
            case TokenType.MINUS:
                operator += "-"
            case TokenType.STAR:
                operator += "*"
            case TokenType.STAR_STAR:
                operator += "**"
            case TokenType.SLASH:
                operator += "/"
            case TokenType.SLASH_SLASH:
                operator += "//"
        self.add_print_expr_item('OPERATOR', operator)
        self.indent_level -= 1
        self.visit_expressions(expr.right)


    def visit_group(self, expr):
        self.add_print_expr_item('GROUP')
        self.visit_expressions(expr.group)


    def visit_unary(self, expr):
        symbol = ""
        match expr.symbol:
            case TokenType.NOT:
                symbol += "not"
            case TokenType.MINUS:
                symbol += "-"
        self.add_print_expr_item('UNARY', symbol)
        self.visit_expressions(expr.unary)


    def visit_literal(self, expr):
        literal = ""
        if expr.literal is None:
            literal += "nil"
        else:
            literal += str(expr.literal)
        self.add_print_expr_item('LITERAL', literal)


    def visit_not_implemented_expr(self, expr):
        print("Not implemented")
