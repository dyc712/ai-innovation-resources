# 🚀 AI创新资源库 - 团队协作指南

## 📋 仓库状态检查结果

### ✅ 本地仓库状态
- **位置**：`/Users/dongyunchuan/ai-innovation-resources`
- **Git初始化**：✅ 已完成
- **提交历史**：✅ 4个commits
- **分支**：main
- **远程仓库**：❌ 尚未推送到GitHub

### ❌ GitHub仓库状态
经检查以下GitHub账号，**仓库尚未创建**：
- https://github.com/dongyunchuan (404)
- https://github.com/dongyunchuan712 (404)

**需要立即执行**：将本地仓库推送到GitHub

---

## 🎯 第一步：创建GitHub仓库（管理员操作）

### 方案A：使用GitHub CLI（推荐，最快）

```bash
cd ~/ai-innovation-resources

# 1. 安装GitHub CLI（如果还没有）
brew install gh

# 2. 登录GitHub（使用 dongyunchuan@gmail.com 或 dongyunchuan712@gmail.com）
gh auth login
# 选择：GitHub.com → HTTPS → 登录浏览器 → 输入验证码

# 3. 创建仓库并推送（一键完成）
gh repo create ai-innovation-resources \
  --public \
  --source=. \
  --remote=origin \
  --description "AI创新资源团队共享库 - AI模型、工具、教程精选" \
  --push

# 4. 添加主题标签
gh repo edit --add-topic ai --add-topic resources --add-topic llm \
  --add-topic machine-learning --add-topic tutorial --add-topic knowledge-base

# 5. 验证创建成功
gh repo view --web
```

### 方案B：手动在GitHub网页创建

```bash
# 1. 访问 https://github.com/new 创建仓库
```

填写信息：
- **Owner**: dongyunchuan 或 dongyunchuan712（根据您的实际账号）
- **Repository name**: `ai-innovation-resources`
- **Description**: `AI创新资源团队共享库 - 收集整理AI模型、工具、教程等优质资源`
- **Visibility**: ✅ Public（公开仓库）
- **Initialize**: ❌ 不要勾选任何初始化选项（README、gitignore等）

点击 **"Create repository"**

```bash
# 2. 推送本地代码到GitHub
cd ~/ai-innovation-resources

# 添加远程仓库（替换USERNAME为实际账号）
git remote add origin https://github.com/USERNAME/ai-innovation-resources.git

# 推送代码
git branch -M main
git push -u origin main

# 如果提示需要认证，使用Personal Access Token：
# 访问 https://github.com/settings/tokens/new 生成Token
# 权限勾选：repo（所有）
# 然后使用Token推送：
git push https://YOUR_TOKEN@github.com/USERNAME/ai-innovation-resources.git main
```

---

## 👥 第二步：获取Git地址（分享给团队）

### 仓库创建成功后，获取Git地址

#### HTTPS地址（推荐）
```
https://github.com/USERNAME/ai-innovation-resources.git
```

#### SSH地址（需配置SSH Key）
```
git@github.com:USERNAME/ai-innovation-resources.git
```

### 分享给团队的信息模板

复制以下内容发送到企业微信群：

```
📢 团队公告：AI创新资源共享库已上线！

🔗 仓库地址：
https://github.com/USERNAME/ai-innovation-resources

📥 克隆命令：
git clone https://github.com/USERNAME/ai-innovation-resources.git

📚 文档目录：
- README.md - 项目说明
- QUICKSTART.md - 快速开始
- CONTRIBUTING.md - 贡献指南
- DEPLOYMENT.md - 部署说明

✅ 已配置功能：
✓ 自动索引生成（GitHub Actions）
✓ 资源提交模板
✓ Issue提交表单
✓ 6大分类目录
✓ 示例资源（Claude Opus 4.6）

💡 如何使用：
1. 查看资源：直接访问仓库浏览
2. 提交资源：Fork → 编辑 → PR 或 创建Issue
3. 订阅更新：点击仓库右上角 "Watch"

🤝 权限申请：
需要直接推送权限的同事，请提供GitHub用户名

欢迎大家贡献优质AI资源！🚀
```

---

## 🔧 第三步：OpenClaw配置Git自动上传

### 方案1：使用Git作为OpenClaw的文档存储目录

