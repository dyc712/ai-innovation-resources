# 富途OpenD配置指南

## 📋 什么是FutuOpenD?

FutuOpenD是富途证券提供的本地网关程序,充当您的Python脚本与富途服务器之间的桥梁。它不是一个Python库,而是需要单独下载运行的守护进程。

---

## 🚀 快速开始

### 1. 下载FutuOpenD

#### Linux系统（AnyDev开发机）

```bash
# 下载Linux版本
cd /data/workspace/tools
wget https://softwarefile.futunn.com/FutuOpenD_7.2.3308_Ubuntu16.04.tar.gz

# 解压
tar -zxvf FutuOpenD_7.2.3308_Ubuntu16.04.tar.gz
cd FutuOpenD_7.2.3308_Ubuntu16.04

# 赋予执行权限
chmod +x FutuOpenD
```

#### Mac系统

```bash
# 下载Mac版本
wget https://softwarefile.futunn.com/FutuOpenD_7.2.3308_MacOS.dmg

# 双击dmg文件安装
```

#### Windows系统

- 下载链接: https://www.futunn.com/download/OpenAPI
- 下载后双击exe文件安装

---

### 2. 配置FutuOpenD

创建配置文件 `FutuOpenD.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<FutuOpenD>
    <client_id>123456789</client_id>  <!-- 富途牛牛账号 -->
    <rsa_private_key></rsa_private_key>  <!-- 如需加密连接,填写私钥 -->
    <rsa_public_key></rsa_public_key>    <!-- 如需加密连接,填写公钥 -->
    <api_ip>127.0.0.1</api_ip>
    <api_port>11111</api_port>
    <push_proto_type>json</push_proto_type>
    <qot_push_frequency>3000</qot_push_frequency>
    <telnet_ip>127.0.0.1</telnet_ip>
    <telnet_port>22222</telnet_port>
    <login_region>1</login_region>  <!-- 1=港股 2=美股 3=A股 -->
</FutuOpenD>
```

---

### 3. 启动FutuOpenD

#### Linux/Mac（推荐后台运行）

```bash
cd /data/workspace/tools/FutuOpenD_7.2.3308_Ubuntu16.04

# 前台运行（测试用）
./FutuOpenD

# 后台运行（生产环境）
nohup ./FutuOpenD > futuopend.log 2>&1 &

# 查看日志
tail -f futuopend.log

# 查看进程
ps aux | grep FutuOpenD

# 停止进程
pkill FutuOpenD
```

#### Windows

- 双击 `FutuOpenD.exe` 启动
- 会打开一个黑色命令行窗口,保持窗口开启

---

### 4. 验证连接

```bash
# 安装Python客户端库
pip install futu-api

# 测试连接
python3 << EOF
from futu import OpenQuoteContext, RET_OK

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
ret, data = quote_ctx.get_market_snapshot(['US.AAPL'])

if ret == RET_OK:
    print("✅ 连接成功!")
    print(data)
else:
    print("❌ 连接失败:", data)

quote_ctx.close()
EOF
```

预期输出:
```
✅ 连接成功!
      code  last_price  prev_close_price  ...
0  US.AAPL      175.23            174.50  ...
```

---

## 🔧 常见问题排查

### 问题1: 连接被拒绝

```
ConnectionRefusedError: [Errno 111] Connection refused
```

**原因**: FutuOpenD未启动

**解决**:
```bash
# 检查进程是否在运行
ps aux | grep FutuOpenD

# 如果没有,启动它
cd /data/workspace/tools/FutuOpenD_7.2.3308_Ubuntu16.04
./FutuOpenD &
```

---

### 问题2: 端口被占用

```
bind port fail, error code: 98
```

**原因**: 11111端口已被占用

**解决**:
```bash
# 查看占用端口的进程
lsof -i :11111

# 如果是旧的FutuOpenD进程,杀掉它
kill -9 <PID>

# 重新启动
./FutuOpenD &
```

---

### 问题3: 超过订阅数量限制

```
订阅失败: 超过最大订阅数量
```

**原因**: 免费账户有订阅限制

**解决方案**:
- 免费账户: 最多订阅5只股票
- 需要订阅更多: 开通富途证券账户
- 或使用分批订阅方式:

```python
# 分批订阅（每批5只）
import time

tickers = ['US.AAPL', 'US.TSLA', 'US.NVDA', 'US.GOOGL', 'US.MSFT', 'US.AMZN']

for i in range(0, len(tickers), 5):
    batch = tickers[i:i+5]
    # 处理这一批
    # ...
    
    # 取消订阅,释放名额
    quote_ctx.unsubscribe(batch, [SubType.QUOTE])
    time.sleep(1)
```

---

### 问题4: AnyDev开发机网络限制

如果AnyDev开发机无法直接访问富途服务器:

