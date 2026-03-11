#!/usr/bin/env python3
"""
命令历史工具 - 记录和搜索使用过的命令
解决找不到之前命令的问题
"""

import sys
import json
from pathlib import Path
from datetime import datetime
import readline

DATA_FILE = Path.home() / ".openclaw" / "workspace" / "main" / "memory" / "cmd_history.json"
MAX_HISTORY = 1000


def load_history():
    """加载历史"""
    if not DATA_FILE.exists():
        return {"commands": [], "last_update": None}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"commands": [], "last_update": None}


def save_history(data):
    """保存历史"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    data["last_update"] = datetime.now().isoformat()
    # 限制历史记录数量
    data["commands"] = data["commands"][-MAX_HISTORY:]
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_command(command: str) -> dict:
    """添加命令到历史"""
    history = load_history()
    
    # 避免重复
    if history["commands"] and history["commands"][-1] == command:
        return {"ok": True, "command": command, "message": "已存在"}
    
    history["commands"].append({
        "command": command,
        "timestamp": datetime.now().isoformat()
    })
    save_history(history)
    
    return {"ok": True, "command": command}


def search_history(keyword: str, limit: int = 10) -> dict:
    """搜索历史命令"""
    history = load_history()
    
    matched = []
    for cmd in reversed(history["commands"]):
        if keyword.lower() in cmd["command"].lower():
            matched.append(cmd)
            if len(matched) >= limit:
                break
    
    return {
        "ok": True,
        "keyword": keyword,
        "count": len(matched),
        "results": matched
    }


def list_history(limit: int = 20) -> dict:
    """列出最近命令"""
    history = load_history()
    
    recent = history["commands"][-limit:]
    
    return {
        "ok": True,
        "count": len(recent),
        "results": recent
    }


def clear_history() -> dict:
    """清空历史"""
    save_history({"commands": [], "last_update": datetime.now().isoformat()})
    return {"ok": True, "message": "已清空历史记录"}


def format_result(result: dict, action: str) -> str:
    """格式化结果"""
    if not result.get("ok"):
        return f"⚠️ 操作失败：{result.get('error')}"
    
    if action == "add":
        return f"✅ 已记录命令\n\n{result['command']}"
    
    if action == "search":
        if not result["results"]:
            return f"🔍 搜索 \"{result['keyword']}\"\n\n未找到匹配的命令"
        
        lines = [f"🔍 搜索 \"{result['keyword']}\"（找到{result['count']}条）\n"]
        for i, cmd in enumerate(result["results"], 1):
            time_str = cmd["timestamp"][:16].replace("T", " ")
            lines.append(f"{i}. [{time_str}] {cmd['command']}")
        
        return "\n".join(lines)
    
    if action == "list":
        if not result["results"]:
            return "📋 命令历史\n\n暂无历史记录"
        
        lines = ["📋 最近命令\n"]
        for i, cmd in enumerate(reversed(result["results"]), 1):
            time_str = cmd["timestamp"][:16].replace("T", " ")
            lines.append(f"{i}. [{time_str}] {cmd['command']}")
        
        return "\n".join(lines)
    
    if action == "clear":
        return "✅ 已清空历史记录"
    
    return str(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python cmdhistory.py <命令> [参数]",
            "commands": [
                "add <命令> - 添加命令到历史",
                "search <关键词> - 搜索历史命令",
                "list [数量] - 列出最近命令",
                "clear - 清空历史"
            ],
            "examples": [
                "python cmdhistory.py add 'git commit -m \"fix bug\"'",
                "python cmdhistory.py search git",
                "python cmdhistory.py list 10"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "add":
        if len(sys.argv) < 3:
            print("请提供命令")
            sys.exit(1)
        result = add_command(sys.argv[2])
        print(format_result(result, "add"))
    
    elif command == "search":
        if len(sys.argv) < 3:
            print("请提供关键词")
            sys.exit(1)
        result = search_history(sys.argv[2])
        print(format_result(result, "search"))
    
    elif command == "list":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20
        result = list_history(limit)
        print(format_result(result, "list"))
    
    elif command == "clear":
        result = clear_history()
        print(format_result(result, "clear"))
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)
