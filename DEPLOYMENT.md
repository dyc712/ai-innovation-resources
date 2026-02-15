# 📦 部署到GitHub完整指南

本文档提供将本地仓库部署到GitHub的完整步骤。

---

## 🎯 前提条件

### 1. GitHub账号
- 确保已有GitHub账号：dongyunchuan@gmail.com
- 如果还没有，访问 https://github.com/signup 注册

### 2. Git配置
```bash
# 检查Git配置
git config --list

# 如果还没配置，运行：
git config --global user.name "Yunchuan Dong"
git config --global user.email "dongyunchuan@gmail.com"
```

### 3. GitHub认证
选择以下任一方式：

#### 方式A：Personal Access Token（推荐）
```bash
# 1. 生成Token
# 访问：https://github.com/settings/tokens/new
# 勾选：repo（所有权限）
# 点击：Generate token
# 复制保存token

# 2. 使用Token推送
git push https://TOKEN@github.com/dongyunchuan/ai-innovation-resources.git main
```

#### 方式B：SSH Key
```bash
# 1. 生成SSH密钥
ssh-keygen -t ed25519 -C "dongyunchuan@gmail.com"

# 2. 添加到GitHub
cat ~/.ssh/id_ed25519.pub
# 复制输出，添加到：https://github.com/settings/keys

# 3. 测试连接
ssh -T git@github.com
```

#### 方式C：GitHub CLI（最简单）
```bash
# 1. 安装GitHub CLI
brew install gh

# 2. 登录
gh auth login

# 3. 使用gh创建仓库（见下文）
```

---

## 🚀 部署步骤

### 步骤1：在GitHub创建仓库

#### 方法A：使用GitHub CLI（推荐）
```bash
cd ~/ai-innovation-resources

# 创建公开仓库并推送
gh repo create ai-innovation-resources \
  --public \
  --source=. \
  --remote=origin \
  --push
```

#### 方法B：手动在GitHub网页创建
1. 访问 https://github.com/new
2. 填写信息：
   - **Repository name**: `ai-innovation-resources`
   - **Description**: `AI创新资源团队共享库 - 收集整理AI模型、工具、教程等优质资源`
   - **Public**: 勾选（公开仓库）
   - **不要勾选**: Initialize this repository with...
3. 点击 "Create repository"

### 步骤2：连接远程仓库（如果手动创建）

```bash
cd ~/ai-innovation-resources

# 添加远程仓库
git remote add origin https://github.com/dongyunchuan/ai-innovation-resources.git

# 或使用SSH
git remote add origin git@github.com:dongyunchuan/ai-innovation-resources.git

# 验证
git remote -v
```

### 步骤3：推送代码

```bash
# 确认分支名
git branch -M main

# 推送到GitHub
git push -u origin main

# 如果推送失败，可能需要：
# 1. 使用Token：
git push https://YOUR_TOKEN@github.com/dongyunchuan/ai-innovation-resources.git main

# 2. 或配置凭证缓存：
git config --global credential.helper cache
git push -u origin main
# 输入GitHub用户名和Token
```

### 步骤4：验证部署

```bash
# 访问仓库
open https://github.com/dongyunchuan/ai-innovation-resources

# 检查内容
# - README.md应正确显示
# - 目录结构完整
# - 文件无遗漏
```

---

## 👥 配置团队协作

### 1. 添加协作者

```bash
# 使用GitHub CLI
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  /repos/dongyunchuan/ai-innovation-resources/collaborators/USERNAME \
  -f permission='push'

# 或在网页操作：
# Settings → Access → Collaborators → Add people
```

### 2. 设置分支保护规则

访问：`https://github.com/dongyunchuan/ai-innovation-resources/settings/branches`

建议规则：
- ✅ Require pull request reviews before merging
- ✅ Require status checks to pass before merging
- ✅ Require branches to be up to date before merging

### 3. 配置Issue和PR模板

模板已在 `.github/ISSUE_TEMPLATE/` 目录中，GitHub会自动识别。

---

## 🔧 启用自动化功能

### 1. 启用GitHub Actions

```bash
# 访问 Actions 标签页
open https://github.com/dongyunchuan/ai-innovation-resources/actions

# 点击 "I understand my workflows, go ahead and enable them"
```

### 2. 设置仓库描述和主题

