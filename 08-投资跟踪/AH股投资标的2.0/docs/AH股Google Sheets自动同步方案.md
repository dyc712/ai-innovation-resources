# AH股投资标的2.0 - Google Sheets自动同步方案

## 📋 方案概述

由于AnyDev开发机无法直接访问Google API，采用**GitHub中转**的方式实现自动同步：

```
AnyDev开发机 → GitHub仓库 → Mac本地 → Google Sheets
   (自动推送)      (版本控制)    (定时拉取)   (API上传)
```

**优势**：
- ✅ 完全自动化（配置一次，永久运行）
- ✅ 有版本历史（GitHub记录所有变更）
- ✅ 高可靠性（即使Mac关机，数据也在GitHub）
- ✅ 无需人工干预

---

## 🚀 完整配置步骤

### 第一步：AnyDev端配置（已完成✅）

**脚本位置**：`/data/workspace/scripts/sync_ah_stock_to_git.py`

**功能**：每次AH股数据更新后，自动推送到GitHub仓库

**测试结果**：
```
✅ 成功同步到GitHub: 2026-02-25 19:37:31
🔗 查看仓库: https://github.com/dyc712/ai-innovation-resources.git
📁 GitHub路径: 08-投资跟踪/AH股投资标的/AH股投资标的_跟踪2.0.xlsx
```

**如何使用**：
```bash
# 在AnyDev开发机执行
python3 /data/workspace/scripts/sync_ah_stock_to_git.py
```

---

### 第二步：Google API配置（需要在Mac本地完成）

#### 2.1 创建Google Cloud项目

1. **访问Google Cloud Console**
   ```
   https://console.cloud.google.com/
   ```

2. **创建新项目**
   - 点击顶部的项目下拉菜单
   - 选择"新建项目"
   - 项目名称：`AH股投资跟踪`
   - 点击"创建"

3. **启用Google Sheets API**
   - 在左侧菜单选择"API和服务" > "库"
   - 搜索"Google Sheets API"
   - 点击"启用"

#### 2.2 创建服务账号

1. **创建服务账号**
   - 左侧菜单：IAM和管理 > 服务账号
   - 点击"创建服务账号"
   - 服务账号名称：`ah-stock-sync`
   - 服务账号ID：`ah-stock-sync@项目ID.iam.gserviceaccount.com`
   - 点击"创建并继续"
   - 角色：选择"编辑者"（或不选）
   - 点击"完成"

2. **生成JSON密钥**
   - 在服务账号列表中找到刚创建的账号
   - 点击服务账号邮箱
   - 切换到"密钥"标签页
   - 点击"添加密钥" > "创建新密钥"
   - 选择"JSON"格式
   - 点击"创建"
   - **JSON文件会自动下载到您的Mac**

3. **保存凭证文件**
   ```bash
   # 在Mac终端执行
   mv ~/Downloads/项目ID-xxxx.json ~/google-credentials.json
   
   # 验证文件存在
   ls -lh ~/google-credentials.json
   ```

#### 2.3 创建Google Sheets并共享

1. **创建新的Google Sheets**
   - 访问 https://sheets.google.com
   - 点击"空白"创建新表格
   - 重命名为：`AH股投资标的_跟踪2.0`

2. **获取表格ID**
   - 从URL中复制ID
   - 格式：`https://docs.google.com/spreadsheets/d/{这里是ID}/edit`
   - 示例：如果URL是 `https://docs.google.com/spreadsheets/d/1ABC-xyz123/edit`
   - 那么ID就是：`1ABC-xyz123`

3. **共享表格给服务账号**
   - 点击右上角"共享"按钮
   - 在"添加用户和群组"中输入服务账号邮箱
     格式：`ah-stock-sync@项目ID.iam.gserviceaccount.com`
   - 权限设为：**编辑者**
   - **取消勾选**"通知用户"
   - 点击"共享"

---

### 第三步：Mac本地配置

#### 3.1 安装Python依赖

```bash
# 在Mac终端执行
pip3 install gspread google-auth pandas openpyxl

# 验证安装
python3 -c "import gspread; import pandas; print('✅ 依赖安装成功')"
```

#### 3.2 下载并配置脚本

```bash
# 创建脚本目录
mkdir -p ~/scripts

# 从AnyDev下载脚本（或手动复制）
# 脚本内容见附件：upload_ah_stock_to_gsheet.py
```

**重要配置项**（编辑脚本中的配置区域）：

```python
# 修改这两个配置
CREDENTIALS_FILE = os.path.expanduser("~/google-credentials.json")  # 凭证文件路径
SPREADSHEET_ID = "YOUR_SPREADSHEET_ID_HERE"  # 替换为您的表格ID
```

