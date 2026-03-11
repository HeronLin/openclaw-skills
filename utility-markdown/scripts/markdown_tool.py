#!/usr/bin/env python3
"""
Markdown 处理工具 - 转换、预览、统计、格式化
完全本地处理，无需 API
"""

import sys
import json
import re
from pathlib import Path


def md_to_html(md_text: str) -> dict:
    """Markdown 转 HTML"""
    try:
        html = md_text
        
        # 标题
        html = re.sub(r'^###### (.*$)', r'<h6>\1</h6>', html, flags=re.MULTILINE)
        html = re.sub(r'^##### (.*$)', r'<h5>\1</h5>', html, flags=re.MULTILINE)
        html = re.sub(r'^#### (.*$)', r'<h4>\1</h4>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.*$)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*$)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.*$)', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        
        # 粗体和斜体
        html = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', html)
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
        
        # 链接
        html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)
        
        # 图片
        html = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1">', html)
        
        # 代码块
        html = re.sub(r'```(\w*?)\n(.*?)```', r'<pre><code class="language-\1">\2</code></pre>', html, flags=re.DOTALL)
        
        # 行内代码
        html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)
        
        # 引用
        html = re.sub(r'^> (.*$)', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
        
        # 列表
        html = re.sub(r'^[-*] (.*$)', r'<li>\1</li>', html, flags=re.MULTILINE)
        
        # 换行
        html = html.replace('\n\n', '</p><p>')
        
        return {
            "ok": True,
            "html": html,
            "original_length": len(md_text),
            "html_length": len(html)
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def count_md_elements(md_text: str) -> dict:
    """统计 Markdown 元素"""
    try:
        headings = len(re.findall(r'^#+\s', md_text, re.MULTILINE))
        links = len(re.findall(r'\[.*?\]\(.*?\)', md_text))
        images = len(re.findall(r'!\[.*?\]\(.*?\)', md_text))
        code_blocks = len(re.findall(r'```', md_text)) // 2
        lists = len(re.findall(r'^[-*]\s', md_text, re.MULTILINE))
        blockquotes = len(re.findall(r'^>\s', md_text, re.MULTILINE))
        bold = len(re.findall(r'\*\*.*?\*\*', md_text))
        italic = len(re.findall(r'\*.*?\*', md_text))
        
        # 字数统计
        words = len(md_text.split())
        chars = len(md_text)
        lines = len(md_text.split('\n'))
        
        return {
            "ok": True,
            "headings": headings,
            "links": links,
            "images": images,
            "code_blocks": code_blocks,
            "lists": lists,
            "blockquotes": blockquotes,
            "bold": bold,
            "italic": italic,
            "words": words,
            "chars": chars,
            "lines": lines
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def extract_toc(md_text: str) -> dict:
    """提取目录"""
    try:
        toc = []
        for line in md_text.split('\n'):
            match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if match:
                level = len(match.group(1))
                title = match.group(2)
                # 生成锚点
                anchor = re.sub(r'[^\w\s-]', '', title.lower())
                anchor = re.sub(r'\s+', '-', anchor)
                toc.append({
                    "level": level,
                    "title": title,
                    "anchor": anchor
                })
        
        return {
            "ok": True,
            "toc": toc,
            "count": len(toc)
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def format_md(md_text: str) -> dict:
    """格式化 Markdown"""
    try:
        # 移除多余的空行
        lines = md_text.split('\n')
        formatted_lines = []
        prev_empty = False
        
        for line in lines:
            is_empty = line.strip() == ''
            if is_empty:
                if not prev_empty:
                    formatted_lines.append('')
                prev_empty = True
            else:
                formatted_lines.append(line.rstrip())
                prev_empty = False
        
        formatted = '\n'.join(formatted_lines)
        
        return {
            "ok": True,
            "formatted": formatted,
            "original_lines": len(lines),
            "formatted_lines": len(formatted_lines)
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def format_result(result: dict, action: str) -> str:
    """格式化结果"""
    if not result.get("ok"):
        return f"⚠️ 操作失败：{result.get('error')}"
    
    if action == "tohtml":
        return f"📄 Markdown 转 HTML\n\n原始：{result['original_length']} 字符\nHTML: {result['html_length']} 字符\n\n{result['html'][:500]}{'...' if len(result['html']) > 500 else ''}"
    
    if action == "count":
        lines = [
            "📊 Markdown 统计",
            "",
            f"标题：{result['headings']}",
            f"链接：{result['links']}",
            f"图片：{result['images']}",
            f"代码块：{result['code_blocks']}",
            f"列表：{result['lists']}",
            f"引用：{result['blockquotes']}",
            f"粗体：{result['bold']}",
            f"斜体：{result['italic']}",
            "",
            f"字数：{result['words']}",
            f"字符：{result['chars']}",
            f"行数：{result['lines']}"
        ]
        return "\n".join(lines)
    
    if action == "toc":
        lines = ["📑 目录\n"]
        for item in result['toc']:
            indent = "  " * (item['level'] - 1)
            lines.append(f"{indent}- [{item['title']}](#{item['anchor']})")
        return "\n".join(lines)
    
    if action == "format":
        return f"📝 Markdown 格式化\n\n原始：{result['original_lines']} 行\n格式化后：{result['formatted_lines']} 行\n\n{result['formatted'][:500]}{'...' if len(result['formatted']) > 500 else ''}"
    
    return str(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python markdown_tool.py <命令> [参数]",
            "commands": [
                "tohtml <Markdown 文本> - 转 HTML",
                "count <Markdown 文本> - 统计元素",
                "toc <Markdown 文本> - 提取目录",
                "format <Markdown 文本> - 格式化"
            ],
            "examples": [
                "python markdown_tool.py tohtml '# Hello'",
                "python markdown_tool.py count '# Title\\n\\nContent'"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    md_text = sys.argv[2] if len(sys.argv) > 2 else ""
    
    # 处理转义字符
    md_text = md_text.replace('\\n', '\n')
    
    if command == "tohtml":
        result = md_to_html(md_text)
        print(format_result(result, "tohtml"))
    elif command == "count":
        result = count_md_elements(md_text)
        print(format_result(result, "count"))
    elif command == "toc":
        result = extract_toc(md_text)
        print(format_result(result, "toc"))
    elif command == "format":
        result = format_md(md_text)
        print(format_result(result, "format"))
    else:
        print(f"未知命令：{command}")
        sys.exit(1)