```bash
# 使用GitHub CLI
gh repo edit \
  --description "AI创新资源团队共享库 - AI模型、工具、教程精选" \
  --homepage "https://github.com/dongyunchuan/ai-innovation-resources" \
  --add-topic ai \
  --add-topic resources \
  --add-topic llm \
  --add-topic machine-learning \
  --add-topic tutorial

# 或在网页操作：
# Settings → General → Description and Topics
```

### 3. 配置GitHub Pages（可选）

如果想创建网站展示：

```bash
# 使用GitHub CLI
gh api \
  --method POST \
  -H "Accept: application/vnd.github+json" \
  /repos/dongyunchuan/ai-innovation-resources/pages \
  -f "source[branch]=main" \
  -f "source[path]=/"

# 或在网页：
# Settings → Pages → Source → Deploy from a branch → main → / (root)
```

访问：https://dongyunchuan.github.io/ai-innovation-resources/

---

## 📱 日常维护

### 更新远程仓库

```bash
cd ~/ai-innovation-resources

# 拉取最新更改
git pull origin main

# 添加新资源
# ... 编辑文件 ...

# 提交更改
git add .
git commit -m "添加：XXX资源"
git push origin main
```

### 同步Fork仓库（团队成员）

```bash
# 添加上游仓库
git remote add upstream https://github.com/dongyunchuan/ai-innovation-resources.git

# 同步最新代码
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

---

## 🔐 安全最佳实践

### 1. 保护敏感信息

```bash
# 添加到.gitignore
echo "*.env" >> .gitignore
echo "secrets/" >> .gitignore
echo "*.key" >> .gitignore

git add .gitignore
git commit -m "更新：.gitignore规则"
```

### 2. 定期审计

```bash
# 检查历史提交中的敏感信息
git log --all --full-history --source -- '*password*'

# 如果发现敏感信息，使用git filter-branch清理
```

### 3. 启用Dependabot（自动依赖更新）

访问：Settings → Security → Dependabot

---

## 📊 监控和分析

### 1. 启用Insights

访问：https://github.com/dongyunchuan/ai-innovation-resources/pulse

查看：
- Contributors（贡献者）
- Traffic（访问量）
- Commits（提交历史）

### 2. 设置Webhooks（可选）

如果需要集成企业微信或其他工具：

Settings → Webhooks → Add webhook

---

## 🐛 常见问题

### Q1: 推送失败：Authentication failed

**解决**：
```bash
# 使用Personal Access Token
git remote set-url origin https://TOKEN@github.com/dongyunchuan/ai-innovation-resources.git
git push -u origin main
```

### Q2: 文件太大无法推送

**解决**：
```bash
# 使用Git LFS（大文件存储）
brew install git-lfs
git lfs install
git lfs track "*.psd"
git lfs track "*.zip"
git add .gitattributes
git commit -m "添加：Git LFS配置"
```

### Q3: 提交历史混乱

**解决**：
```bash
# 使用Rebase整理提交历史
git rebase -i HEAD~5
# 按提示合并或编辑提交信息
```

### Q4: 不小心提交了敏感信息

**解决**：
```bash
# 从历史中完全删除文件
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/sensitive/file" \
  --prune-empty --tag-name-filter cat -- --all

# 强制推送（谨慎！）
git push origin --force --all
```

---

## ✅ 部署检查清单

部署完成后，检查以下项：

- [ ] 仓库已创建并设为Public
- [ ] 本地代码成功推送
- [ ] README正确显示
- [ ] 目录结构完整
- [ ] Actions已启用
- [ ] 添加了仓库描述和主题标签
- [ ] 邀请了团队协作者
- [ ] 设置了分支保护规则（可选）
- [ ] 创建了第一个Issue或讨论
- [ ] 在企业微信群分享了仓库链接

---

## 📞 需要帮助？

- GitHub文档：https://docs.github.com/
- GitHub CLI文档：https://cli.github.com/manual/
- 本项目讨论：https://github.com/dongyunchuan/ai-innovation-resources/discussions

---

## 🎉 完成！

恭喜！您已成功将AI创新资源库部署到GitHub！

**下一步**：
1. 分享仓库链接给团队成员
2. 鼓励大家添加第一个资源
3. 在企业微信群置顶仓库链接
4. 开始你的协作之旅！

Happy Coding! 🚀