**方案A: 使用本地Mac/Windows运行FutuOpenD**

1. 在本地Mac/Windows启动FutuOpenD
2. 修改脚本连接到本地机器:

```python
# 修改 update_stock_2.0_v4.py
FUTU_HOST = "192.168.1.100"  # 你的本地机器IP
FUTU_PORT = 11111
```

3. 确保本地防火墙允许11111端口

**方案B: 使用SSH隧道**

```bash
# 在AnyDev开发机执行
ssh -L 11111:127.0.0.1:11111 user@your-local-machine

# 然后脚本中继续使用 127.0.0.1:11111
```

---

## 📊 使用限制对比

| 账户类型 | 免费账户 | 富途证券账户 |
|---------|---------|-------------|
| **行情订阅** | 5只股票 | 无限制 |
| **历史K线** | 最近2年 | 全部历史 |
| **实时推送** | 不支持 | 支持 |
| **Level2数据** | 不支持 | 支持 |
| **交易功能** | 不支持 | 支持 |

---

## 🎯 针对您的使用场景建议

### 方案1: 混合模式（推荐）✅

**适用场景**: 32只股票 + 2只指数 = 34只标的

```python
# 优先使用富途获取指数和核心股票（前5只）
# 其余股票使用yfinance
```

**优点**: 
- 免费
- 指数数据实时性高
- 大部分股票仍可获取

**实施**:
```python
# 在脚本中设置优先级
FUTU_PRIORITY_TICKERS = ['QQQ', 'SPY', 'NVDA', 'AAPL', 'TSLA']

if ticker in FUTU_PRIORITY_TICKERS:
    # 使用富途
else:
    # 使用yfinance
```

---

### 方案2: 纯yfinance模式（当前备用）

**如果富途连接失败,脚本会自动fallback到yfinance**

```python
# 脚本会自动检测
if quote_ctx is None:
    print("⚠️  富途不可用,使用yfinance...")
```

---

### 方案3: 开通富途证券账户（长期方案）

**好处**:
- 无订阅限制
- 实时推送行情
- 可进行美股交易

**开户**: https://www.futunn.com/

---

## 📝 配置文件示例

### 最小配置（免费账户）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<FutuOpenD>
    <api_ip>127.0.0.1</api_ip>
    <api_port>11111</api_port>
    <login_region>2</login_region>  <!-- 2=美股 -->
</FutuOpenD>
```

### 生产环境配置（证券账户）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<FutuOpenD>
    <client_id>YOUR_FUTU_ACCOUNT</client_id>
    <api_ip>127.0.0.1</api_ip>
    <api_port>11111</api_port>
    <push_proto_type>json</push_proto_type>
    <qot_push_frequency>1000</qot_push_frequency>  <!-- 行情推送频率 -->
    <login_region>2</login_region>
    <login_account>YOUR_PHONE_OR_EMAIL</login_account>
    <login_pwd_md5>YOUR_PASSWORD_MD5</login_pwd_md5>
</FutuOpenD>
```

---

## 🔗 官方文档链接

- **富途OpenAPI主页**: https://www.futunn.com/download/OpenAPI
- **Python API文档**: https://openapi.futunn.com/futu-api-doc/
- **FutuOpenD下载**: https://www.futunn.com/download/OpenAPI#FutuOpenD
- **示例代码**: https://github.com/FutunnOpen/py-futu-api

---

## 🚀 启动脚本（推荐）

创建 `/data/workspace/scripts/start_futuopend.sh`:

```bash
#!/bin/bash

FUTU_DIR="/data/workspace/tools/FutuOpenD_7.2.3308_Ubuntu16.04"
FUTU_BIN="$FUTU_DIR/FutuOpenD"
LOG_FILE="$FUTU_DIR/futuopend.log"
PID_FILE="$FUTU_DIR/futuopend.pid"

# 检查是否已在运行
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ FutuOpenD已在运行 (PID: $PID)"
        exit 0
    fi
fi

# 启动FutuOpenD
echo "🚀 启动FutuOpenD..."
cd "$FUTU_DIR"
nohup "$FUTU_BIN" > "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"

# 等待启动
sleep 3

# 验证启动
if ps -p $(cat "$PID_FILE") > /dev/null 2>&1; then
    echo "✅ FutuOpenD启动成功 (PID: $(cat $PID_FILE))"
    echo "📄 日志文件: $LOG_FILE"
else
    echo "❌ FutuOpenD启动失败"
    cat "$LOG_FILE"
    exit 1
fi
```

使用:
```bash
chmod +x /data/workspace/scripts/start_futuopend.sh
/data/workspace/scripts/start_futuopend.sh
```

---

**维护人员**: AI助手  
**最后更新**: 2026-02-25  
**下次Review**: 测试富途连接后更新