```bash
# 1. 将OpenClaw工作目录切换到Git仓库的某个子目录
cd ~/ai-innovation-resources

# 2. 创建OpenClaw专用目录
mkdir -p 07-团队分享/OpenClaw文档
mkdir -p 07-团队分享/每日报告

# 3. 在OpenClaw中配置默认保存路径
# 如果OpenClaw支持配置默认目录，设置为：
# /Users/dongyunchuan/ai-innovation-resources/07-团队分享/OpenClaw文档
```

### 方案2：配置自动同步脚本

创建自动Git提交脚本：

```bash
# 创建自动同步脚本
cat > ~/ai-innovation-resources/scripts/auto-sync.sh << 'EOF'
#!/bin/bash
# AI创新资源库 - 自动同步脚本

cd ~/ai-innovation-resources

# 拉取最新更改
git pull origin main

# 添加所有更改
git add .

# 检查是否有更改
if git diff --staged --quiet; then
  echo "📊 无新内容需要同步"
  exit 0
fi

# 提交更改（使用时间戳）
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
git commit -m "自动同步: $TIMESTAMP"

# 推送到远程
git push origin main

echo "✅ 同步完成: $TIMESTAMP"
EOF

# 添加执行权限
chmod +x ~/ai-innovation-resources/scripts/auto-sync.sh

# 测试运行
~/ai-innovation-resources/scripts/auto-sync.sh
```

### 方案3：配置定时自动同步（可选）

```bash
# 使用crontab配置定时任务
# 每小时自动同步一次
crontab -e

# 添加以下行：
0 * * * * ~/ai-innovation-resources/scripts/auto-sync.sh >> ~/ai-innovation-resources/logs/sync.log 2>&1

# 或每30分钟同步：
*/30 * * * * ~/ai-innovation-resources/scripts/auto-sync.sh >> ~/ai-innovation-resources/logs/sync.log 2>&1
```

### 方案4：OpenClaw保存后手动触发同步

创建快速同步命令：

```bash
# 添加到 ~/.zshrc 或 ~/.bashrc
echo 'alias git-sync="cd ~/ai-innovation-resources && git add . && git commit -m \"更新: \$(date +%Y-%m-%d\ %H:%M)\" && git push origin main && cd -"' >> ~/.zshrc

# 重新加载配置
source ~/.zshrc

# 使用方法：OpenClaw保存文件后，在终端输入
git-sync
```

---

## 📝 团队成员使用指南

### 团队成员克隆仓库

```bash
# 1. 克隆仓库到本地
git clone https://github.com/USERNAME/ai-innovation-resources.git
cd ai-innovation-resources

# 2. 查看现有资源
ls -la
cat README.md

# 3. 配置Git用户信息
git config user.name "你的名字"
git config user.email "your-email@example.com"
```

### 贡献资源的三种方式

#### 方式1：直接推送（需要Collaborator权限）

```bash
# 1. 拉取最新代码
git pull origin main

# 2. 添加资源文件
cp templates/resource-template.md "01-模型与研究/开源模型/新资源.md"
# 编辑文件...

# 3. 提交并推送
git add .
git commit -m "添加：XXX资源"
git push origin main
```

#### 方式2：Fork + Pull Request

```bash
# 1. 在GitHub网页Fork仓库
# 2. 克隆你的Fork
git clone https://github.com/YOUR_USERNAME/ai-innovation-resources.git
cd ai-innovation-resources

# 3. 创建功能分支
git checkout -b add-new-resource

# 4. 添加资源
# ... 编辑文件 ...

# 5. 提交并推送到你的Fork
git add .
git commit -m "添加：XXX资源"
git push origin add-new-resource

# 6. 在GitHub网页创建Pull Request
```

#### 方式3：通过Issue提交

访问：https://github.com/USERNAME/ai-innovation-resources/issues/new/choose

选择"资源提交"模板，填写表单

---

## 🔐 权限管理

### 添加团队协作者（管理员操作）

#### 使用GitHub CLI

```bash
# 添加单个协作者（Write权限）
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  /repos/USERNAME/ai-innovation-resources/collaborators/TEAMMATE_USERNAME \
  -f permission='push'

# 批量添加多个协作者
for user in user1 user2 user3; do
  gh api \
    --method PUT \
    -H "Accept: application/vnd.github+json" \
    /repos/USERNAME/ai-innovation-resources/collaborators/$user \
    -f permission='push'
done
```

