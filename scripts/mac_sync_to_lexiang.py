#!/usr/bin/env python3
"""
Mac本地脚本：从GitHub同步投资跟踪文件并上传到乐享
运行环境：Mac本地（需要已配置lexiang skill）
"""
import os
import sys
import subprocess
from pathlib import Path

# GitHub仓库配置
GITHUB_REPO = "https://github.com/dyc712/ai-innovation-resources.git"
LOCAL_REPO_PATH = Path.home() / "ai-innovation-resources"

# 乐享目标目录
LEXIANG_TARGET_URL = "https://lexiangla.com/pages/9e1769519a9343fc8042084e3e9b9c4b"
LEXIANG_PAGE_ID = "9e1769519a9343fc8042084e3e9b9c4b"

# 需要上传的文件路径（相对于仓库根目录）
FILES_TO_UPLOAD = [
    "08-投资跟踪/AH股投资标的/AH股投资标的_跟踪2.0.xlsx",
    "08-投资跟踪/美股投资标的/美股投资标的_跟踪2.0.xlsx",
    "08-投资跟踪/美股投资标的/美股2.0更新报告_20260225_0604.md",
    "08-投资跟踪/美股投资标的/富途OpenD配置指南.md",
    "08-投资跟踪/美股投资标的/美股投资标的2.0-配置说明.md",
]


def run_command(cmd, cwd=None):
    """执行shell命令"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def sync_from_github():
    """从GitHub同步最新文件"""
    print("\n" + "=" * 60)
    print("📥 从GitHub同步最新文件")
    print("=" * 60)
    
    if LOCAL_REPO_PATH.exists():
        print(f"✅ 仓库已存在: {LOCAL_REPO_PATH}")
        print("🔄 执行 git pull...")
        
        success, stdout, stderr = run_command("git pull origin main", cwd=LOCAL_REPO_PATH)
        
        if success:
            print("✅ 同步成功")
            return True
        else:
            print(f"❌ 同步失败: {stderr}")
            return False
    else:
        print(f"📦 克隆仓库到: {LOCAL_REPO_PATH}")
        
        success, stdout, stderr = run_command(
            f"git clone {GITHUB_REPO} {LOCAL_REPO_PATH}"
        )
        
        if success:
            print("✅ 克隆成功")
            return True
        else:
            print(f"❌ 克隆失败: {stderr}")
            return False


def upload_to_lexiang():
    """上传文件到乐享（使用lexiang skill）"""
    print("\n" + "=" * 60)
    print("📤 上传文件到乐享")
    print("=" * 60)
    
    print("\n⚠️  请在Clawdbot对话中运行以下命令：")
    print("-" * 60)
    
    for file_path in FILES_TO_UPLOAD:
        full_path = LOCAL_REPO_PATH / file_path
        
        if full_path.exists():
            print(f"\n上传文件: {file_path}")
            print(f'请向Clawdbot发送：')
            print(f'"""')
            print(f'使用lexiang skill上传文件到乐享：')
            print(f'- 文件路径: {full_path}')
            print(f'- 目标目录: {LEXIANG_TARGET_URL}')
            print(f'"""')
        else:
            print(f"\n⚠️  文件不存在: {file_path}")
    
    print("-" * 60)
    print(f"\n🔗 上传后查看: {LEXIANG_TARGET_URL}")


def main():
    """主函数"""
    print("=" * 60)
    print("🔄 投资跟踪文件同步与上传工具")
    print("=" * 60)
    
    # 步骤1: 从GitHub同步
    if not sync_from_github():
        print("\n❌ GitHub同步失败，终止操作")
        return 1
    
    # 步骤2: 准备上传到乐享的提示
    upload_to_lexiang()
    
    print("\n" + "=" * 60)
    print("✅ 同步完成！请按提示在Clawdbot中上传文件")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
