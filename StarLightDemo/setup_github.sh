#!/bin/bash

# Starlight 项目 GitHub 仓库设置脚本
# 使用方法: ./setup_github.sh

set -e

echo "🚀 设置 Starlight 项目 GitHub 仓库..."

# 检查必要的工具
check_dependencies() {
    echo "📋 检查依赖..."
    
    if ! command -v git &> /dev/null; then
        echo "❌ Git 未安装，请先安装 Git"
        exit 1
    fi
    
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 未安装，请先安装 Python 3"
        exit 1
    fi
    
    echo "✅ 依赖检查完成"
}

# 初始化 Git 仓库
init_git_repo() {
    echo "🔧 初始化 Git 仓库..."
    
    if [ ! -d ".git" ]; then
        git init
        echo "✅ Git 仓库初始化完成"
    else
        echo "ℹ️  Git 仓库已存在"
    fi
}

# 创建初始提交
create_initial_commit() {
    echo "📝 创建初始提交..."
    
    # 添加所有文件
    git add .
    
    # 创建提交
    git commit -m "feat: 初始项目结构

- 完成 Starlight 编程语言设计文档
- 实现编译器原型（词法分析器 + 语法分析器）
- 创建示例代码和教程
- 建立项目路线图和决策文档

核心特性:
- Java 100% 互操作
- 跨平台编译 (JVM/JS/WASM/Native)
- 轻量化语法设计
- 现代化工具链

下一步:
- 完善编译器后端
- 开发标准库
- 构建开发工具"
    
    echo "✅ 初始提交创建完成"
}

# 创建 GitHub 仓库建议
create_github_repo_suggestions() {
    echo "📋 GitHub 仓库设置建议..."
    
    cat << 'EOF'

🎯 创建 GitHub 仓库步骤:

1. 访问 https://github.com/new
2. 仓库设置:
   - Repository name: starlight
   - Description: Starlight programming language - Write once, run anywhere Java does, and anywhere JavaScript does
   - Visibility: Public
   - Initialize with README: ❌ (我们已经有了)
   - Add .gitignore: ❌ (我们已经有了)
   - Choose a license: MIT (我们已经有了)

3. 推送代码:
   git remote add origin https://github.com/你的用户名/starlight.git
   git branch -M main
   git push -u origin main

4. 仓库设置:
   - 启用 Issues
   - 启用 Discussions
   - 启用 Wiki
   - 添加主题标签: programming-language, jvm, javascript, webassembly, cross-platform, java-interop

5. 创建里程碑:
   - v0.1.0 MVP (2024 Q1)
   - v0.2.0 增强版 (2024 Q2)
   - v0.3.0 生态建设 (2024 Q3)
   - v1.0.0 生产就绪 (2024 Q4)

6. 创建标签:
   - enhancement (功能增强)
   - bug (Bug 修复)
   - documentation (文档)
   - question (问题)
   - help wanted (需要帮助)
   - good first issue (适合新手)

EOF
}

# 创建 CI/CD 配置
create_ci_config() {
    echo "🔧 创建 CI/CD 配置..."
    
    mkdir -p .github/workflows
    
    cat > .github/workflows/ci.yml << 'EOF'
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', 3.11]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest pytest-cov
    
    - name: Test compiler prototype
      run: |
        python3 compiler/lexer.py
        python3 compiler/parser.py
        python3 compiler/main.py examples/hello_world.sl --tokens
        python3 compiler/main.py examples/hello_world.sl --ast
    
    - name: Run tests
      run: |
        pytest tests/ -v --cov=compiler
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true

  build:
    runs-on: ubuntu-latest
    needs: test
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build documentation
      run: |
        echo "Building documentation..."
        # 这里将来添加文档构建命令
    
    - name: Upload build artifacts
      uses: actions/upload-artifact@v3
      with:
        name: build-artifacts
        path: build/
EOF
    
    echo "✅ CI/CD 配置创建完成"
}

# 创建发布配置
create_release_config() {
    echo "📦 创建发布配置..."
    
    cat > .github/workflows/release.yml << 'EOF'
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
      with:
        fetch-depth: 0
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Publish to PyPI
      if: github.event_name == 'push' && startsWith(github.ref, 'refs/tags/')
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
    
    - name: Create GitHub Release
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ github.ref }}
        release_name: Release ${{ github.ref }}
        body: |
          ## 新功能
          - 添加新功能描述
          
          ## Bug 修复
          - 修复问题描述
          
          ## 改进
          - 性能优化
          - 文档更新
        draft: false
        prerelease: false
EOF
    
    echo "✅ 发布配置创建完成"
}

# 创建项目状态徽章
create_badges() {
    echo "🏆 创建项目徽章..."
    
    cat > BADGES.md << 'EOF'
# 项目徽章

## 构建状态
[![CI](https://github.com/starlight-lang/starlight/workflows/CI/badge.svg)](https://github.com/starlight-lang/starlight/actions)
[![Coverage](https://codecov.io/gh/starlight-lang/starlight/branch/main/graph/badge.svg)](https://codecov.io/gh/starlight-lang/starlight)

## 版本信息
[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/starlight-lang/starlight/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 语言支持
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![Rust](https://img.shields.io/badge/rust-1.70%2B-orange.svg)](https://rust-lang.org)
[![Node.js](https://img.shields.io/badge/node.js-16%2B-green.svg)](https://nodejs.org)

## 目标平台
[![JVM](https://img.shields.io/badge/JVM-✅-green.svg)](https://openjdk.java.net)
[![JavaScript](https://img.shields.io/badge/JavaScript-✅-yellow.svg)](https://javascript.info)
[![WebAssembly](https://img.shields.io/badge/WebAssembly-🚧-orange.svg)](https://webassembly.org)
[![Native](https://img.shields.io/badge/Native-📋-blue.svg)](https://llvm.org)

## 社区
[![GitHub stars](https://img.shields.io/github/stars/starlight-lang/starlight?style=social)](https://github.com/starlight-lang/starlight)
[![GitHub forks](https://img.shields.io/github/forks/starlight-lang/starlight?style=social)](https://github.com/starlight-lang/starlight)
[![Discussions](https://img.shields.io/badge/discussions-join-blue.svg)](https://github.com/starlight-lang/starlight/discussions)

## 使用方法
```bash
# 安装
curl -fsSL https://starlight.io/install.sh | bash

# 创建项目
starlight create my-project && cd my-project

# 编译运行
jstarc src/main.sl --target=jvm
jstarc src/main.sl --target=js
jstarc src/main.sl --target=wasm
```
EOF
    
    echo "✅ 项目徽章创建完成"
}

# 主函数
main() {
    echo "🌟 Starlight 编程语言 - GitHub 仓库设置"
    echo "========================================"
    
    check_dependencies
    init_git_repo
    create_initial_commit
    create_ci_config
    create_release_config
    create_badges
    create_github_repo_suggestions
    
    echo ""
    echo "🎉 GitHub 仓库设置完成！"
    echo ""
    echo "📋 下一步操作:"
    echo "1. 按照上述建议在 GitHub 创建仓库"
    echo "2. 推送代码到远程仓库"
    echo "3. 配置 CI/CD 和发布流程"
    echo "4. 开始开发 v0.1.0 MVP"
    echo ""
    echo "🚀 让我们开始打造 Starlight 的未来！"
}

# 运行主函数
main "$@"
