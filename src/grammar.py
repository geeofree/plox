from abc import ABC, abstractmethod
from src.token import TokenType


class Expr(ABC):
    @abstractmethod
    def visit_binary(self, expr: 'BinaryExpr'):
        pass


    @abstractmethod
    def visit_unary(self, expr: 'UnaryExpr'):
        pass


    @abstractmethod
    def visit_group(self, expr: 'GroupExpr'):
        pass


    @abstractmethod
    def visit_literal(self, expr: 'LiteralExpr'):
        pass


    @abstractmethod
    def visit_not_implemented_expr(self, expr: 'NotImplementedExpr'):
        pass


class ExprElem(ABC):
    @abstractmethod
    def accept(self, expr: Expr):
        pass


class BinaryExpr(ExprElem):
    def __init__(self, left: ExprElem, operator: TokenType, right: ExprElem) -> None:
        self.left = left
        self.operator = operator
        self.right = right


    def accept(self, expr: Expr):
        return expr.visit_binary(self)


class UnaryExpr(ExprElem):
    def __init__(
        self,
        symbol: TokenType,
        unary: ExprElem
    ) -> None:
        self.symbol = symbol
        self.unary = unary


    def accept(self, expr: Expr):
        return expr.visit_unary(self)


class GroupExpr(ExprElem):
    def __init__(self, group: ExprElem) -> None:
        self.group = group


    def accept(self, expr: Expr):
        return expr.visit_group(self)


class LiteralExpr(ExprElem):
    def __init__(self, literal: str | int | float | bool | None) -> None:
        self.literal = literal


    def accept(self, expr: Expr):
        return expr.visit_literal(self)


class NotImplementedExpr(ExprElem):
    def accept(self, expr: Expr):
        return expr.visit_not_implemented_expr(self)
