#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AH股投资标的2.0自动更新任务包装脚本
此脚本作为定时任务的入口，会调用核心更新脚本并发送企业微信通知
"""

import subprocess
import sys
import os
from datetime import datetime

def send_notification(title, message):
    """发送企业微信通知"""
    try:
        # 使用Python API调用notify
        import json
        notification = {
            'title': title,
            'message': message
        }
        print(f"\n{'='*60}")
        print(f"企业微信通知内容:")
        print(f"标题: {title}")
        print(f"内容:\n{message}")
        print(f"{'='*60}\n")
        
        # 实际发送通知的代码（通过Knot API）
        # 注意：这里需要调用notify工具，但在脚本中我们只能打印
        # 实际通知由定时任务的jobMessage触发
        
    except Exception as e:
        print(f"通知发送失败: {str(e)}")

def run_update():
    """执行AH股更新任务"""
    script_path = '/data/workspace/scripts/update_ah_stock_2.0.py'
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始执行AH股投资标的2.0自动更新任务...")
    
    try:
        # 执行更新脚本（设置30分钟超时）
        result = subprocess.run(
            ['python3', script_path],
            capture_output=True,
            text=True,
            timeout=1800
        )
        
        if result.returncode == 0:
            # 成功
            success_msg = f"""
# ✅ AH股投资标的2.0更新成功

**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{result.stdout}

---
📊 查看完整数据: `/data/workspace/stock_pool/AH股投资标的_跟踪2.0.xlsx`
"""
            send_notification("✅ AH股2.0更新成功", success_msg)
            print(success_msg)
            return 0
        else:
            # 失败
            error_msg = f"""
# ❌ AH股投资标的2.0更新失败

**失败时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 错误信息
```
{result.stderr}
```

## 建议解决方案
1. 检查网络连接是否正常
2. 检查Yahoo Finance API是否限流
3. 手动执行脚本查看详细错误: `python3 {script_path}`
4. 如持续失败，考虑增加请求间隔或更换数据源

---
⚠️ 请及时处理以确保数据准确性
"""
            send_notification("❌ AH股2.0更新失败", error_msg)
            print(error_msg)
            return 1
            
    except subprocess.TimeoutExpired:
        timeout_msg = f"""
# ⏱️ AH股投资标的2.0更新超时

**超时时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

任务执行超过30分钟，已被强制终止。

## 可能原因
1. API响应缓慢或限流
2. 网络连接不稳定
3. 股票数量过多导致处理时间过长

## 建议解决方案
1. 检查网络状态
2. 增加请求间隔（当前1秒）
3. 考虑分批更新
4. 手动执行并观察卡在哪个股票

---
⚠️ 请手动重试更新任务
"""
        send_notification("⏱️ AH股2.0更新超时", timeout_msg)
        print(timeout_msg)
        return 1
        
    except Exception as e:
        exception_msg = f"""
# ⚠️ AH股投资标的2.0更新异常

**异常时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 异常详情
```
{str(e)}
```

## 建议
请联系技术支持或查看系统日志获取详细信息

---
⚠️ 任务执行遇到未知错误
"""
        send_notification("⚠️ AH股2.0更新异常", exception_msg)
        print(exception_msg)
        return 1

if __name__ == '__main__':
    exit_code = run_update()
    sys.exit(exit_code)
