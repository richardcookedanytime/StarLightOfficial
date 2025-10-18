# Starlight 语法规范 (EBNF)

## 📋 语法版本管理

**版本**: 1.0  
**兼容性**: Java 17+, Kotlin 1.9+  
**更新日期**: 2024年1月

## 🎯 核心语法规则

### 1. 程序结构

```ebnf
program = package_declaration? import_declaration* statement* EOF;

package_declaration = "package" qualified_name ";";
import_declaration = "import" qualified_name ( "." "*" )? ";";
```

### 2. 语句 (Statements)

```ebnf
statement = 
    | function_declaration
    | class_declaration
    | data_class_declaration
    | interface_declaration
    | variable_declaration
    | expression_statement
    | block_statement
    | control_statement
    | rule_declaration
    ;

function_declaration = 
    "async"? "fun" identifier type_parameters? 
    "(" parameter_list? ")" 
    ( ":" type_expression )?
    block;

class_declaration = 
    "class" identifier type_parameters? 
    ( ":" type_expression )?
    "{" class_member* "}";

data_class_declaration = 
    "data" identifier type_parameters? 
    "(" parameter_list? ")" 
    "{" class_member* "}";

interface_declaration = 
    "interface" identifier type_parameters? 
    "{" interface_member* "}";

variable_declaration = 
    ( "val" | "var" ) identifier ( ":" type_expression )? 
    "=" expression ";";

expression_statement = expression ";";
block_statement = "{" statement* "}";
```

### 3. 表达式 (Expressions)

```ebnf
expression = 
    | assignment_expression
    | conditional_expression
    | logical_or_expression
    | logical_and_expression
    | equality_expression
    | relational_expression
    | additive_expression
    | multiplicative_expression
    | unary_expression
    | postfix_expression
    | primary_expression
    ;

assignment_expression = 
    identifier assignment_operator expression;

conditional_expression = 
    logical_or_expression ( "?" expression ":" expression )?;

logical_or_expression = 
    logical_and_expression ( "||" logical_and_expression )*;

logical_and_expression = 
    equality_expression ( "&&" equality_expression )*;

equality_expression = 
    relational_expression ( ( "==" | "!=" ) relational_expression )*;

relational_expression = 
    additive_expression ( ( "<" | ">" | "<=" | ">=" ) additive_expression )*;

additive_expression = 
    multiplicative_expression ( ( "+" | "-" ) multiplicative_expression )*;

multiplicative_expression = 
    unary_expression ( ( "*" | "/" | "%" ) unary_expression )*;

unary_expression = 
    ( "+" | "-" | "!" | "await" )? postfix_expression;

postfix_expression = 
    primary_expression ( 
        | "(" argument_list? ")"
        | "." identifier
        | "[" expression "]"
        | "?" "." identifier
        | "!!"
        | "++"
        | "--"
    )*;
```

### 4. 主要表达式 (Primary Expressions)

```ebnf
primary_expression = 
    | literal
    | identifier
    | "(" expression ")"
    | lambda_expression
    | list_comprehension
    | pattern_match
    | rule_expression
    ;

literal = 
    | integer_literal
    | float_literal
    | string_literal
    | boolean_literal
    | null_literal
    | list_literal
    | map_literal
    ;

integer_literal = digit+;
float_literal = digit+ "." digit+;
string_literal = '"' string_content* '"' | "'" string_content* "'";
boolean_literal = "true" | "false";
null_literal = "null";

list_literal = "[" ( expression ( "," expression )* )? "]";
map_literal = "{" ( map_entry ( "," map_entry )* )? "}";
map_entry = expression ":" expression;
```

### 5. 类型系统

```ebnf
type_expression = 
    | primitive_type
    | reference_type
    | nullable_type
    | generic_type
    | function_type
    | union_type
    | intersection_type
    | type_alias
    ;

primitive_type = 
    "int" | "long" | "float" | "double" | 
    "boolean" | "char" | "string" | "void";

reference_type = qualified_name type_arguments?;

nullable_type = type_expression "?";
generic_type = identifier "<" type_expression ( "," type_expression )* ">";

function_type = 
    "(" type_expression ( "," type_expression )* ")" "->" type_expression;

union_type = type_expression ( "|" type_expression )+;
intersection_type = type_expression ( "&" type_expression )+;

type_alias = "type" identifier "=" type_expression;
```

