from enum import Enum


class DfaState(Enum):
    Initial = 0
    If = 1
    Id_if1 = 2
    Id_if2 = 3
    Else = 4
    Id_else1 = 5
    Id_else2 = 6
    Id_else3 = 7
    Id_else4 = 8
    Int = 9
    Id_int1 = 10
    Id_int2 = 11
    Id_int3 = 12
    Id = 13
    GT = 14
    GE = 15
    Assignment = 16
    Plus = 17
    Minus = 18
    Star = 19
    Slash = 20
    SemiColon = 21
    LeftParen = 22
    RightParen = 23
    IntLiteral = 24


class TokenType(Enum):
    Plus = 0  # +
    Minus = 1  # -
    Star = 3  # *
    Slash = 4  # /

    GE = 5  # >=
    GT = 6  # >
    EQ = 7  # ==
    LE = 8  # <=
    LT = 9  # <

    SemiColon = 10  # ;
    LeftParen = 11  # (
    RightParen = 12  # )

    Assignment = 13  # =

    If = 14
    Else = 15

    Int = 16
    Identifier = 17  # 标识符

    IntLiteral = 18  # 整型字面量
    StringLiteral = 19  # 字符串字面量


class ASTNodeType(Enum):
    Programm = 1  # 程序入口，根节点
    IntDeclaration = 2  # 整型变量声明
    ExpressionStmt = 3  # 表达式语句，即表达式后面跟个分号
    AssignmentStmt = 4  # 赋值语句

    Primary = 5  # 基础表达式
    Multiplicative = 6  # 乘法表达式
    Additive = 7  # 加法表达式

    Identifier = 8  # 标识符
    IntLiteral = 9  # 整型字面量
