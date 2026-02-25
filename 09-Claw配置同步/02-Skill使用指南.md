# 02 - Skill 使用指南

## 📋 已安装 Skill 清单

当前环境已安装 **14个 Skill**，涵盖文档处理、数据分析、内容生成等多个领域。

| Skill 名称 | 使用频率 | 主要用途 | 触发场景 |
|-----------|---------|---------|---------|
| **xlsx** | ⭐⭐⭐⭐⭐ | 表格处理 | 处理投资跟踪Excel |
| **docx** | ⭐⭐⭐⭐ | 文档创建 | 生成周度市场报告 |
| **pdf** | ⭐⭐⭐ | PDF处理 | 提取财报数据 |
| **pptx** | ⭐⭐⭐ | 演示文稿 | AI创新报告海报 |
| **web-fetch** | ⭐⭐⭐⭐ | 网页抓取 | 获取财经资讯 |
| **diagram-generator** | ⭐⭐ | 图表生成 | 绘制架构图 |
| **business-analytics-reporter** | ⭐⭐ | 业务分析 | 投资数据分析 |
| **finance-manager** | ⭐⭐ | 财务管理 | 个人财务追踪 |
| **ai-daily-brief** | ⭐⭐⭐ | AI资讯 | 自动生成AI日报 |
| **data-analyst** | ⭐⭐ | 数据分析 | CSV数据处理 |
| **humanizer-zh** | ⭐ | 文本润色 | 报告人性化处理 |
| **obsidian** | ⭐ | 笔记管理 | 知识库管理 |
| **weather** | ⭐ | 天气查询 | 获取天气信息 |
| **skill-creator** | ⭐ | Skill开发 | 创建新Skill |

---

## 📊 核心 Skill 详解

### 1. xlsx - 表格处理专家 ⭐⭐⭐⭐⭐

**描述**：处理 Excel 表格的首选 Skill，支持读取、编辑、创建、格式化等。

**主要用途**：
- 更新美股投资标的数据
- 处理 AH 股跟踪表格
- 生成投资分析报告

**使用场景**：
```
触发词：
- "更新 Excel 文件"
- "读取表格数据"
- "创建新的 xlsx 文件"
- "添加/修改列"
- "计算公式"
```

**实际应用**：
```python
# 定时任务中自动调用
# 文件：/data/workspace/scripts/update_stock_2.0_v4.py

import pandas as pd

# 读取现有数据
df = pd.read_excel('/data/workspace/stock_pool/美股投资标的_跟踪2.0.xlsx')

# 更新价格数据
df.loc[df['股票代码'] == 'AAPL', '最新价'] = 178.45

# 保存修改
df.to_excel('/data/workspace/stock_pool/美股投资标的_跟踪2.0.xlsx', index=False)
```

**最佳实践**：
- ✅ 处理大文件时使用分批读取
- ✅ 保存前先备份原文件
- ✅ 使用 openpyxl 引擎保留格式

---

### 2. docx - 文档创建大师 ⭐⭐⭐⭐

**描述**：创建、编辑和分析 Word 文档，支持格式化、批注、修订等。

**主要用途**：
- 生成周度市场投资洞察报告
- 创建投资分析文档
- 编辑和修订报告

**使用场景**：
```
触发词：
- "创建 Word 文档"
- "生成 docx 报告"
- "添加批注"
- "修订文档"
```

**实际应用**：
```python
# 在周度市场洞察任务中使用
# 定时任务ID: 9a475b86-17ee-4c82-bc98-14eee44063fa

from docx import Document

doc = Document()
doc.add_heading('市场投资洞察报告', 0)
doc.add_heading('一、宏观政策', 1)
doc.add_paragraph('本周美联储...')

doc.save('/data/workspace/weekly_market_insights/市场投资洞察报告_2026-02-25.docx')
```

**转换工具**：
```bash
# DOCX → Markdown
python3 /data/workspace/convert_docx_to_md.py 报告.docx
```

---

### 3. web-fetch - 网络数据猎手 ⭐⭐⭐⭐

**描述**：从 URL 获取并提取可读内容，将 HTML 转为 Markdown/文本。

**主要用途**：
- 抓取财经新闻
- 获取投行研报
- 采集 AI 技术文章

**使用场景**：
```
触发词：
- "获取网页内容"
- "抓取文章"
- "提取网页文本"
- "分析网页信息"
```

