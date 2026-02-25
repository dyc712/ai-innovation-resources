# Claw 配置同步文档

## 📋 文档概述

本文档包含您的 Claw 实例的完整配置信息，包括定时任务、Skill使用经验、记忆体信息等。

**目的**：方便将配置迁移到其他 Claw 实例，实现快速学习和同步。

**创建时间**：2026-02-25  
**环境**：AnyDev 开发机 (Linux)  
**工作目录**：`/data/workspace`

---

## 📑 文档结构

本配置文档分为以下几个部分：

1. **定时任务配置** (`01-定时任务配置.md`) - 所有 cron 定时任务的详细配置
2. **Skill 使用指南** (`02-Skill使用指南.md`) - 已安装的 Skill 和使用经验
3. **记忆体信息** (`03-记忆体信息.md`) - 系统记忆的关键信息
4. **环境配置** (`04-环境配置.md`) - 开发环境、依赖库、脚本路径
5. **快速迁移指南** (`05-快速迁移指南.md`) - 新 Claw 实例的配置步骤

---

## 🚀 快速开始

### 对于新的 Claw 实例

1. **克隆配置仓库**：
```bash
cd /data/workspace
git clone https://github.com/dyc712/ai-innovation-resources.git
```

2. **导入配置文档**：
将 `09-Claw配置同步/` 目录下的所有文档内容提供给新 Claw 实例阅读

3. **执行迁移脚本**：
```bash
python3 /data/workspace/scripts/setup_new_claw.py
```

4. **验证配置**：
```bash
# 检查定时任务
python3 -c "from cron import list; print(list())"

# 检查关键脚本
ls -lh /data/workspace/scripts/
```

---

## 📊 配置概览

### 定时任务统计
- **总数**：4个定时任务
- **类型**：投资跟踪(2)、AI信息采集(1)、市场分析(1)
- **执行频率**：每日(3)、每周(1)

### Skill 统计
- **已安装**：14个 Skill
- **常用**：docx, xlsx, pdf, web-fetch, diagram-generator
- **专用**：business-analytics-reporter, finance-manager, ai-daily-brief

### 记忆体信息
- **投资跟踪**：美股32只、AH股若干
- **报告生成**：AI创新报告、市场洞察报告
- **GitHub集成**：自动同步到 ai-innovation-resources 仓库

---

## 🔗 相关链接

- **GitHub 仓库**：https://github.com/dyc712/ai-innovation-resources
- **配置文档目录**：`09-Claw配置同步/`
- **乐享投资跟踪**：https://lexiangla.com/pages/9e1769519a9343fc8042084e3e9b9c4b

---

## 📝 更新日志

| 日期 | 版本 | 更新内容 |
|------|------|---------|
| 2026-02-25 | v1.0 | 初始版本，包含所有配置信息 |

---

## ⚠️ 重要提示

### AnyDev 开发机限制

新 Claw 实例需要注意 AnyDev 开发机的网络限制：

| 服务 | 可用性 | 备注 |
|------|--------|------|
| GitHub | ✅ 可用 | 用于代码同步 |
| yfinance | ✅ 可用 | 美股数据主要来源 |
| 富途 OpenD | ❌ 不可用 | SSL连接失败，需Mac本地运行 |
| Finnhub API | ❌ 不可用 | 网络限制 |
| 乐享 API | ❌ 不可用 | 需通过GitHub中转 |

### 数据源策略

由于网络限制，当前配置采用：
- **主数据源**：yfinance (95%+ 成功率)
- **备用方案**：通过 GitHub 中转上传到乐享
- **实时行情**：需 Mac 本地运行富途 OpenD + SSH 隧道

---

## 📖 详细文档索引

点击下方链接查看各部分详细配置：

1. [定时任务配置](./01-定时任务配置.md) - 4个定时任务的完整配置
2. [Skill 使用指南](./02-Skill使用指南.md) - 14个 Skill 的使用场景
3. [记忆体信息](./03-记忆体信息.md) - 系统记忆的关键知识
4. [环境配置](./04-环境配置.md) - Python环境、依赖库、脚本清单
5. [快速迁移指南](./05-快速迁移指南.md) - 一键配置新 Claw 实例

---

**文档维护者**：AI Assistant  
**联系方式**：通过 Claw 实例交互