示例：
```python
SPREADSHEET_ID = "1ABC-xyz123"  # 从Google Sheets URL中获取
```

#### 3.3 测试脚本

```bash
# 手动运行测试
python3 ~/scripts/upload_ah_stock_to_gsheet.py

# 预期输出：
# ======================================================================
# AH股投资标的2.0 - Google Sheets自动同步
# 时间: 2026-02-25 20:00:00
# ======================================================================
# ✅ 所有依赖已安装
# ✅ 凭证文件存在: /Users/dongyunchuan/google-credentials.json
# 🔄 拉取最新代码...
# ✅ 已更新到最新版本
# 📄 Excel文件大小: 10.9 KB
# 📖 读取Excel文件...
# ✅ 成功读取: 15 行 x 10 列
# 🔗 连接Google Sheets...
# ✅ 已打开表格: AH股投资标的_跟踪2.0
# ✅ 已找到工作表: AH股投资标的2.0
# 📝 更新数据到Google Sheets...
# ✅ 成功上传 15 行数据到 Google Sheets
# 🔗 查看表格: https://docs.google.com/spreadsheets/d/1ABC-xyz123/edit
# ======================================================================
# ✅ 所有操作成功完成！
# 📊 数据已同步到Google Sheets
# ======================================================================
```

---

### 第四步：配置Mac自动任务

#### 方式1：使用launchd（推荐）

```bash
# 创建launchd配置文件
cat > ~/Library/LaunchAgents/com.user.ah-stock-sync.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.ah-stock-sync</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/Users/dongyunchuan/scripts/upload_ah_stock_to_gsheet.py</string>
    </array>
    
    <key>StartInterval</key>
    <integer>3600</integer>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>StandardOutPath</key>
    <string>/Users/dongyunchuan/logs/ah-stock-sync.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Users/dongyunchuan/logs/ah-stock-sync-error.log</string>
</dict>
</plist>
EOF

# 创建日志目录
mkdir -p ~/logs

# 加载任务
launchctl load ~/Library/LaunchAgents/com.user.ah-stock-sync.plist

# 验证任务状态
launchctl list | grep ah-stock-sync

# 立即测试任务
launchctl start com.user.ah-stock-sync

# 查看日志
tail -f ~/logs/ah-stock-sync.log
```

**参数说明**：
- `StartInterval`: 3600秒（每小时检查一次）
- `RunAtLoad`: 开机自动运行
- 日志文件：`~/logs/ah-stock-sync.log`

#### 方式2：使用cron（备选）

```bash
# 编辑crontab
crontab -e

# 添加以下行（每小时第0分钟执行）
0 * * * * /usr/local/bin/python3 ~/scripts/upload_ah_stock_to_gsheet.py >> ~/logs/ah-stock-sync.log 2>&1

# 保存并退出（按Esc，输入:wq）

# 验证cron任务
crontab -l
```

---

## 🔧 故障排查

### 问题1：找不到表格ID

**症状**：
```
❌ 找不到表格ID: YOUR_SPREADSHEET_ID_HERE
```

**解决**：
1. 检查脚本中的`SPREADSHEET_ID`配置是否正确
2. 确认已从URL中复制正确的ID
3. 确认已共享表格给服务账号

### 问题2：权限不足

**症状**：
```
gspread.exceptions.APIError: [403] The caller does not have permission
```

**解决**：
1. 检查服务账号邮箱是否正确
2. 确认在Google Sheets中已添加该邮箱为编辑者
3. 等待1-2分钟后重试（权限生效需要时间）

### 问题3：凭证文件错误

**症状**：
```
❌ Google API凭证文件不存在
```

**解决**：
```bash
# 检查文件是否存在
ls -lh ~/google-credentials.json

# 检查文件内容（应该是JSON格式）
head -5 ~/google-credentials.json

# 如果文件不存在，重新下载JSON密钥
```

### 问题4：Mac休眠导致任务停止

**解决方案**：

```bash
# 方式1: 防止Mac休眠（不推荐，费电）
sudo pmset -a sleep 0

# 方式2: 设置定时唤醒（推荐）
# 每天早上7点自动唤醒
sudo pmset repeat wakeorpoweron MTWRFSU 07:00:00

# 方式3: 使用caffeinate防止休眠
# 修改launchd配置中的ProgramArguments：
<array>
    <string>/usr/bin/caffeinate</string>
    <string>-s</string>
    <string>/usr/local/bin/python3</string>
    <string>/Users/dongyunchuan/scripts/upload_ah_stock_to_gsheet.py</string>
</array>
```