**实际应用**：
```python
# 在 AI 创新报告任务中使用
# 定时任务ID: 52c8bec1-0a70-42c5-8f60-6090636b029d

# 使用 web-fetch skill 获取内容
# 然后分析和提取关键信息
```

**最佳实践**：
- ✅ 设置合理的超时时间
- ✅ 处理请求失败的情况
- ✅ 遵守网站的 robots.txt

**替代方案**：
- 如需浏览器自动化，使用 `Agent Browser` skill
- 如需 JavaScript 渲染，使用 browser 工具

---

### 4. pptx - 演示文稿设计师 ⭐⭐⭐

**描述**：创建、编辑、读取 PowerPoint 文件，支持模板、布局、备注等。

**主要用途**：
- 生成 AI 创新报告海报
- 创建投资分析演示文稿
- 制作分享材料

**使用场景**：
```
触发词：
- "创建 PPT"
- "生成演示文稿"
- "制作海报"
- "添加幻灯片"
```

**实际应用**：
```python
# AI 创新报告海报生成
# 脚本：/data/workspace/scripts/generate_poster.py

from pptx import Presentation
from pptx.util import Inches

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[0])

title = slide.shapes.title
title.text = "AI创新报告 2026-02-25"

# 使用 Ocean Gradient 配色方案
# 保存海报
prs.save('/data/workspace/ai_innovation_reports/AI创新报告_2026-02-25_海报.pptx')
```

**配色方案**：Ocean Gradient
- 主色：#0077BE（深海蓝）
- 辅色：#00A8E8（天蓝）
- 强调色：#FFD700（金色）

---

### 5. pdf - PDF 处理专家 ⭐⭐⭐

**描述**：读取、提取、合并、分割、加密 PDF 文件。

**主要用途**：
- 提取上市公司财报数据
- 读取投资研究报告
- OCR 扫描文档

**使用场景**：
```
触发词：
- "读取 PDF"
- "提取 PDF 文本"
- "合并 PDF"
- "PDF 转文本"
```

**实际应用**：
```python
# 提取财报关键数据
import PyPDF2

with open('财报.pdf', 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    # 解析财务数据
    # ...
```

---

### 6. diagram-generator - 图表绘制专家 ⭐⭐

**描述**：生成和编辑多种类型的图表（draw.io、Mermaid、Excalidraw）。

**主要用途**：
- 绘制投资策略流程图
- 创建系统架构图
- 制作思维导图

**支持的图表类型**：
- 流程图（Flowchart）
- 序列图（Sequence Diagram）
- 类图（Class Diagram）
- ER图（Entity-Relationship）
- 思维导图（Mind Map）
- 架构图（Architecture）
- 网络拓扑（Network Topology）

**使用场景**：
```
触发词：
- "画流程图"
- "创建架构图"
- "生成思维导图"
- "绘制 ER 图"
```

**实际应用**：
```
# 在 Claw 对话中
"绘制美股投资决策流程图：
1. 数据采集（yfinance + 富途）
2. 指标计算（29个指标）
3. 评分排序
4. 执行优先级分类"
```

---

### 7. business-analytics-reporter - 业务分析师 ⭐⭐

**描述**：分析业务销售和收入数据，识别弱点，提供改进建议。

**主要用途**：
- 投资组合业绩分析
- 股票表现对比
- 收益率统计

**使用场景**：
```
触发词：
- "分析投资业绩"
- "生成业务报告"
- "识别弱点"
- "改进建议"
```

**实际应用**：
```
# 分析投资组合
"使用 business-analytics-reporter 分析我的美股投资组合业绩，
CSV文件路径：/data/workspace/portfolio_performance.csv"
```

---

### 8. finance-manager - 财务管理专家 ⭐⭐

**描述**：个人财务管理系统，分析交易数据，生成洞察和建议。

**主要用途**：
- 追踪投资支出
- 分析收益率
- 生成财务报告

**功能**：
- 分析消费模式
- 预算追踪
- 可视化财务数据
- 从PDF提取交易记录
- 计算储蓄率
- 识别支出趋势

**使用场景**：
```
触发词：
- "分析我的财务"
- "追踪支出"
- "创建财务报告"
- "提取PDF交易记录"
- "可视化预算"
```

---

### 9. ai-daily-brief - AI 资讯收集器 ⭐⭐⭐

**描述**：自动生成 AI 日报，面向产品经理和 AI 从业者。

**主要用途**：
- 配合 AI 创新报告定时任务
- 快速浏览 AI 领域资讯
- 生成结构化 HTML 日报

