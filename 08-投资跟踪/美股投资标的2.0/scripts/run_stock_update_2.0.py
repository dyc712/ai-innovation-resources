#!/usr/bin/env python3
"""
美股投资标的2.0更新任务包装脚本
负责执行更新并发送企业微信通知
"""

import subprocess
import sys
import os
from datetime import datetime

def send_notification(title, message):
    """发送企业微信通知"""
    # 这里需要调用notify工具，在定时任务中会自动处理
    print("[NOTIFY_TRIGGER]")
    print(f"Title: {title}")
    print(f"Message: {message}")
    print("[NOTIFY_END]")

def main():
    print("=" * 80)
    print("🚀 美股投资标的2.0自动更新任务")
    print(f"⏰ 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # 执行更新脚本
    script_path = "/data/workspace/scripts/update_stock_2.0.py"
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=600  # 10分钟超时
        )
        
        # 提取报告内容
        output = result.stdout
        if "[REPORT_FOR_NOTIFY]" in output:
            report = output.split("[REPORT_FOR_NOTIFY]")[-1].strip()
        else:
            report = output
        
        if result.returncode == 0:
            print("✅ 更新任务执行成功")
            send_notification(
                "✅ 美股2.0更新成功",
                report
            )
        else:
            print(f"❌ 更新任务执行失败 (退出码: {result.returncode})")
            error_msg = f"**执行失败**\n\n```\n{result.stderr}\n```"
            send_notification(
                "❌ 美股2.0更新失败",
                error_msg
            )
            
    except subprocess.TimeoutExpired:
        error_msg = "⏱️ 更新任务执行超时（>10分钟）"
        print(error_msg)
        send_notification(
            "⚠️ 美股2.0更新超时",
            error_msg
        )
    except Exception as e:
        error_msg = f"💥 更新任务执行异常: {str(e)}"
        print(error_msg)
        send_notification(
            "❌ 美股2.0更新异常",
            error_msg
        )

if __name__ == "__main__":
    main()
