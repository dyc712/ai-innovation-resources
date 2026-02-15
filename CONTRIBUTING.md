# 贡献指南

感谢您对AI创新资源共享库的贡献！本文档将帮助您了解如何参与贡献。

---

## 🎯 贡献方式

### 1. 添加新资源

我们欢迎以下类型的资源：
- ✅ 开源AI模型及使用指南
- ✅ 优质技术论文及解读
- ✅ 实用开发工具与框架
- ✅ 高质量教程与最佳实践
- ✅ 行业分析报告与案例研究
- ✅ 优质技术社区与开源项目

### 2. 改进现有内容

- 更新过时信息
- 补充遗漏的资源链接
- 修正错误或笔误
- 优化内容组织结构

### 3. 维护与管理

- 审核其他成员的PR
- 整理和归档资源
- 更新目录索引

---

## 📝 提交流程

### 标准流程（推荐）

#### 步骤1：Fork仓库

点击仓库右上角的 "Fork" 按钮，将仓库复制到你的GitHub账号下。

#### 步骤2：克隆到本地

```bash
git clone https://github.com/YOUR_USERNAME/ai-innovation-resources.git
cd ai-innovation-resources
```

#### 步骤3：添加上游仓库

```bash
git remote add upstream https://github.com/dongyunchuan/ai-innovation-resources.git
```

#### 步骤4：创建新分支

```bash
# 同步最新代码
git fetch upstream
git checkout main
git merge upstream/main

# 创建功能分支（命名规范见下文）
git checkout -b feature/add-claude-opus-review
```

#### 步骤5：添加资源

1. **选择合适的目录**
   ```
   例如：添加模型评测 → 01-模型与研究/开源模型/
   ```

2. **使用模板创建文件**
   ```bash
   cp templates/resource-template.md "01-模型与研究/开源模型/Claude-Opus-4.6-评测.md"
   ```

3. **填写资源信息**（参考模板格式）

4. **更新目录索引**
   编辑对应目录的 `README.md`，添加资源条目

#### 步骤6：提交更改

```bash
# 查看更改
git status

# 添加文件
git add .

# 提交（遵循提交信息规范）
git commit -m "添加：Claude Opus 4.6 模型评测报告"
```

#### 步骤7：推送到你的仓库

```bash
git push origin feature/add-claude-opus-review
```

#### 步骤8：创建Pull Request

1. 访问你Fork的仓库页面
2. 点击 "Compare & pull request"
3. 填写PR描述（使用PR模板）
4. 提交PR等待审核

---

## 📋 规范要求

### 分支命名规范

```
feature/功能描述      # 添加新功能或资源
fix/问题描述         # 修复错误
docs/文档描述        # 文档更新
refactor/重构描述    # 代码或内容重构
```

**示例**：
- `feature/add-qwen3.5-tutorial`
- `fix/broken-link-in-readme`
- `docs/update-contributing-guide`

### 提交信息规范

使用以下前缀：
- `添加：` 新增资源或内容
- `更新：` 更新现有内容
- `修复：` 修复错误
- `删除：` 删除过时内容
- `重构：` 重新组织内容结构

**示例**：
```
添加：Qwen 3.5 多模态模型使用教程
更新：GLM-5 模型性能测试数据
修复：ArXiv论文链接失效问题
```

### 文件命名规范

- **使用中文**：`Claude-Opus-4.6-评测报告.md`
- **连字符分隔**：单词间用 `-` 连接
- **避免特殊字符**：不使用 `/ \ : * ? " < > |`
- **有意义的名称**：能清楚表达内容主题

### 内容格式规范

#### Markdown格式要求

```markdown
# 一级标题（资源名称）

## 二级标题（章节）

### 三级标题（小节）

- 使用无序列表
1. 使用有序列表

**加粗重点内容**
*斜体强调*

[链接文字](https://example.com)

![图片描述](图片URL)
```

#### 资源信息完整性

每个资源文件必须包含：
- ✅ 资源名称
- ✅ 类型标签
- ✅ 简介（100-200字）
- ✅ 核心亮点
- ✅ 资源链接
- ✅ 推荐指数
- ✅ 提交者和时间

---

## 🔍 质量标准

### 资源质量要求

