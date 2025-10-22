#!/bin/bash

echo "🚀 === Starlight 推送到 GitHub ==="
echo ""
echo "仓库地址: https://github.com/richardcookedanytime/StarLightOfficial"
echo ""

# 检查远程仓库
echo "📊 当前配置:"
git remote -v
echo ""

# 显示状态
echo "📝 Git 状态:"
git status
echo ""

# 显示最近提交
echo "📋 最近的提交:"
git log --oneline -3
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "准备推送到 GitHub..."
echo ""
echo "⚠️  重要提示:"
echo "1. GitHub 不再接受密码认证"
echo "2. 你需要使用 Personal Access Token (PAT)"
echo "3. 获取 Token: https://github.com/settings/tokens"
echo "4. 推送时使用 Token 作为密码"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

read -p "按 Enter 继续推送..." 

echo ""
echo "🚀 开始推送..."
echo ""

# 推送
git push -u origin master

if [ $? -eq 0 ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🎉 推送成功！"
    echo ""
    echo "📋 下一步:"
    echo "1. 访问仓库: https://github.com/richardcookedanytime/StarLightOfficial"
    echo "2. 查看代码和文件"
    echo "3. 添加仓库描述和 Topics"
    echo "4. 启用 GitHub Actions"
    echo "5. 创建第一个 Release"
    echo ""
    echo "📊 推送统计:"
    echo "- 49 个文件"
    echo "- 7,835+ 行代码"
    echo "- 包含完整的编译器实现"
    echo ""
    echo "✨ Starlight 已经在 GitHub 上线！"
    echo ""
else
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "❌ 推送失败"
    echo ""
    echo "可能的原因:"
    echo "1. 认证失败 - 请使用 Personal Access Token"
    echo "2. 网络问题 - 请检查网络连接"
    echo "3. 权限问题 - 请确认有推送权限"
    echo ""
    echo "解决方法:"
    echo ""
    echo "方法 1: 使用 Personal Access Token (PAT)"
    echo "  1. 访问: https://github.com/settings/tokens"
    echo "  2. 生成新 token (勾选 'repo' 权限)"
    echo "  3. 复制 token"
    echo "  4. 再次运行此脚本，使用 token 作为密码"
    echo ""
    echo "方法 2: 使用 SSH"
    echo "  1. 生成 SSH 密钥: ssh-keygen -t ed25519"
    echo "  2. 添加到 GitHub: https://github.com/settings/keys"
    echo "  3. 更新远程 URL:"
    echo "     git remote set-url origin git@github.com:richardcookedanytime/StarLightOfficial.git"
    echo "  4. 再次推送"
    echo ""
    echo "方法 3: 使用 GitHub CLI"
    echo "  1. 安装: brew install gh"
    echo "  2. 登录: gh auth login"
    echo "  3. 推送: git push -u origin master"
    echo ""
    echo "详细说明请查看: PUSH_INSTRUCTIONS.md"
    echo ""
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

