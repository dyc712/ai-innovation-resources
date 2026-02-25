# 美股投资标的2.0

## 📋 目录说明

### scripts/
更新脚本文件：
- `update_stock_2.0.py` - V3版本（Finnhub + yfinance）
- `update_stock_2.0_v4.py` - V4版本（富途 + yfinance + Polygon.io）
- `run_stock_update_2.0.py` - 包装脚本（自动通知）
- `test_stock_v4.py` - V4测试脚本
- `test_yfinance_only.py` - 纯yfinance测试脚本

### data/
数据文件：
- `美股投资标的_跟踪2.0.xlsx` - 32只美股标的跟踪表

### docs/
配置文档：
- `美股2.0数据源切换说明_V3.md` - V3架构说明
- `美股2.0数据源升级说明_V4.md` - V4升级说明
- `美股2.0 V4快速入门.md` - 快速开始指南
- `美股投资标的2.0 V4升级完成报告.md` - 升级报告
- `富途OpenD配置指南.md` - 富途配置详解

### reports/
最新更新报告（每日更新）

---

## 🚀 快速开始

### 1. 安装依赖
```bash
pip3 install finnhub-python yfinance pandas openpyxl requests
```

### 2. 运行更新
```bash
# V4版本（推荐）
python3 scripts/update_stock_2.0_v4.py

# V3版本
python3 scripts/update_stock_2.0.py
```

### 3. 查看结果
更新后的数据保存在 `data/美股投资标的_跟踪2.0.xlsx`

---

## 📊 系统架构

### V4数据源（2026-02-25）
```
优先级：
1. 富途 OpenAPI（实时，需本地FutuOpenD）
2. yfinance 优化版（15-30分钟延迟）
3. Polygon.io（历史回测）
```

### 分析指标（29个）
- 技术面：RS相对强度、VAP筹码、趋势动量、ATR波动率
- 资金面：机构持仓、筹码集中度
- 消息面：分析师评级、市场情绪
- 综合：总评分、执行优先级（A/B/C级）

### 新增功能（V4）
- ✅ 指数跟踪（QQQ、SPY）
- ✅ 市场环境判断（多头/震荡/空头）
- ✅ 系统性风控（指数空头保护）

---

## ⏰ 定时任务

- **执行时间**：每天早上6:00（北京时间）
- **对应时间**：美股收盘后1小时（美东17:00）
- **Cron表达式**：`0 6 * * *`
- **任务ID**：`cc97b4b3-c824-4b90-ba5b-598b65c5dc47`

---

## 📈 成功率

| 版本 | 数据源 | 成功率 | 更新时间 |
|------|--------|--------|---------|
| V4 | 富途+yfinance+Polygon | 95%+ | 2026-02-25 |
| V3 | Finnhub+yfinance | 81.2% | 2026-02-24 |
| V2 | Finnhub单一 | 63.6% | 2026-02-22 |

---

📅 **最后更新**: 2026-02-25
