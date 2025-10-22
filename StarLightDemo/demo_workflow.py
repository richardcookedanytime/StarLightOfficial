#!/usr/bin/env python3
"""
Starlight 语言工作流演示脚本
展示完整的 CI/CD 流程和编译器功能
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(title):
    """打印标题"""
    print(f"\n{'='*60}")
    print(f"🚀 {title}")
    print(f"{'='*60}")

def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"\n📋 {description}")
    print(f"命令: {cmd}")
    print("-" * 40)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("错误输出:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"执行失败: {e}")
        return False

def check_github_workflows():
    """检查 GitHub 工作流配置"""
    print_header("GitHub Actions 工作流检查")
    
    workflows_dir = Path(".github/workflows")
    if not workflows_dir.exists():
        print("❌ .github/workflows 目录不存在")
        return False
    
    workflow_files = list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml"))
    print(f"✅ 找到 {len(workflow_files)} 个工作流文件:")
    
    for workflow in workflow_files:
        print(f"  - {workflow.name}")
    
    return True

def test_compiler():
    """测试编译器功能"""
    print_header("编译器功能测试")
    
    # 检查编译器文件
    compiler_files = [
        "compiler/main.py",
        "compiler/lexer.py", 
        "compiler/parser.py",
        "compiler/semantic_analyzer.py"
    ]
    
    for file in compiler_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} 不存在")
            return False
    
    # 测试编译器帮助信息
    success = run_command("python3 compiler/main.py --help", "测试编译器帮助信息")
    if not success:
        return False
    
    # 测试示例文件编译
    examples = list(Path("examples").glob("*.sl"))
    if not examples:
        print("❌ 没有找到示例文件")
        return False
    
    print(f"✅ 找到 {len(examples)} 个示例文件")
    
    # 测试第一个示例文件
    example_file = examples[0]
    success = run_command(f"python3 compiler/main.py {example_file} --tokens", 
                         f"测试 {example_file} 词法分析")
    
    return success

def check_dependencies():
    """检查依赖项"""
    print_header("依赖项检查")
    
    # 检查 requirements.txt
    if Path("requirements.txt").exists():
        print("✅ requirements.txt 存在")
        with open("requirements.txt", "r") as f:
            deps = f.read().strip()
            print(f"依赖项:\n{deps}")
    else:
        print("❌ requirements.txt 不存在")
        return False
    
    # 检查 Python 版本
    python_version = sys.version_info
    print(f"✅ Python 版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    return True

def simulate_ci_pipeline():
    """模拟 CI 管道"""
    print_header("模拟 CI/CD 管道")
    
    steps = [
        ("代码质量检查", "echo 'Running code quality checks...'"),
        ("运行测试", "echo 'Running tests...'"),
        ("构建项目", "echo 'Building project...'"),
        ("生成文档", "echo 'Generating documentation...'"),
        ("安全检查", "echo 'Running security scans...'"),
        ("部署准备", "echo 'Preparing for deployment...'")
    ]
    
    for step_name, cmd in steps:
        print(f"\n🔄 {step_name}")
        run_command(cmd, step_name)
    
    print("\n✅ CI/CD 管道模拟完成")

def show_deployment_info():
    """显示部署信息"""
    print_header("部署信息")
    
    print("📋 部署配置:")
    print("  - 源仓库: 当前仓库")
    print("  - 目标仓库: richardcookedanytime/StarLightOfficial")
    print("  - 触发条件: 推送到 main/master 分支")
    print("  - 自动同步: 是")
    
    print("\n📋 工作流文件:")
    workflow_files = [
        ".github/workflows/ci.yml - 持续集成",
        ".github/workflows/deploy.yml - 自动部署", 
        ".github/workflows/setup-repo.yml - 仓库设置"
    ]
    
    for workflow in workflow_files:
        print(f"  ✅ {workflow}")
    
    print("\n📋 下一步操作:")
    print("  1. git add .")
    print("  2. git commit -m 'Add GitHub Actions workflows'")
    print("  3. git push origin main")
    print("  4. 查看 GitHub Actions 标签页")

def main():
    """主函数"""
    print("🌟 Starlight 语言工作流演示")
    print("=" * 60)
    
    # 检查当前目录
    if not Path("compiler").exists():
        print("❌ 请在项目根目录运行此脚本")
        sys.exit(1)
    
    # 执行各项检查
    checks = [
        ("GitHub 工作流", check_github_workflows),
        ("依赖项", check_dependencies),
        ("编译器", test_compiler),
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        if not check_func():
            print(f"❌ {check_name} 检查失败")
            all_passed = False
        else:
            print(f"✅ {check_name} 检查通过")
    
    if all_passed:
        print_header("🎉 所有检查通过！")
        simulate_ci_pipeline()
        show_deployment_info()
    else:
        print_header("❌ 部分检查失败")
        print("请修复上述问题后重新运行")

if __name__ == "__main__":
    main()
