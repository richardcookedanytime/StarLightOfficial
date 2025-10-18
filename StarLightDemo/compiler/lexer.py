#!/usr/bin/env python3
"""
Starlight 编程语言 - 词法分析器
负责将源代码解析为 Token 序列
"""

import re
from typing import List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class TokenType(Enum):
    # 字面量
    IDENTIFIER = "IDENTIFIER"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    
    # 关键字
    FUNC = "func"
    LET = "let"
    VAR = "var"
    CONST = "const"
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    FOR = "for"
    MATCH = "match"
    CASE = "case"
    RETURN = "return"
    ASYNC = "async"
    AWAIT = "await"
    TRY = "try"
    CATCH = "catch"
    THROW = "throw"
    IMPORT = "import"
    EXPORT = "export"
    STRUCT = "struct"
    ENUM = "enum"
    INTERFACE = "interface"
    TYPE = "type"
    ACTOR = "actor"
    SPAWN = "spawn"
    RECEIVE = "receive"
    REPLY = "reply"
    
    # Starlight 扩展关键字
    DATA = "data"
    RULE = "rule"
    EXTEND = "extend"
    TRANSACTION = "transaction"
    EXPECT = "expect"
    ACTUAL = "actual"
    VERSION = "version"
    FEATURE = "feature"
    PIPE_KEYWORD = "pipe"
    YIELD = "yield"
    
    # 运算符
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MODULO = "%"
    ASSIGN = "="
    EQUALS = "=="
    NOT_EQUALS = "!="
    LESS = "<"
    GREATER = ">"
    LESS_EQUAL = "<="
    GREATER_EQUAL = ">="
    AND = "&&"
    OR = "||"
    NOT = "!"
    DOT = "."
    ARROW = "->"
    FAT_ARROW = "=>"
    
    # 分隔符
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    LEFT_BRACKET = "["
    RIGHT_BRACKET = "]"
    SEMICOLON = ";"
    COMMA = ","
    COLON = ":"
    QUESTION = "?"
    PIPE = "|"
    AMPERSAND = "&"
    AT = "@"
    
    # 特殊
    NEWLINE = "NEWLINE"
    EOF = "EOF"
    COMMENT = "COMMENT"

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int
    
    def __str__(self):
        return f"Token({self.type.value}, '{self.value}', {self.line}:{self.column})"

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
        # 关键字映射
        self.keywords = {
            'func': TokenType.FUNC,
            'let': TokenType.LET,
            'var': TokenType.VAR,
            'const': TokenType.CONST,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'for': TokenType.FOR,
            'match': TokenType.MATCH,
            'case': TokenType.CASE,
            'return': TokenType.RETURN,
            'async': TokenType.ASYNC,
            'await': TokenType.AWAIT,
            'try': TokenType.TRY,
            'catch': TokenType.CATCH,
            'throw': TokenType.THROW,
            'import': TokenType.IMPORT,
            'export': TokenType.EXPORT,
            'struct': TokenType.STRUCT,
            'enum': TokenType.ENUM,
            'interface': TokenType.INTERFACE,
            'type': TokenType.TYPE,
            'actor': TokenType.ACTOR,
            'spawn': TokenType.SPAWN,
            'receive': TokenType.RECEIVE,
            'reply': TokenType.REPLY,
            'data': TokenType.DATA,
            'rule': TokenType.RULE,
            'extend': TokenType.EXTEND,
            'transaction': TokenType.TRANSACTION,
            'expect': TokenType.EXPECT,
            'actual': TokenType.ACTUAL,
            'version': TokenType.VERSION,
            'feature': TokenType.FEATURE,
            'pipe': TokenType.PIPE_KEYWORD,
            'yield': TokenType.YIELD,
            'true': TokenType.BOOLEAN,
            'false': TokenType.BOOLEAN,
            'null': TokenType.BOOLEAN,
        }
    
    def tokenize(self) -> List[Token]:
        """将源代码转换为 Token 序列"""
        while self.position < len(self.source):
            self._skip_whitespace()
            
            if self.position >= len(self.source):
                break
                
            current_char = self.source[self.position]
            
            # 处理标识符和关键字
            if current_char.isalpha() or current_char == '_':
                token = self._read_identifier_or_keyword()
                if token:
                    self.tokens.append(token)
            
            # 处理数字
            elif current_char.isdigit():
                token = self._read_number()
                if token:
                    self.tokens.append(token)
            
            # 处理字符串
            elif current_char == '"' or current_char == "'":
                token = self._read_string()
                if token:
                    self.tokens.append(token)
            
            # 处理运算符和分隔符
            elif current_char in '+-*/%=!<>(){}[];,:?|&':
                token = self._read_operator_or_delimiter()
                if token:
                    self.tokens.append(token)
            
            # 处理注释
            elif current_char == '/':
                if self.position + 1 < len(self.source) and self.source[self.position + 1] == '/':
                    self._skip_line_comment()
                elif self.position + 1 < len(self.source) and self.source[self.position + 1] == '*':
                    self._skip_block_comment()
                else:
                    token = self._read_operator_or_delimiter()
                    if token:
                        self.tokens.append(token)
            
            # 处理换行符
            elif current_char == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\n', self.line, self.column))
                self._advance()
                self.line += 1
                self.column = 1
            
            else:
                # 未知字符，跳过
                self._advance()
        
        # 添加 EOF token
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens
    
    def _skip_whitespace(self):
        """跳过空白字符"""
        while self.position < len(self.source) and self.source[self.position].isspace() and self.source[self.position] != '\n':
            self._advance()
    
    def _advance(self):
        """前进一个字符"""
        if self.position < len(self.source):
            self.position += 1
            self.column += 1
    
    def _read_identifier_or_keyword(self) -> Optional[Token]:
        """读取标识符或关键字"""
        start_pos = self.position
        start_line = self.line
        start_col = self.column
        
        while (self.position < len(self.source) and 
               (self.source[self.position].isalnum() or self.source[self.position] == '_')):
            self._advance()
        
        value = self.source[start_pos:self.position]
        
        # 检查是否为关键字
        if value in self.keywords:
            return Token(self.keywords[value], value, start_line, start_col)
        else:
            return Token(TokenType.IDENTIFIER, value, start_line, start_col)
    
    def _read_number(self) -> Optional[Token]:
        """读取数字（整数或浮点数）"""
        start_pos = self.position
        start_line = self.line
        start_col = self.column
        
        # 读取整数部分
        while self.position < len(self.source) and self.source[self.position].isdigit():
            self._advance()
        
        # 检查是否为浮点数
        if (self.position < len(self.source) and 
            self.source[self.position] == '.' and 
            self.position + 1 < len(self.source) and 
            self.source[self.position + 1].isdigit()):
            
            self._advance()  # 跳过小数点
            
            # 读取小数部分
            while self.position < len(self.source) and self.source[self.position].isdigit():
                self._advance()
            
            value = self.source[start_pos:self.position]
            return Token(TokenType.FLOAT, value, start_line, start_col)
        else:
            value = self.source[start_pos:self.position]
            return Token(TokenType.INTEGER, value, start_line, start_col)
    
    def _read_string(self) -> Optional[Token]:
        """读取字符串"""
        quote_char = self.source[self.position]
        start_line = self.line
        start_col = self.column
        
        self._advance()  # 跳过开始引号
        
        value = ""
        while self.position < len(self.source) and self.source[self.position] != quote_char:
            if self.source[self.position] == '\\' and self.position + 1 < len(self.source):
                # 处理转义字符
                self._advance()
                escape_char = self.source[self.position]
                if escape_char == 'n':
                    value += '\n'
                elif escape_char == 't':
                    value += '\t'
                elif escape_char == 'r':
                    value += '\r'
                elif escape_char == '\\':
                    value += '\\'
                elif escape_char == '"':
                    value += '"'
                elif escape_char == "'":
                    value += "'"
                else:
                    value += escape_char
                self._advance()
            else:
                value += self.source[self.position]
                self._advance()
        
        if self.position < len(self.source):
            self._advance()  # 跳过结束引号
        
        return Token(TokenType.STRING, value, start_line, start_col)
    
    def _read_operator_or_delimiter(self) -> Optional[Token]:
        """读取运算符或分隔符"""
        current_char = self.source[self.position]
        start_line = self.line
        start_col = self.column
        
        # 双字符运算符
        if self.position + 1 < len(self.source):
            two_char = self.source[self.position:self.position + 2]
            
            double_char_ops = {
                '->': TokenType.ARROW,
                '=>': TokenType.FAT_ARROW,
                '==': TokenType.EQUALS,
                '!=': TokenType.NOT_EQUALS,
                '<=': TokenType.LESS_EQUAL,
                '>=': TokenType.GREATER_EQUAL,
                '&&': TokenType.AND,
                '||': TokenType.OR,
            }
            
            if two_char in double_char_ops:
                self._advance()
                self._advance()
                return Token(double_char_ops[two_char], two_char, start_line, start_col)
        
        # 单字符运算符和分隔符
        single_char_ops = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULTIPLY,
            '/': TokenType.DIVIDE,
            '%': TokenType.MODULO,
            '=': TokenType.ASSIGN,
            '<': TokenType.LESS,
            '>': TokenType.GREATER,
            '!': TokenType.NOT,
            '.': TokenType.DOT,
            '(': TokenType.LEFT_PAREN,
            ')': TokenType.RIGHT_PAREN,
            '{': TokenType.LEFT_BRACE,
            '}': TokenType.RIGHT_BRACE,
            '[': TokenType.LEFT_BRACKET,
            ']': TokenType.RIGHT_BRACKET,
            ';': TokenType.SEMICOLON,
            ',': TokenType.COMMA,
            ':': TokenType.COLON,
            '?': TokenType.QUESTION,
            '|': TokenType.PIPE,
            '&': TokenType.AMPERSAND,
        }
        
        if current_char in single_char_ops:
            self._advance()
            return Token(single_char_ops[current_char], current_char, start_line, start_col)
        
        return None
    
    def _skip_line_comment(self):
        """跳过单行注释"""
        while self.position < len(self.source) and self.source[self.position] != '\n':
            self._advance()
    
    def _skip_block_comment(self):
        """跳过块注释"""
        self._advance()  # 跳过第一个 *
        self._advance()  # 跳过第二个 *
        
        while self.position < len(self.source) - 1:
            if (self.source[self.position] == '*' and 
                self.source[self.position + 1] == '/'):
                self._advance()
                self._advance()
                break
            self._advance()

def lex_file(filename: str) -> List[Token]:
    """从文件读取源代码并词法分析"""
    with open(filename, 'r', encoding='utf-8') as f:
        source = f.read()
    
    lexer = Lexer(source)
    return lexer.tokenize()

if __name__ == "__main__":
    # 测试词法分析器
    test_code = '''
    func greet(name: string) -> string {
        return "Hello, ${name}!"
    }
    
    let message = greet("World")
    '''
    
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    
    for token in tokens:
        print(token)
