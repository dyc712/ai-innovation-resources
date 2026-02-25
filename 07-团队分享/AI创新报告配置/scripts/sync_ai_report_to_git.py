#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI创新报告自动同步到GitHub脚本
功能：将生成的AI创新报告自动上传到GitHub仓库，按月份归档
"""

import os
import sys
import shutil
from datetime import datetime
import subprocess

# 配置
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")  # 从环境变量读取，避免硬编码敏感信息
REPO_URL = f"https://dyc712:{GITHUB_TOKEN}@github.com/dyc712/ai-innovation-resources" if GITHUB_TOKEN else "https://github.com/dyc712/ai-innovation-resources"
REPO_NAME = "ai-innovation-resources"
SOURCE_DIR = "/data/workspace/ai_innovation_reports"
FALLBACK_SOURCE_DIR = "/Users/dongyunchuan/openclaw/ai_innovation_reports"

def run_command(cmd, cwd=None):
    """执行Shell命令"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd,
            capture_output=True, 
            text=True, 
            timeout=30
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def sync_reports():
    """同步报告到GitHub"""
    print("=" * 60)
    print("AI创新报告 GitHub同步脚本")
    print("=" * 60)
    
    # 检查源目录
    source_dir = SOURCE_DIR if os.path.exists(SOURCE_DIR) else FALLBACK_SOURCE_DIR
    if not os.path.exists(source_dir):
        print(f"❌ 错误：源目录不存在 {source_dir}")
        return False
    
    print(f"✓ 源目录: {source_dir}")
    
    # 获取今天的日期
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    year_month = today.strftime("%Y-%m")
    
    # 查找今天的报告文件
    md_file = f"AI创新报告_{date_str}.md"
    pptx_file = f"AI创新报告海报_{date_str}.pptx"
    
    md_path = os.path.join(source_dir, md_file)
    pptx_path = os.path.join(source_dir, pptx_file)
    
    if not os.path.exists(md_path):
        print(f"❌ 错误：找不到报告文件 {md_path}")
        return False
    
    print(f"✓ 找到报告文件:")
    print(f"  - {md_file} ({os.path.getsize(md_path)} bytes)")
    if os.path.exists(pptx_path):
        print(f"  - {pptx_file} ({os.path.getsize(pptx_path)} bytes)")
    
    # 工作目录
    work_dir = "/tmp/ai_innovation_sync"
    repo_dir = os.path.join(work_dir, REPO_NAME)
    
    # 清理旧的工作目录
    if os.path.exists(work_dir):
        shutil.rmtree(work_dir)
    os.makedirs(work_dir)
    
    print("\n📥 克隆GitHub仓库...")
    success, stdout, stderr = run_command(
        f"git clone {REPO_URL} {REPO_NAME}",
        cwd=work_dir
    )
    
    if not success:
        print(f"❌ 克隆失败: {stderr}")
        return False
    
    print("✓ 克隆成功")
    
    # 创建目标目录
    target_dir = os.path.join(repo_dir, "07-团队分享", "AI创新报告", year_month)
    os.makedirs(target_dir, exist_ok=True)
    print(f"\n✓ 目标目录: 07-团队分享/AI创新报告/{year_month}/")
    
    # 复制文件
    print("\n📋 复制报告文件...")
    shutil.copy2(md_path, os.path.join(target_dir, md_file))
    print(f"  ✓ {md_file}")
    
    if os.path.exists(pptx_path):
        shutil.copy2(pptx_path, os.path.join(target_dir, pptx_file))
        print(f"  ✓ {pptx_file}")
    
    # Git操作
    print("\n📤 提交到GitHub...")
    
    # 配置Git用户（如果需要）
    run_command('git config user.email "ai-report-bot@example.com"', cwd=repo_dir)
    run_command('git config user.name "AI Report Bot"', cwd=repo_dir)
    
    # 添加文件
    run_command("git add .", cwd=repo_dir)
    
    # 检查是否有变更
    success, stdout, stderr = run_command("git status --short", cwd=repo_dir)
    if not stdout.strip():
        print("⚠️  没有新的变更，跳过提交")
        return True
    
    # 提交
    commit_msg = f"📊 添加AI创新报告 {date_str}"
    success, stdout, stderr = run_command(
        f'git commit -m "{commit_msg}"',
        cwd=repo_dir
    )
    
    if not success:
        print(f"❌ 提交失败: {stderr}")
        return False
    
    print("✓ 提交成功")
    
    # 获取当前分支名
    success, current_branch, stderr = run_command("git branch --show-current", cwd=repo_dir)
    if not success or not current_branch.strip():
        current_branch = "main"
    else:
        current_branch = current_branch.strip()
    
    print(f"\n🚀 推送到GitHub (分支: {current_branch})...")
    
    # 设置推送URL（包含Token）
    push_url = REPO_URL
    run_command(f"git remote set-url origin {push_url}", cwd=repo_dir)
    
    success, stdout, stderr = run_command(f"git push origin {current_branch}", cwd=repo_dir)
    
    if not success:
        print(f"❌ 推送失败: {stderr}")
        print("\n💡 可能的原因:")
        print("   1. GitHub凭证未配置或已过期")
        print("   2. 仓库权限不足")
        print("   3. 网络连接问题")
        print(f"\n📁 仓库位置: {repo_dir}")
        print("\n🔧 解决方法:")
        print("   1. 确保GitHub Personal Access Token已配置")
        print("   2. 运行: git config --global credential.helper store")
        print("   3. 手动推送一次以保存凭证")
        return False
    
    print("✓ 推送成功")
    
    # 清理
    shutil.rmtree(work_dir)
    
    print("\n" + "=" * 60)
    print("✅ 同步完成！")
    print(f"📁 报告已归档到: 07-团队分享/AI创新报告/{year_month}/")
    print(f"🔗 仓库地址: {REPO_URL}")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = sync_reports()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ 发生异常: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
