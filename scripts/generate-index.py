#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI创新资源库 - 自动索引生成器
自动扫描资源目录，生成分类索引和统计信息
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict

class ResourceIndexer:
    """资源索引生成器"""
    
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.categories = [
            "01-模型与研究",
            "02-工具与平台",
            "03-教程与实践",
            "04-行业洞察",
            "05-社区资源",
            "06-每周精选"
        ]
        self.stats = {
            "total_resources": 0,
            "by_category": {},
            "recent_updates": []
        }
    
    def extract_metadata(self, file_path: Path) -> Dict:
        """从Markdown文件提取元数据"""
        metadata = {
            "title": file_path.stem,
            "type": "",
            "author": "",
            "date": "",
            "rating": 0,
            "submitter": "",
            "tags": []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # 提取标题
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                if title_match:
                    metadata["title"] = title_match.group(1).strip()
                
                # 提取类型
                type_match = re.search(r'\*\*类型\*\*[：:]\s*(.+)$', content, re.MULTILINE)
                if type_match:
                    metadata["type"] = type_match.group(1).strip().split('/')[0].strip()
                
                # 提取作者
                author_match = re.search(r'\*\*作者/机构\*\*[：:]\s*(.+)$', content, re.MULTILINE)
                if author_match:
                    metadata["author"] = author_match.group(1).strip()
                
                # 提取日期
                date_match = re.search(r'\*\*发布时间\*\*[：:]\s*(\d{4}-\d{2}-\d{2})', content)
                if date_match:
                    metadata["date"] = date_match.group(1)
                
                # 提取评分
                rating_match = re.search(r'(⭐+)', content)
                if rating_match:
                    metadata["rating"] = len(rating_match.group(1))
                
                # 提取提交者
                submitter_match = re.search(r'\*\*提交者\*\*[：:]\s*\[@?([^\]]+)\]', content)
                if submitter_match:
                    metadata["submitter"] = submitter_match.group(1).strip()
                
                # 提取标签
                tags_match = re.search(r'\*\*标签\*\*[：:]\s*(.+)$', content, re.MULTILINE)
                if tags_match:
                    tags_str = tags_match.group(1)
                    metadata["tags"] = [tag.strip() for tag in re.findall(r'#(\w+)', tags_str)]
        
        except Exception as e:
            print(f"⚠️  读取文件元数据失败: {file_path} - {e}")
        
        return metadata
    
    def scan_category(self, category: str) -> List[Dict]:
        """扫描指定分类目录"""
        resources = []
        category_path = self.root_dir / category
        
        if not category_path.exists():
            return resources
        
        for md_file in category_path.rglob("*.md"):
            # 跳过README文件
            if md_file.name.upper() == "README.MD":
                continue
            
            metadata = self.extract_metadata(md_file)
            metadata["path"] = str(md_file.relative_to(self.root_dir))
            metadata["category"] = category
            
            resources.append(metadata)
            self.stats["total_resources"] += 1
        
        self.stats["by_category"][category] = len(resources)
        return resources
    
    def generate_category_readme(self, category: str, resources: List[Dict]):
        """生成分类目录的README索引"""
        category_path = self.root_dir / category
        readme_path = category_path / "README.md"
        
        # 分类信息映射
        category_info = {
            "01-模型与研究": {
                "icon": "🔬",
                "title": "模型与研究",
                "desc": "最新AI模型、论文解读和研究报告"
            },
            "02-工具与平台": {
                "icon": "🛠️",
                "title": "工具与平台",
                "desc": "实用的开发工具、Agent框架和部署平台"
            },
            "03-教程与实践": {
                "icon": "📚",
                "title": "教程与实践",
                "desc": "从入门到精通的学习资源和最佳实践"
            },
            "04-行业洞察": {
                "icon": "💼",
                "title": "行业洞察",
                "desc": "市场分析、企业案例和趋势预测"
            },
            "05-社区资源": {
                "icon": "🌐",
                "title": "社区资源",
                "desc": "优质技术社区、博客和开源项目"
            },
            "06-每周精选": {
                "icon": "📰",
                "title": "每周精选",
                "desc": "每周AI创新资讯摘要"
            }
        }
        
        info = category_info.get(category, {"icon": "📁", "title": category, "desc": ""})
        
        content = f"""# {info['icon']} {info['title']}

> {info['desc']}

**资源总数**：{len(resources)}  
**最后更新**：{datetime.now().strftime('%Y-%m-%d')}

---

## 📚 资源列表

| 资源名称 | 类型 | 作者/机构 | 推荐指数 | 提交者 |
|---------|------|----------|----------|--------|
"""
        
        # 按评分排序
        sorted_resources = sorted(resources, key=lambda x: x.get('rating', 0), reverse=True)
        
        for res in sorted_resources:
            title = res.get('title', '未命名')
            res_type = res.get('type', '-')
            author = res.get('author', '-')
            rating = '⭐' * res.get('rating', 0) if res.get('rating', 0) > 0 else '-'
            submitter = res.get('submitter', '-')
            path = res.get('path', '')
            
            # 生成相对路径链接
            rel_path = Path(path).relative_to(category)
            content += f"| [{title}]({rel_path}) | {res_type} | {author} | {rating} | @{submitter} |\n"
        
        content += f"""
---

## 📂 子目录

"""
        
        # 列出子目录
        subdirs = [d for d in category_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
        for subdir in sorted(subdirs):
            subdir_resources = [r for r in resources if subdir.name in r.get('path', '')]
            count = len(subdir_resources)
            content += f"- **{subdir.name}/** ({count} 个资源)\n"
        
        content += f"""
---

## 🔍 快速筛选

### 按类型筛选
"""
        
        # 统计资源类型
        types = {}
        for res in resources:
            res_type = res.get('type', '其他')
            types[res_type] = types.get(res_type, 0) + 1
        
        for res_type, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
            content += f"- **{res_type}**：{count} 个\n"
        
        content += f"""
### 按标签筛选
"""
        
        # 统计标签
        tags = {}
        for res in resources:
            for tag in res.get('tags', []):
                tags[tag] = tags.get(tag, 0) + 1
        
        for tag, count in sorted(tags.items(), key=lambda x: x[1], reverse=True)[:10]:
            content += f"- #{tag}：{count} 个\n"
        
        content += """
---

## ➕ 贡献资源

欢迎贡献优质资源！请参考：
- [贡献指南](../CONTRIBUTING.md)
- [资源模板](../templates/resource-template.md)

**提交方式**：
1. Fork本仓库
2. 添加资源并更新本README
3. 提交Pull Request

或者直接[创建Issue](https://github.com/dongyunchuan/ai-innovation-resources/issues/new/choose)提交资源信息。

---

<div align="center">

[返回主页](../README.md) | [贡献指南](../CONTRIBUTING.md)

</div>
"""
        
        # 写入文件
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已更新: {readme_path}")
    
    def update_main_readme(self):
        """更新主README的统计信息"""
        main_readme = self.root_dir / "README.md"
        
        if not main_readme.exists():
            return
        
        with open(main_readme, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 更新统计数据部分
        stats_section = f"""## 📊 统计数据

> 数据由GitHub Actions自动更新（最后更新：{datetime.now().strftime('%Y-%m-%d %H:%M')}）

- 📚 总资源数：**{self.stats['total_resources']}**
- 📂 分类统计：
"""
        
        for category, count in self.stats['by_category'].items():
            stats_section += f"  - {category}：{count} 个\n"
        
        # 替换统计数据部分
        pattern = r'## 📊 统计数据.*?(?=\n##|\Z)'
        content = re.sub(pattern, stats_section, content, flags=re.DOTALL)
        
        with open(main_readme, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已更新主README统计信息")
    
    def run(self):
        """执行索引生成"""
        print("🚀 开始生成资源索引...\n")
        
        for category in self.categories:
            print(f"📂 扫描分类: {category}")
            resources = self.scan_category(category)
            
            if resources:
                self.generate_category_readme(category, resources)
            else:
                print(f"  ℹ️  暂无资源")
        
        print("\n📊 更新主README统计信息...")
        self.update_main_readme()
        
        print(f"\n✨ 完成！共处理 {self.stats['total_resources']} 个资源")
        print(f"📊 分类统计: {self.stats['by_category']}")

if __name__ == "__main__":
    indexer = ResourceIndexer()
    indexer.run()