**特点**：
- 预设信息源搜索
- 规范筛选和提炼
- 自动排序
- 支持自定义

**使用场景**：
```
触发词：
- "生成 AI 日报"
- "AI 资讯采集"
- "今日 AI 动态"
```

**实际应用**：
```
# 在 AI 创新报告任务中配合使用
# 定时任务ID: 52c8bec1-0a70-42c5-8f60-6090636b029d

"使用 ai-daily-brief skill 采集今天的 AI 资讯，
关注方向：模型发布、工具更新、开源项目"
```

---

### 10. data-analyst - 数据分析师 ⭐⭐

**描述**：分析 CSV 数据集，处理缺失值，创建交互式仪表板。

**主要用途**：
- CSV 数据清洗
- 缺失值填充
- 统计分析
- Plotly Dash 仪表板

**使用场景**：
```
触发词：
- "分析 CSV 数据"
- "处理缺失值"
- "创建仪表板"
- "数据质量评估"
```

---

## 🔧 其他实用 Skill

### humanizer-zh - 文本人性化 ⭐

**用途**：去除 AI 生成痕迹，使文本更自然。

**触发场景**：
```
"润色这段报告，使其更人性化"
```

### obsidian - 笔记管理 ⭐

**用途**：管理 Obsidian 笔记库（Markdown）。

**触发场景**：
```
"在 Obsidian 中创建投资笔记"
```

### weather - 天气查询 ⭐

**用途**：获取当前天气和预报（无需 API Key）。

**触发场景**：
```
"深圳今天天气如何？"
```

### skill-creator - Skill 开发 ⭐

**用途**：创建新的自定义 Skill。

**触发场景**：
```
"帮我创建一个新的 Skill 用于..."
```

---

## 📚 Skill 使用最佳实践

### 1. 明确触发词

**推荐做法**：
```
❌ "处理这个文件"（不明确）
✅ "使用 xlsx skill 更新这个 Excel 文件"（明确）
```

### 2. 组合使用

**示例：生成投资报告**
```
1. web-fetch: 抓取市场新闻
2. data-analyst: 分析价格数据
3. business-analytics-reporter: 生成业绩分析
4. docx: 创建最终报告
```

### 3. 错误处理

```python
# 在脚本中使用 try-except
try:
    # 使用 skill 处理
    result = process_with_skill()
except Exception as e:
    # 降级到备用方案
    result = fallback_method()
```

### 4. 定期更新

```bash
# 检查 Skill 更新（在支持的环境中）
clawdbot skills update
```

---

## 🔄 Skill 迁移指南

### 检查已安装 Skill

**在 Claw 对话中**：
```
"列出所有已安装的 skill"
```

### 导出 Skill 列表

```bash
# 如果使用 clawdbot
clawdbot skills list > /data/workspace/installed_skills.txt
```

### 在新 Claw 实例中安装

**方式1：手动安装**
```
"安装以下 skill：
- xlsx
- docx
- web-fetch
- pptx
- pdf
- diagram-generator
- business-analytics-reporter
- finance-manager
- ai-daily-brief"
```

**方式2：批量安装脚本**
```bash
# 如果使用 clawdbot
for skill in xlsx docx web-fetch pptx pdf; do
    clawdbot skills install $skill
done
```

---

## 💡 自定义 Skill 开发

### 使用 skill-creator

```
"使用 skill-creator 创建一个新的 skill：

名称：stock-analyzer
用途：自动化股票分析
功能：
1. 从多个数据源获取价格
2. 计算技术指标
3. 生成评分
4. 输出建议"
```

### Skill 结构

```
my-skill/
├── SKILL.md          # Skill 描述和指令
├── README.md         # 使用说明
├── tools/            # 工具脚本
│   └── analyzer.py
└── resources/        # 资源文件
    └── templates/
```

---

## 🔗 相关资源

### Skill 文档
- 每个 Skill 的详细说明在其各自的 README 中
- 使用 `skill-creator` 查看 Skill 开发指南

### 脚本集成
- `/data/workspace/scripts/` - 所有定时任务脚本都集成了 Skill 调用

### 最佳实践案例
- 美股2.0更新脚本：集成 xlsx skill
- AI 创新报告：集成 web-fetch + pptx skill
- 市场洞察报告：集成 docx skill

---

**文档维护者**：AI Assistant  
**最后更新**：2026-02-25