### 6. 高级特性

#### 6.1 模式匹配

```ebnf
pattern_match = 
    "match" expression "{" pattern_case+ "}";

pattern_case = 
    pattern ( "if" expression )? "=>" expression;

pattern = 
    | literal_pattern
    | identifier_pattern
    | constructor_pattern
    | type_pattern
    | destructuring_pattern
    | wildcard_pattern
    ;

literal_pattern = literal;
identifier_pattern = identifier;
constructor_pattern = identifier "(" pattern ( "," pattern )* ")";
type_pattern = identifier ":" type_expression;
destructuring_pattern = "{" pattern ( "," pattern )* "}";
wildcard_pattern = "_";
```

#### 6.2 Lambda 表达式

```ebnf
lambda_expression = 
    "(" parameter_list? ")" ( ":" type_expression )? "=>" expression;

parameter_list = 
    parameter ( "," parameter )*;

parameter = 
    identifier ( ":" type_expression )?;
```

#### 6.3 列表推导式

```ebnf
list_comprehension = 
    "[" expression "|" comprehension_clause+ "]";

comprehension_clause = 
    "for" identifier "in" expression ( "if" expression )?;
```

#### 6.4 规则系统

```ebnf
rule_declaration = 
    "rule" rule_condition "=>" rule_action;

rule_condition = expression;
rule_action = expression;

rule_expression = 
    "rule" "{" rule_declaration+ "}";
```

#### 6.5 扩展函数

```ebnf
extension_function = 
    "extend" type_expression "{" function_declaration+ "}";
```

#### 6.6 异步编程

```ebnf
async_function = 
    "async" "fun" identifier type_parameters? 
    "(" parameter_list? ")" 
    ( ":" type_expression )?
    block;

await_expression = 
    "await" expression;
```

#### 6.7 事务处理

```ebnf
transaction_statement = 
    "transaction" block;
```

### 7. 控制流

```ebnf
control_statement = 
    | if_statement
    | while_statement
    | for_statement
    | try_catch_statement
    | return_statement
    | break_statement
    | continue_statement
    ;

if_statement = 
    "if" "(" expression ")" statement ( "else" statement )?;

while_statement = 
    "while" "(" expression ")" statement;

for_statement = 
    "for" "(" ( variable_declaration | expression )? ";" 
    expression? ";" expression? ")" statement;

try_catch_statement = 
    "try" block 
    ( "catch" "(" identifier ":" type_expression ")" block )* 
    ( "finally" block )?;

return_statement = 
    "return" expression? ";";
```

### 8. 标识符和关键字

```ebnf
identifier = ( letter | "_" ) ( letter | digit | "_" )*;
qualified_name = identifier ( "." identifier )*;

letter = "a".."z" | "A".."Z";
digit = "0".."9";

keyword = 
    "fun" | "class" | "data" | "interface" | "type" | "val" | "var" |
    "if" | "else" | "while" | "for" | "try" | "catch" | "finally" |
    "return" | "break" | "continue" | "throw" |
    "async" | "await" | "match" | "rule" | "extend" |
    "import" | "package" | "public" | "private" | "protected" |
    "static" | "final" | "abstract" | "override" |
    "true" | "false" | "null" | "this" | "super" |
    "int" | "long" | "float" | "double" | "boolean" | "char" | "string" | "void";
```

## 🔧 语法验证工具

### 使用语法验证器

```bash
# 验证语法文件
starlight parse --ast demo.sl

# 输出 JSON AST
starlight parse --json demo.sl

# 检查语法版本兼容性
starlight parse --version 1.0 demo.sl
```

### AST 输出格式

```json
{
  "type": "Program",
  "version": "1.0",
  "statements": [
    {
      "type": "FunctionDeclaration",
      "name": "main",
      "parameters": [],
      "body": {
        "type": "Block",
        "statements": [...]
      }
    }
  ]
}
```

## 📋 语法变更日志

### v1.0 (2024-01-01)
- 初始语法定义
- 基础类型系统
- 函数和类声明
- 模式匹配
- 异步编程支持

### v1.1 (计划中)
- 泛型系统完善
- 更多内置类型
- 标准库集成

---

**Starlight Grammar** - 精确、简洁、可扩展的语法规范 ✨