---

## 📊 完整工作流程

### 自动化流程

```
1. AnyDev定时更新AH股数据
   ↓
2. 更新后自动运行 sync_ah_stock_to_git.py
   ↓
3. Excel文件推送到GitHub
   ↓
4. Mac本地launchd任务（每小时）
   ↓
5. 从GitHub拉取最新文件
   ↓
6. 解析Excel数据
   ↓
7. 通过Google API上传到Sheets
   ↓
8. 完成！可以在线查看
```

### 手动触发

**在AnyDev端**：
```bash
python3 /data/workspace/scripts/sync_ah_stock_to_git.py
```

**在Mac端**：
```bash
python3 ~/scripts/upload_ah_stock_to_gsheet.py
```

---

## 📈 监控与维护

### 查看同步日志

```bash
# Mac端日志
tail -f ~/logs/ah-stock-sync.log

# AnyDev端日志（如果配置了日志）
tail -f /data/workspace/logs/ah-stock-sync.log
```

### 监控任务状态

```bash
# Mac端 - 查看launchd任务
launchctl list | grep ah-stock-sync

# 如果需要重启任务
launchctl unload ~/Library/LaunchAgents/com.user.ah-stock-sync.plist
launchctl load ~/Library/LaunchAgents/com.user.ah-stock-sync.plist
```

### 定期检查

建议每周检查：
1. ✅ GitHub仓库是否有最新提交
2. ✅ Google Sheets数据是否更新
3. ✅ Mac端日志是否有错误
4. ✅ launchd任务是否正常运行

---

## 🎯 优化建议

### 1. 增加企业微信通知

在Mac脚本中添加通知功能：

```python
# 在main()函数末尾添加
def send_wechat_notification(success, message):
    """发送企业微信通知"""
    # 使用Knot消息通知机器人
    pass
```

### 2. 数据版本对比

```python
def compare_versions():
    """对比新旧数据，标记变化"""
    # 读取上次同步的数据
    # 对比当前数据
    # 高亮显示变化的单元格
    pass
```

### 3. 异常重试机制

```python
def upload_with_retry(max_retries=3):
    """失败后自动重试"""
    for i in range(max_retries):
        try:
            upload_to_gsheet()
            break
        except Exception as e:
            if i < max_retries - 1:
                time.sleep(60)  # 等待1分钟后重试
            else:
                raise
```

---

## 📝 配置检查清单

完成配置后，请确认以下项目：

**AnyDev端**：
- [ ] 脚本已创建：`/data/workspace/scripts/sync_ah_stock_to_git.py`
- [ ] 测试运行成功
- [ ] GitHub仓库可以访问
- [ ] Excel文件已推送到GitHub

**Mac端**：
- [ ] Python依赖已安装（gspread, google-auth, pandas, openpyxl）
- [ ] Google API凭证已下载（`~/google-credentials.json`）
- [ ] 脚本已配置（`~/scripts/upload_ah_stock_to_gsheet.py`）
- [ ] SPREADSHEET_ID已正确填写
- [ ] 测试运行成功
- [ ] launchd任务已加载
- [ ] Google Sheets可以访问并查看数据

**Google Cloud端**：
- [ ] 项目已创建
- [ ] Google Sheets API已启用
- [ ] 服务账号已创建
- [ ] JSON密钥已下载
- [ ] Google Sheets已创建
- [ ] 表格已共享给服务账号

---

## 🔗 相关链接

- **GitHub仓库**: https://github.com/dyc712/ai-innovation-resources
- **Google Cloud Console**: https://console.cloud.google.com/
- **Google Sheets**: https://sheets.google.com
- **AnyDev脚本**: `/data/workspace/scripts/sync_ah_stock_to_git.py`
- **Mac脚本**: `~/scripts/upload_ah_stock_to_gsheet.py`

---

## ✅ 总结

**方案优势**：
- ✅ 完全自动化（配置一次，永久运行）
- ✅ 高可靠性（GitHub版本控制 + Google Sheets在线同步）
- ✅ 无需手动干预
- ✅ 支持历史版本回溯
- ✅ 跨平台兼容（AnyDev + Mac）

**预期效果**：
- AH股数据更新后30-60分钟内自动同步到Google Sheets
- 可以随时在线查看最新数据
- 支持多设备访问（手机、平板、电脑）

**后续维护**：
- 定期检查日志
- 确保Mac保持开机（或设置定时唤醒）
- 监控GitHub和Google Sheets同步状态

---

📅 **文档版本**: v1.0  
📝 **最后更新**: 2026-02-25  
✍️ **维护者**: AI Assistant