#### ✅ 高质量资源特征
- 来源可靠（官方、知名机构、技术大牛）
- 内容准确、时效性强
- 实用价值高
- 有清晰的使用说明
- 活跃维护（对于工具和项目）

#### ❌ 不接受的资源
- 商业广告或营销内容
- 低质量或抄袭内容
- 违反法律法规的内容
- 侵犯版权的资源
- 恶意链接或钓鱼网站

### 内容审核标准

贡献的内容会经过以下检查：
1. **格式检查**：Markdown语法、目录结构
2. **链接检查**：确保链接有效
3. **重复检查**：避免重复资源
4. **质量评估**：内容价值和准确性
5. **许可检查**：版权和许可协议

---

## 👥 审核流程

### PR审核流程

1. **自动检查**（GitHub Actions）
   - Markdown语法检查
   - 链接有效性测试
   - 文件命名规范检查

2. **人工审核**（至少1位维护者）
   - 内容质量评估
   - 分类准确性
   - 格式规范性

3. **反馈与修改**
   - 审核者提出修改建议
   - 贡献者根据反馈修改
   - 重新审核直到通过

4. **合并入库**
   - 审核通过后合并到main分支
   - 自动更新目录索引
   - 关闭相关Issue

### 审核时间

- 工作日PR通常在**24小时内**得到响应
- 复杂PR可能需要**2-3天**审核
- 紧急PR可以在企业微信群@维护者

---

## 🏆 贡献者权益

### 贡献者认可

- ✨ 名字出现在贡献者列表
- 🎖️ 获得对应徽章（Bronze/Silver/Gold Contributor）
- 📊 贡献统计展示在个人profile

### 晋升路径

| 等级 | 要求 | 权限 |
|-----|------|------|
| **Contributor** | 1个PR被合并 | - |
| **Active Contributor** | 5个PR被合并 | 优先审核 |
| **Core Contributor** | 20个PR + 3个月活跃 | Issue/PR管理权限 |
| **Maintainer** | 核心贡献者推荐 | 完全管理权限 |

---

## 🛠️ 工具支持

### 推荐工具

- **编辑器**：VS Code + Markdown插件
- **Git工具**：GitHub Desktop / GitKraken
- **格式检查**：markdownlint
- **链接检查**：markdown-link-check

### VS Code插件推荐

```json
{
  "recommendations": [
    "yzhang.markdown-all-in-one",
    "DavidAnson.vscode-markdownlint",
    "bierner.markdown-preview-github-styles"
  ]
}
```

---

## ❓ 常见问题

### Q1: 如何快速找到合适的目录？

**A**: 参考以下决策树：

```
是模型/论文? → 01-模型与研究/
是工具/框架? → 02-工具与平台/
是教程/案例? → 03-教程与实践/
是行业报告? → 04-行业洞察/
是社区资源? → 05-社区资源/
```

### Q2: 资源已经在其他分类，还要重复添加吗？

**A**: 不需要。可以在其他分类的README中添加交叉引用：

```markdown
另见：[Claude Opus 4.6评测](../01-模型与研究/开源模型/Claude-Opus-4.6-评测.md)
```

### Q3: 发现错误但不知道如何修复？

**A**: 创建Issue说明问题，由其他成员协助修复。

### Q4: PR被拒绝怎么办？

**A**: 查看审核意见，修改后重新提交。可以在PR评论区讨论。

### Q5: 想贡献但没有具体资源？

**A**: 可以：
- 审核其他PR
- 更新现有内容
- 整理目录索引
- 改进文档

---

## 📞 获取帮助

遇到问题？联系我们：

1. **GitHub Issues**：[提交问题](https://github.com/dongyunchuan/ai-innovation-resources/issues)
2. **GitHub Discussions**：[参与讨论](https://github.com/dongyunchuan/ai-innovation-resources/discussions)
3. **企业微信群**：团队内部沟通群
4. **邮件联系**：dongyunchuan@gmail.com

---

## 📚 参考资源

- [GitHub Guides](https://guides.github.com/)
- [Markdown指南](https://www.markdownguide.org/)
- [如何参与开源项目](https://opensource.guide/zh-hans/how-to-contribute/)

---

<div align="center">

**感谢你的贡献！让我们一起打造最优质的AI资源库！** 🚀

</div>
