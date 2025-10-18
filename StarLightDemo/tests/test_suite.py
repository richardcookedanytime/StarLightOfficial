#!/usr/bin/env python3
"""
Starlight 编译器测试套件
"""

import sys
import os
import unittest
import tempfile
import subprocess
from pathlib import Path

# 添加编译器路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compiler.lexer import Lexer, TokenType
from compiler.parser import Parser
from compiler.semantic_analyzer import SemanticAnalyzer
from compiler.jvm_backend import JVMCodeGenerator
from compiler.js_backend import JavaScriptCodeGenerator

class TestLexer(unittest.TestCase):
    """测试词法分析器"""
    
    def test_basic_tokens(self):
        """测试基本 token"""
        code = 'func hello() { return "world"; }'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.FUNC)
        self.assertEqual(tokens[1].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].value, "hello")
    
    def test_string_literal(self):
        """测试字符串字面量"""
        code = '"Hello, World!"'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.STRING)
        self.assertEqual(tokens[0].value, "Hello, World!")
    
    def test_numbers(self):
        """测试数字"""
        code = '42 3.14'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.INTEGER)
        self.assertEqual(tokens[0].value, "42")
        self.assertEqual(tokens[1].type, TokenType.FLOAT)
        self.assertEqual(tokens[1].value, "3.14")

class TestParser(unittest.TestCase):
    """测试语法分析器"""
    
    def test_function_declaration(self):
        """测试函数声明"""
        code = '''
        func greet(name: string) -> string {
            return "Hello, " + name;
        }
        '''
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        self.assertEqual(len(ast.statements), 1)
        self.assertEqual(ast.statements[0].name, "greet")
        self.assertEqual(len(ast.statements[0].parameters), 1)
    
    def test_variable_declaration(self):
        """测试变量声明"""
        code = 'let message = "Hello World";'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        self.assertEqual(len(ast.statements), 1)
        self.assertEqual(ast.statements[0].name, "message")
        self.assertIsNotNone(ast.statements[0].initializer)
    
    def test_function_call(self):
        """测试函数调用"""
        code = 'greet("World");'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        self.assertEqual(len(ast.statements), 1)
        expr_stmt = ast.statements[0]
        self.assertIsNotNone(expr_stmt.expression)
        self.assertEqual(expr_stmt.expression.callee.name, "greet")

class TestSemanticAnalyzer(unittest.TestCase):
    """测试语义分析器"""
    
    def test_symbol_table(self):
        """测试符号表"""
        code = '''
        func greet(name: string) -> string {
            return "Hello, " + name;
        }
        let message = greet("World");
        '''
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        result = analyzer.analyze(ast)
        
        self.assertTrue(result['success'])
        self.assertIn('greet', result['symbols'])
        self.assertIn('message', result['symbols'])
    
    def test_undefined_variable(self):
        """测试未定义变量"""
        code = 'let x = undefined_var;'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        result = analyzer.analyze(ast)
        
        self.assertFalse(result['success'])
        self.assertTrue(len(result['errors']) > 0)

class TestJVMBackend(unittest.TestCase):
    """测试 JVM 后端"""
    
    def test_java_code_generation(self):
        """测试 Java 代码生成"""
        code = '''
        func greet(name: string) -> string {
            return "Hello, " + name;
        }
        
        func main() {
            let message = greet("World");
            println(message);
        }
        '''
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        semantic_result = analyzer.analyze(ast)
        
        if semantic_result['success']:
            generator = JVMCodeGenerator()
            java_code = generator.generate(ast, "TestClass")
            
            # 检查生成的代码包含关键元素
            self.assertIn("public class TestClass", java_code)
            self.assertIn("public static String greet", java_code)
            self.assertIn("public static void main", java_code)
            self.assertIn("System.out.println", java_code)
    
    def test_java_compilation(self):
        """测试 Java 编译"""
        code = '''
        func main() {
            println("Hello, Java!");
        }
        '''
        
        # 生成 Java 代码
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        semantic_result = analyzer.analyze(ast)
        
        if semantic_result['success']:
            generator = JVMCodeGenerator()
            java_code = generator.generate(ast, "TestJava")
            
            # 保存到临时文件，确保文件名匹配类名
            temp_dir = tempfile.mkdtemp()
            temp_java = os.path.join(temp_dir, 'TestJava.java')
            
            try:
                with open(temp_java, 'w') as f:
                    f.write(java_code)
                
                # 编译 Java 代码
                result = subprocess.run(['javac', temp_java], 
                                      capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, 
                               f"Java compilation failed: {result.stderr}")
            finally:
                import shutil
                shutil.rmtree(temp_dir)

