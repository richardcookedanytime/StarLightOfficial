#!/usr/bin/env python3
"""
Starlight 增强特性测试套件
测试语法糖、逻辑化扩展和声明式编程特性
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from compiler.lexer import Lexer
from compiler.enhanced_parser import EnhancedParser

def test_data_class_parsing():
    """测试数据类解析"""
    print("=== 测试数据类解析 ===")
    
    code = """
    data User(name: string, age: int) {
        fun isAdult(): boolean = age >= 18
    }
    """
    
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        print(f"词法分析成功，生成 {len(tokens)} 个 token")
        
        parser = EnhancedParser(tokens)
        ast = parser.parse()
        print(f"语法分析成功，生成 {len(ast.statements)} 个语句")
        
        if ast.statements:
            data_class = ast.statements[0]
            print(f"数据类名: {data_class.name}")
            print(f"字段数量: {len(data_class.fields)}")
            print(f"方法数量: {len(data_class.methods)}")
        
        return True
    except Exception as e:
        print(f"❌ 数据类解析失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_rule_system():
    """测试规则系统"""
    print("\n=== 测试规则系统 ===")
    
    code = """
    rule adult(User.age >= 18) => User.canVote = true
    
    rule eligibility(user: User, product: Product) => {
        if (user.isAdult() && product.price <= user.budget) {
            user.canPurchase = true
        }
    }
    """
    
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        print("Tokens:")
        for i, token in enumerate(tokens[:20]):  # 显示前20个
            print(f"  {i}: {token}")
        
        parser = EnhancedParser(tokens)
        ast = parser.parse()
        print("✅ 规则系统解析成功")
        
        if ast.statements:
            for stmt in ast.statements:
                print(f"  规则类型: {type(stmt).__name__}")
        
        return True
    except Exception as e:
        print(f"❌ 规则系统解析失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_extension_functions():
    """测试扩展函数"""
    print("\n=== 测试扩展函数 ===")
    
    code = """
    extend String {
        fun isEmail(): boolean = this.contains("@")
        fun capitalize(): string = this.substring(0, 1).toUpperCase() + this.substring(1)
    }
    """
    
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        parser = EnhancedParser(tokens)
        ast = parser.parse()
        print("✅ 扩展函数解析成功")
        
        if ast.statements:
            extension = ast.statements[0]
            print(f"  扩展类型: {extension.target_type}")
            print(f"  函数数量: {len(extension.functions)}")
        
        return True
    except Exception as e:
        print(f"❌ 扩展函数解析失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_list_comprehension():
    """测试列表推导式"""
    print("\n=== 测试列表推导式 ===")
    
    code = """
    val names = [user.name | for user in users if user.age > 18]
    """
    
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        print("Tokens:")
        for i, token in enumerate(tokens):
            print(f"  {i}: {token}")
        
        parser = EnhancedParser(tokens)
        ast = parser.parse()
        print("✅ 列表推导式解析成功")
        
        return True
    except Exception as e:
        print(f"❌ 列表推导式解析失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_transaction_block():
    """测试事务块"""
    print("\n=== 测试事务块 ===")
    
    code = """
    transaction {
        account1 -= 100
        account2 += 100
    }
    """
    
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        parser = EnhancedParser(tokens)
        ast = parser.parse()
        print("✅ 事务块解析成功")
        
        if ast.statements:
            transaction = ast.statements[0]
            print(f"  事务语句数量: {len(transaction.statements)}")
        
        return True
    except Exception as e:
        print(f"❌ 事务块解析失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_version_and_features():
    """测试版本和特性声明"""
    print("\n=== 测试版本和特性声明 ===")
    
    code = """
    @version("1.0")
    @feature("rules", enabled=true)
    @feature("comprehensions", enabled=false)
    """
    
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        print("Tokens:")
        for i, token in enumerate(tokens):
            print(f"  {i}: {token}")
        
        parser = EnhancedParser(tokens)
        ast = parser.parse()
        print("✅ 版本和特性声明解析成功")
        
        if ast.statements:
            for stmt in ast.statements:
                print(f"  声明类型: {type(stmt).__name__}")
        
        return True
    except Exception as e:
        print(f"❌ 版本和特性声明解析失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pipe_expression():
    """测试管道表达式"""
    print("\n=== 测试管道表达式 ===")
    
    code = """
    val result = users | filter { it.age > 18 } | map { it.name }
    """
    
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        parser = EnhancedParser(tokens)
        ast = parser.parse()
        print("✅ 管道表达式解析成功")
        
        return True
    except Exception as e:
        print(f"❌ 管道表达式解析失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_complex_program():
    """测试复杂程序"""
    print("\n=== 测试复杂程序 ===")
    
    code = """
    @version("1.0")
    @feature("rules", enabled=true)
    
    data User(name: string, age: int) {
        fun isAdult(): boolean = age >= 18
    }
    
    rule adult(User.age >= 18) => User.canVote = true
    
    extend String {
        fun isEmail(): boolean = this.contains("@")
    }
    
    fun processUsers(users: List<User>): List<string> {
        return [user.name | for user in users if user.isAdult()]
    }
    
    fun main() {
        val users = listOf(User("Alice", 25), User("Bob", 17))
        val adultNames = processUsers(users)
        println(adultNames)
    }
    """
    
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        parser = EnhancedParser(tokens)
        ast = parser.parse()
        print("✅ 复杂程序解析成功")
        
        print(f"解析出 {len(ast.statements)} 个语句:")
        for i, stmt in enumerate(ast.statements):
            print(f"  {i}: {type(stmt).__name__}")
            if hasattr(stmt, 'name'):
                print(f"    名称: {stmt.name}")
        
        return True
    except Exception as e:
        print(f"❌ 复杂程序解析失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starlight 增强特性测试套件")
    print("=" * 60)
    
    tests = [
        test_data_class_parsing,
        test_rule_system,
        test_extension_functions,
        test_list_comprehension,
        test_transaction_block,
        test_version_and_features,
        test_pipe_expression,
        test_complex_program
    ]
    
    success_count = 0
    total_tests = len(tests)
    
    for test in tests:
        if test():
            success_count += 1
    
    print(f"\n测试结果: {success_count}/{total_tests} 通过")
    print("=" * 60)
    
    if success_count == total_tests:
        print("🎉 所有测试通过！Starlight 增强特性实现成功！")
    else:
        print(f"⚠️  有 {total_tests - success_count} 个测试失败，需要修复")