#### 使用GitHub网页

1. 访问：`https://github.com/USERNAME/ai-innovation-resources/settings/access`
2. 点击 **"Collaborators" → "Add people"**
3. 输入团队成员的GitHub用户名
4. 选择权限级别：
   - **Read**：只读
   - **Write**：推送权限（推荐）
   - **Admin**：完全管理

### 权限说明

| 角色 | 权限 | 适用对象 |
|-----|------|---------|
| **Owner** | 完全控制 | 仓库创建者 |
| **Admin** | 管理仓库 | 核心管理员 |
| **Write** | 推送代码 | 活跃贡献者 |
| **Read** | 只读访问 | 所有人（Public仓库） |

---

## 🎯 OpenClaw工作流程建议

### 每日报告自动上传到Git

修改您的定时任务脚本，在生成报告后自动提交：

```python
# 在generate-index.py或报告生成脚本末尾添加
import subprocess
from datetime import datetime

def auto_commit_to_git(report_path):
    """自动提交报告到Git"""
    try:
        # 切换到Git目录
        os.chdir('/Users/dongyunchuan/ai-innovation-resources')
        
        # 拉取最新
        subprocess.run(['git', 'pull', 'origin', 'main'], check=True)
        
        # 添加文件
        subprocess.run(['git', 'add', '.'], check=True)
        
        # 提交
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        subprocess.run(['git', 'commit', '-m', f'自动更新: AI创新报告 {timestamp}'], check=True)
        
        # 推送
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print(f"✅ 报告已自动上传到GitHub")
        return True
    except Exception as e:
        print(f"❌ Git提交失败: {e}")
        return False

# 在报告生成后调用
if report_generated:
    auto_commit_to_git(report_path)
```

### 目录结构建议

```
ai-innovation-resources/
├── 07-团队分享/              # 新增：团队分享目录
│   ├── AI创新报告/
│   │   ├── 2026-02/
│   │   │   ├── AI创新报告_2026-02-15.md
│   │   │   └── AI创新报告_2026-02-15_海报.pptx
│   │   └── README.md
│   ├── 市场投资洞察/
│   │   ├── 2026-02/
│   │   │   └── 市场投资洞察报告_2026-02-14.docx
│   │   └── README.md
│   └── OpenClaw文档/
│       └── README.md
```

---

## 📞 支持与帮助

### 常见问题

**Q1: 推送失败，提示认证错误？**
```bash
# 解决方案：使用Personal Access Token
# 1. 生成Token: https://github.com/settings/tokens/new
# 2. 勾选 repo 权限
# 3. 使用Token推送
git push https://TOKEN@github.com/USERNAME/ai-innovation-resources.git main
```

**Q2: 如何撤销错误的提交？**
```bash
# 撤销最后一次提交（保留修改）
git reset --soft HEAD~1

# 撤销并丢弃修改
git reset --hard HEAD~1
```

**Q3: 多人同时编辑冲突了怎么办？**
```bash
# 拉取最新代码
git pull origin main

# 如果有冲突，手动解决冲突文件
# 然后提交
git add .
git commit -m "解决冲突"
git push origin main
```

**Q4: OpenClaw如何自动同步到Git？**

使用上面提供的自动同步脚本，或配置crontab定时任务。

### 联系方式

- **项目管理员**：dongyunchuan@gmail.com
- **GitHub Issue**：https://github.com/USERNAME/ai-innovation-resources/issues
- **企业微信群**：AI创新资源分享群

---

## ✅ 快速检查清单

部署完成后，请确认：

- [ ] GitHub仓库已创建
- [ ] 本地代码已推送
- [ ] 远程仓库可访问
- [ ] README正确显示
- [ ] Actions已启用
- [ ] 团队成员已邀请
- [ ] Git地址已分享到群
- [ ] OpenClaw同步脚本已配置
- [ ] 测试提交成功
- [ ] 团队成员已测试克隆

---

<div align="center">

**📢 完成以上步骤后，在企业微信群置顶仓库链接！**

🚀 开始团队协作之旅！

</div>
