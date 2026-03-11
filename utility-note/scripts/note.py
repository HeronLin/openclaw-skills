#!/usr/bin/env python3
"""
笔记/备忘录 - 快速记录、查看、管理笔记
本地存储，无需 API
"""

import json
import sys
from datetime import datetime
from pathlib import Path

DATA_FILE = Path.home() / ".openclaw" / "workspace" / "main" / "memory" / "notes.json"


def load_notes():
    """加载笔记"""
    if not DATA_FILE.exists():
        return {"notes": [], "last_update": None}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"notes": [], "last_update": None}


def save_notes(data):
    """保存笔记"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    data["last_update"] = datetime.now().isoformat()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_note(title: str, content: str, tags: list = None):
    """添加笔记"""
    notes = load_notes()
    
    new_note = {
        "id": len(notes["notes"]) + 1,
        "title": title,
        "content": content,
        "tags": tags or [],
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat()
    }
    
    notes["notes"].append(new_note)
    save_notes(notes)
    
    return f"✅ 已添加笔记 #{new_note['id']}\n标题：{title}\n标签：{', '.join(tags) if tags else '无'}"


def view_note(note_id: int):
    """查看笔记"""
    notes = load_notes()
    
    for note in notes["notes"]:
        if note["id"] == note_id:
            lines = [
                f"📝 笔记 #{note['id']}",
                "",
                f"标题：{note['title']}",
                f"创建：{note['created'][:16]}",
                f"标签：{', '.join(note['tags']) if note['tags'] else '无'}",
                "",
                "-" * 40,
                note['content'],
                "-" * 40
            ]
            return "\n".join(lines)
    
    return f"❌ 未找到笔记 #{note_id}"


def list_notes(tag: str = None, limit: int = 10):
    """列出笔记"""
    notes = load_notes()
    
    if not notes["notes"]:
        return "📝 笔记列表\n\n暂无笔记"
    
    # 过滤
    filtered = notes["notes"]
    if tag:
        filtered = [n for n in filtered if tag in n.get("tags", [])]
    
    # 排序（最新的在前）
    filtered = sorted(filtered, key=lambda x: x["created"], reverse=True)
    
    lines = ["📝 笔记列表", ""]
    for note in filtered[:limit]:
        tags = f" [{', '.join(note['tags'][:2])}]" if note.get("tags") else ""
        lines.append(f"📌 #{note['id']}: {note['title']}{tags}")
        lines.append(f"   创建：{note['created'][:16]}")
        lines.append("")
    
    if len(filtered) > limit:
        lines.append(f"... 还有 {len(filtered) - limit} 条笔记")
    
    return "\n".join(lines)


def search_notes(keyword: str):
    """搜索笔记"""
    notes = load_notes()
    
    if not notes["notes"]:
        return "🔍 搜索笔记\n\n暂无笔记"
    
    # 搜索标题和内容
    matched = []
    for note in notes["notes"]:
        if keyword.lower() in note["title"].lower() or keyword.lower() in note["content"].lower():
            matched.append(note)
    
    if not matched:
        return f"🔍 搜索笔记\n\n未找到包含 \"{keyword}\" 的笔记"
    
    lines = [f"🔍 搜索 \"{keyword}\"", "", f"找到 {len(matched)} 条笔记:", ""]
    for note in matched[:10]:
        tags = f" [{', '.join(note['tags'][:2])}]" if note.get("tags") else ""
        lines.append(f"📌 #{note['id']}: {note['title']}{tags}")
        # 显示内容片段
        content_preview = note["content"][:50].replace("\n", " ")
        lines.append(f"   {content_preview}...")
        lines.append("")
    
    return "\n".join(lines)


def delete_note(note_id: int):
    """删除笔记"""
    notes = load_notes()
    
    for i, note in enumerate(notes["notes"]):
        if note["id"] == note_id:
            removed = notes["notes"].pop(i)
            save_notes(notes)
            return f"✅ 已删除笔记 #{note_id}\n标题：{removed['title']}"
    
    return f"❌ 未找到笔记 #{note_id}"


def analyze_notes():
    """分析笔记"""
    notes = load_notes()
    
    if not notes["notes"]:
        return "📊 笔记分析\n\n暂无笔记"
    
    total = len(notes["notes"])
    
    # 统计标签
    tag_count = {}
    for note in notes["notes"]:
        for tag in note.get("tags", []):
            tag_count[tag] = tag_count.get(tag, 0) + 1
    
    top_tags = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)[:5]
    
    lines = [
        "📊 笔记分析",
        "",
        f"总笔记数：{total}",
        f"标签数：{len(tag_count)}",
        ""
    ]
    
    if top_tags:
        lines.append("常用标签:")
        for tag, count in top_tags:
            lines.append(f"  #{tag}: {count}条")
    
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python note.py <命令> [参数]",
            "commands": [
                "add <标题> <内容> [--tags 标签 1,标签 2]",
                "view <ID> - 查看笔记",
                "list [--tag 标签] [--limit 数量]",
                "search <关键词>",
                "delete <ID>",
                "analyze"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "add":
        if len(sys.argv) < 4:
            print("用法：python note.py add <标题> <内容> [--tags 标签]")
            sys.exit(1)
        title = sys.argv[2]
        content = sys.argv[3]
        tags = []
        if "--tags" in sys.argv:
            idx = sys.argv.index("--tags")
            if idx + 1 < len(sys.argv):
                tags = sys.argv[idx + 1].split(",")
        print(add_note(title, content, tags))
    
    elif command == "view":
        if len(sys.argv) < 3:
            print("用法：python note.py view <ID>")
            sys.exit(1)
        print(view_note(int(sys.argv[2])))
    
    elif command == "list":
        tag = None
        limit = 10
        if "--tag" in sys.argv:
            idx = sys.argv.index("--tag")
            if idx + 1 < len(sys.argv):
                tag = sys.argv[idx + 1]
        if "--limit" in sys.argv:
            idx = sys.argv.index("--limit")
            if idx + 1 < len(sys.argv):
                limit = int(sys.argv[idx + 1])
        print(list_notes(tag, limit))
    
    elif command == "search":
        if len(sys.argv) < 3:
            print("用法：python note.py search <关键词>")
            sys.exit(1)
        print(search_notes(sys.argv[2]))
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("用法：python note.py delete <ID>")
            sys.exit(1)
        print(delete_note(int(sys.argv[2])))
    
    elif command == "analyze":
        print(analyze_notes())
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
