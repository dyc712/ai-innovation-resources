# 🚀 快速开始指南

本指南帮助您快速了解如何使用和贡献AI创新资源共享库。

---

## 📖 第一步：创建GitHub仓库

### 1. 在GitHub上创建新仓库

```bash
# 方式一：使用GitHub CLI（推荐）
gh repo create ai-innovation-resources --public --source=. --remote=origin

# 方式二：手动在GitHub网页创建
# 1. 访问 https://github.com/new
# 2. 仓库名：ai-innovation-resources
# 3. 描述：AI创新资源团队共享库
# 4. 选择：Public（公开）
# 5. 不要勾选 "Initialize this repository with..."
# 6. 点击 "Create repository"
```

### 2. 推送本地代码到GitHub

```bash
cd ~/ai-innovation-resources

# 添加远程仓库（如果还没添加）
git remote add origin https://github.com/dongyunchuan/ai-innovation-resources.git

# 推送代码
git branch -M main
git push -u origin main
```

---

## 👥 第二步：邀请团队成员

### 添加协作者（Collaborators）

1. 进入仓库设置页面：
   ```
   https://github.com/dongyunchuan/ai-innovation-resources/settings/access
   ```

2. 点击 "Add people"

3. 输入团队成员的GitHub用户名或邮箱

4. 选择权限级别：
   - **Write**：可以直接推送代码（推荐给核心成员）
   - **Maintain**：可以管理Issue和PR
   - **Admin**：完全管理权限

### 团队成员接受邀请

团队成员会收到邮件通知，点击链接接受邀请即可。

---

## 📝 第三步：提交第一个资源

### 方式一：直接编辑（有权限者）

```bash
# 1. 克隆仓库
git clone https://github.com/dongyunchuan/ai-innovation-resources.git
cd ai-innovation-resources

# 2. 创建资源文件（使用模板）
cp templates/resource-template.md "01-模型与研究/开源模型/Claude-Opus-4.6-评测.md"

# 3. 编辑资源文件，填写内容
# ... 编辑 ...

# 4. 更新对应目录的README.md索引

# 5. 提交更改
git add .
git commit -m "添加：Claude Opus 4.6 模型评测"
git push
```

### 方式二：Fork + Pull Request

```bash
# 1. Fork仓库到自己账号（在GitHub网页操作）

# 2. 克隆你Fork的仓库
git clone https://github.com/YOUR_USERNAME/ai-innovation-resources.git
cd ai-innovation-resources

# 3. 创建新分支
git checkout -b add-claude-review

# 4. 添加资源文件

# 5. 提交并推送
git add .
git commit -m "添加：Claude Opus 4.6 评测"
git push origin add-claude-review

# 6. 在GitHub上创建Pull Request
```

---

## 🔧 第四步：启用自动化功能

### 启用GitHub Actions

1. 进入仓库 "Actions" 标签页
2. 如果看到提示，点击 "I understand my workflows, go ahead and enable them"
3. Actions会在每次推送后自动运行，更新资源索引

### 设置GitHub Pages（可选）

如果想要创建网站展示：

1. 进入 Settings → Pages
2. Source 选择 "Deploy from a branch"
3. Branch 选择 "main" 和 "/ (root)"
4. 点击 Save

几分钟后即可通过以下地址访问：
```
https://dongyunchuan.github.io/ai-innovation-resources/
```

---

## 📱 第五步：日常使用

### 查看资源

```bash
# 浏览GitHub仓库
https://github.com/dongyunchuan/ai-innovation-resources

# 使用搜索功能（快捷键：/）
# 搜索示例："LangChain" "教程" "Claude"

# 查看分类目录
01-模型与研究/
02-工具与平台/
...
```

### 贡献资源

```bash
# 方式1：直接提交PR
git clone → 编辑 → commit → push → PR

# 方式2：创建Issue
访问: https://github.com/dongyunchuan/ai-innovation-resources/issues/new/choose
选择"资源提交"模板

# 方式3：在线编辑（小修改）
直接在GitHub网页点击文件的"编辑"按钮
```

### 订阅更新

```bash
# 在GitHub仓库页面点击 "Watch"
Custom → 选择通知类型：
- ✅ Releases（发布）
- ✅ Discussions（讨论）
- ✅ Issues（问题）
- ✅ Pull requests（PR）
```

---

## 💡 使用技巧

### 1. 快速查找资源

```bash
# GitHub搜索语法
is:markdown Claude                    # 搜索Markdown文件
path:01-模型与研究/ LLM              # 在指定目录搜索
created:>2026-02-01                   # 搜索最近创建的
```

### 2. 批量添加资源

```bash
# 使用脚本批量转换
python scripts/import-resources.py --source urls.txt --output 01-模型与研究/
```

### 3. 本地预览Markdown

```bash
# 使用VS Code
code ai-innovation-resources/

# 安装推荐插件后按 Cmd+Shift+V 预览
```

### 4. 同步最新代码

```bash
# 如果是Fork的仓库
git remote add upstream https://github.com/dongyunchuan/ai-innovation-resources.git
git fetch upstream
git merge upstream/main
```

---

## 🎯 最佳实践

### ✅ 推荐做法

1. **使用模板**：统一格式，便于检索
2. **详细描述**：包含简介、亮点、适用场景
3. **有效链接**：确保链接可访问
4. **及时更新**：资源过时后及时标注或删除
5. **添加标签**：便于分类和搜索

### ❌ 避免事项

1. 不要提交商业广告
2. 不要重复添加相同资源
3. 不要上传大文件（使用链接代替）
4. 不要包含敏感信息
5. 不要直接修改他人提交的内容（通过PR讨论）

---

## 📞 获取帮助

- **文档**：查看 [CONTRIBUTING.md](CONTRIBUTING.md)
- **问题**：创建 [Issue](https://github.com/dongyunchuan/ai-innovation-resources/issues)
- **讨论**：参与 [Discussions](https://github.com/dongyunchuan/ai-innovation-resources/discussions)
- **联系**：dongyunchuan@gmail.com

---

## 🎉 完成！

现在您已经完全掌握了如何使用AI创新资源共享库！

**下一步**：
- [ ] 添加第一个资源
- [ ] 邀请团队成员
- [ ] 在企业微信群分享仓库链接
- [ ] 设置自动化工作流

Happy Sharing! 🚀
