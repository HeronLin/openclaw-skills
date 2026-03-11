#!/usr/bin/env python3
"""
待办事项管理 - 添加/完成/删除/查看任务
支持优先级、截止日期、分类
"""

import json
import sys
from datetime import datetime
from pathlib import Path

DATA_FILE = Path.home() / ".openclaw" / "workspace" / "main" / "memory" / "todos.json"


def load_todos():
    """加载待办事项"""
    if not DATA_FILE.exists():
        return {"todos": [], "last_update": None}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"todos": [], "last_update": None}


def save_todos(data):
    """保存待办事项"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    data["last_update"] = datetime.now().isoformat()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_todo(text: str, priority: str = "medium", due_date: str = None):
    """添加待办"""
    todos = load_todos()
    
    new_todo = {
        "id": len(todos["todos"]) + 1,
        "text": text,
        "priority": priority,
        "due_date": due_date,
        "created": datetime.now().isoformat(),
        "completed": False
    }
    
    todos["todos"].append(new_todo)
    save_todos(todos)
    
    return f"✅ 已添加待办 #{new_todo['id']}\n内容：{text}\n优先级：{priority}"


def complete_todo(todo_id: int):
    """完成任务"""
    todos = load_todos()
    
    for todo in todos["todos"]:
        if todo["id"] == todo_id:
            todo["completed"] = True
            todo["completed_at"] = datetime.now().isoformat()
            save_todos(todos)
            return f"✅ 已完成 #{todo_id}\n内容：{todo['text']}"
    
    return f"❌ 未找到任务 #{todo_id}"


def delete_todo(todo_id: int):
    """删除任务"""
    todos = load_todos()
    
    for i, todo in enumerate(todos["todos"]):
        if todo["id"] == todo_id:
            removed = todos["todos"].pop(i)
            save_todos(todos)
            return f"✅ 已删除 #{todo_id}\n内容：{removed['text']}"
    
    return f"❌ 未找到任务 #{todo_id}"


def list_todos(show_completed: bool = False):
    """列出待办"""
    todos = load_todos()
    
    if not todos["todos"]:
        return "📋 待办事项\n\n暂无待办"
    
    # 过滤
    active = [t for t in todos["todos"] if not t["completed"]]
    completed = [t for t in todos["todos"] if t["completed"]]
    
    lines = ["📋 待办事项", ""]
    
    if active:
        lines.append("🔴 进行中:")
        for todo in sorted(active, key=lambda x: x["id"], reverse=True):
            priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(todo["priority"], "⚪")
            due = f" (截止：{todo['due_date']})" if todo.get("due_date") else ""
            lines.append(f"  {priority_icon} #{todo['id']}: {todo['text']}{due}")
        lines.append("")
    
    if show_completed and completed:
        lines.append("✅ 已完成:")
        for todo in completed[-5:]:  # 只显示最近 5 个
            lines.append(f"  ✅ #{todo['id']}: {todo['text']}")
    
    lines.append(f"\n总计：{len(active)} 进行中 / {len(completed)} 已完成")
    
    return "\n".join(lines)


def analyze_todos():
    """分析待办"""
    todos = load_todos()
    
    if not todos["todos"]:
        return "📊 待办分析\n\n暂无待办"
    
    total = len(todos["todos"])
    completed = sum(1 for t in todos["todos"] if t["completed"])
    active = total - completed
    
    high_priority = sum(1 for t in todos["todos"] if not t["completed"] and t["priority"] == "high")
    
    # 过期任务
    today = datetime.now().strftime("%Y-%m-%d")
    overdue = sum(1 for t in todos["todos"] if not t["completed"] and t.get("due_date") and t["due_date"] < today)
    
    lines = [
        "📊 待办分析",
        "",
        f"总任务：{total}",
        f"已完成：{completed} ({completed/total*100:.1f}%)",
        f"进行中：{active}",
        f"高优先级：{high_priority}",
        f"已过期：{overdue}",
        ""
    ]
    
    if overdue > 0:
        lines.append("⚠️ 有任务已过期，请尽快处理！")
    if high_priority > 0:
        lines.append("🔴 有高优先级任务待处理！")
    if active == 0:
        lines.append("🎉 所有任务已完成！")
    
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python todo.py <命令> [参数]",
            "commands": [
                "add <内容> [--priority high/medium/low] [--due YYYY-MM-DD]",
                "complete <ID>",
                "delete <ID>",
                "list [--all]",
                "analyze"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "add":
        if len(sys.argv) < 3:
            print("用法：python todo.py add <内容> [参数]")
            sys.exit(1)
        text = sys.argv[2]
        priority = "medium"
        due_date = None
        
        if "--priority" in sys.argv:
            idx = sys.argv.index("--priority")
            if idx + 1 < len(sys.argv):
                priority = sys.argv[idx + 1]
        
        if "--due" in sys.argv:
            idx = sys.argv.index("--due")
            if idx + 1 < len(sys.argv):
                due_date = sys.argv[idx + 1]
        
        print(add_todo(text, priority, due_date))
    
    elif command == "complete":
        if len(sys.argv) < 3:
            print("用法：python todo.py complete <ID>")
            sys.exit(1)
        print(complete_todo(int(sys.argv[2])))
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("用法：python todo.py delete <ID>")
            sys.exit(1)
        print(delete_todo(int(sys.argv[2])))
    
    elif command == "list":
        show_all = "--all" in sys.argv
        print(list_todos(show_all))
    
    elif command == "analyze":
        print(analyze_todos())
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