class TestJavaScriptBackend(unittest.TestCase):
    """测试 JavaScript 后端"""
    
    def test_js_code_generation(self):
        """测试 JavaScript 代码生成"""
        code = '''
        func greet(name) {
            return "Hello, " + name;
        }
        
        func main() {
            let message = greet("World");
            println(message);
        }
        '''
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        semantic_result = analyzer.analyze(ast)
        
        if semantic_result['success']:
            generator = JavaScriptCodeGenerator()
            js_code = generator.generate(ast, "test")
            
            # 检查生成的代码包含关键元素
            self.assertIn("function greet", js_code)
            self.assertIn("function main", js_code)
            self.assertIn("console.log", js_code)
            self.assertIn("export { main }", js_code)
    
    def test_js_execution(self):
        """测试 JavaScript 执行"""
        code = '''
        func main() {
            println("Hello, JavaScript!");
        }
        '''
        
        # 生成 JavaScript 代码
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        semantic_result = analyzer.analyze(ast)
        
        if semantic_result['success']:
            generator = JavaScriptCodeGenerator()
            js_code = generator.generate(ast, "test")
            
            # 保存到临时文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(js_code)
                temp_js = f.name
            
            try:
                # 执行 JavaScript 代码
                result = subprocess.run(['node', temp_js], 
                                      capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, 
                               f"JavaScript execution failed: {result.stderr}")
                self.assertIn("Hello, JavaScript!", result.stdout)
            finally:
                os.unlink(temp_js)

class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_compilation_jvm(self):
        """测试完整的 JVM 编译流程"""
        code = '''
        func add(a: int, b: int) -> int {
            return a + b;
        }
        
        func main() {
            let result = add(5, 3);
            println(result);
        }
        '''
        
        # 完整编译流程
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        semantic_result = analyzer.analyze(ast)
        
        self.assertTrue(semantic_result['success'])
        
        generator = JVMCodeGenerator()
        java_code = generator.generate(ast, "MathTest")
        
        # 验证生成的代码
        self.assertIn("public static int add", java_code)
        self.assertIn("return (a + b)", java_code)
    
    def test_full_compilation_js(self):
        """测试完整的 JavaScript 编译流程"""
        code = '''
        func multiply(a, b) {
            return a * b;
        }
        
        func main() {
            let result = multiply(4, 7);
            println(result);
        }
        '''
        
        # 完整编译流程
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        semantic_result = analyzer.analyze(ast)
        
        self.assertTrue(semantic_result['success'])
        
        generator = JavaScriptCodeGenerator()
        js_code = generator.generate(ast, "math")
        
        # 验证生成的代码
        self.assertIn("function multiply", js_code)
        self.assertIn("return (a * b)", js_code)

def run_tests():
    """运行所有测试"""
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加测试类
    test_classes = [
        TestLexer,
        TestParser,
        TestSemanticAnalyzer,
        TestJVMBackend,
        TestJavaScriptBackend,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    print("🧪 Starlight 编译器测试套件")
    print("=" * 50)
    
    success = run_tests()
    
    if success:
        print("\n🎉 所有测试通过！")
        sys.exit(0)
    else:
        print("\n❌ 部分测试失败！")
        sys.exit(1)
