# AI创新报告自动生成配置

## 📋 目录说明

### scripts/
脚本文件：
- `sync_ai_report_to_git.py` - 报告自动同步到GitHub
- `generate_poster.py` - 生成精美海报（PPTX格式）

### docs/
配置文档：
- `AI创新日报_Prompt优化方案.md` - Prompt优化说明

---

## 🚀 快速开始

### 1. 报告生成流程

定时任务自动生成报告：
- **执行时间**：每天早上8:00
- **Cron表达式**：`0 8 * * *`
- **任务ID**：`52c8bec1-0a70-42c5-8f60-6090636b029d`

### 2. 报告内容（5大模块）

1. **核心摘要** - 一句话精炼
2. **模型与研究深度** - SOTA前沿
3. **工具与产品实践** - 落地应用
4. **开发者与生态** - 社区动态
5. **宏观与商业观察** - 商业洞察

### 3. 四维过滤器

- 技术前沿度（SOTA & Research）
- 落地可行性（Feasibility）
- 工具效率比（Productivity）
- 行业渗透率（Industry Impact）

---

## 📊 信息渠道

- X/Twitter
- Reddit
- GitHub Trending
- Hugging Face
- ArXiv
- Product Hunt

---

## 📁 文件输出

### Markdown报告
- 路径：`/data/workspace/ai_innovation_reports/`
- 格式：`AI创新报告_YYYY-MM-DD.md`

### PPTX海报
- 路径：同Markdown
- 格式：`AI创新报告_YYYY-MM-DD_海报.pptx`
- 配色：Ocean Gradient

---

## 🔄 自动同步GitHub

报告生成后自动运行 `sync_ai_report_to_git.py`：
- 仓库：https://github.com/dyc712/ai-innovation-resources
- 路径：`07-团队分享/AI创新报告/YYYY-MM/`
- 状态：✅ 已测试成功（2026-02-24）

---

## 📞 通知机制

- 渠道：企业微信「Knot消息通知」机器人
- 触发：报告生成错误或GitHub同步失败

---

📅 **最后更新**: 2026-02-25
