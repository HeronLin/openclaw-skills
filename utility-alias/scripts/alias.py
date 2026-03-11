#!/usr/bin/env python3
"""
快捷别名工具 - 为常用命令创建别名
解决命令太长记不住的问题
"""

import sys
import json
from pathlib import Path
from datetime import datetime

DATA_FILE = Path.home() / ".openclaw" / "workspace" / "main" / "memory" / "aliases.json"


def load_aliases():
    """加载别名"""
    if not DATA_FILE.exists():
        return {"aliases": {}, "last_update": None}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"aliases": {}, "last_update": None}


def save_aliases(data):
    """保存别名"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    data["last_update"] = datetime.now().isoformat()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_alias(name: str, command: str) -> dict:
    """添加别名"""
    aliases = load_aliases()
    aliases["aliases"][name] = command
    save_aliases(aliases)
    return {"ok": True, "name": name, "command": command}


def remove_alias(name: str) -> dict:
    """删除别名"""
    aliases = load_aliases()
    if name in aliases["aliases"]:
        del aliases["aliases"][name]
        save_aliases(aliases)
        return {"ok": True, "name": name}
    return {"ok": False, "error": f"别名不存在：{name}"}


def list_aliases() -> dict:
    """列出别名"""
    aliases = load_aliases()
    return {"ok": True, "aliases": aliases["aliases"], "count": len(aliases["aliases"])}


def get_alias(name: str) -> dict:
    """获取别名"""
    aliases = load_aliases()
    if name in aliases["aliases"]:
        return {"ok": True, "name": name, "command": aliases["aliases"][name]}
    return {"ok": False, "error": f"别名不存在：{name}"}


def format_result(result: dict, action: str) -> str:
    """格式化结果"""
    if not result.get("ok"):
        return f"⚠️ 操作失败：{result.get('error')}"
    
    if action == "add":
        return f"✅ 已添加别名\n\n{result['name']} => {result['command']}"
    
    if action == "remove":
        return f"✅ 已删除别名：{result['name']}"
    
    if action == "list":
        if not result["aliases"]:
            return "📋 别名列表\n\n暂无别名"
        
        lines = ["📋 别名列表\n"]
        for name, command in sorted(result["aliases"].items()):
            lines.append(f"{name:15} => {command}")
        lines.append(f"\n共 {result['count']} 个别名")
        return "\n".join(lines)
    
    if action == "get":
        return f"📋 别名查询\n\n{result['name']} => {result['command']}"
    
    return str(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python alias.py <命令> [参数]",
            "commands": [
                "add <别名> <命令> - 添加别名",
                "remove <别名> - 删除别名",
                "list - 列出所有别名",
                "get <别名> - 查询别名"
            ],
            "examples": [
                "python alias.py add ll 'ls -la'",
                "python alias.py add gs 'git status'",
                "python alias.py list"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "add":
        if len(sys.argv) < 4:
            print("用法：python alias.py add <别名> <命令>")
            sys.exit(1)
        name = sys.argv[2]
        cmd = sys.argv[3]
        result = add_alias(name, cmd)
        print(format_result(result, "add"))
    
    elif command == "remove":
        if len(sys.argv) < 3:
            print("用法：python alias.py remove <别名>")
            sys.exit(1)
        result = remove_alias(sys.argv[2])
        print(format_result(result, "remove"))
    
    elif command == "list":
        result = list_aliases()
        print(format_result(result, "list"))
    
    elif command == "get":
        if len(sys.argv) < 3:
            print("用法：python alias.py get <别名>")
            sys.exit(1)
        result = get_alias(sys.argv[2])
        print(format_result(result, "get"))
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)
