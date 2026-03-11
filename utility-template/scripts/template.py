#!/usr/bin/env python3
"""
快捷模板工具 - 为常用文本创建模板
解决重复输入的问题
"""

import sys
import json
from pathlib import Path
from datetime import datetime

DATA_FILE = Path.home() / ".openclaw" / "workspace" / "main" / "memory" / "templates.json"


def load_templates():
    """加载模板"""
    if not DATA_FILE.exists():
        return {"templates": {}, "last_update": None}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"templates": {}, "last_update": None}


def save_templates(data):
    """保存模板"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    data["last_update"] = datetime.now().isoformat()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_template(name: str, content: str, description: str = "") -> dict:
    """添加模板"""
    templates = load_templates()
    templates["templates"][name] = {
        "content": content,
        "description": description,
        "created": datetime.now().isoformat()
    }
    save_templates(templates)
    return {"ok": True, "name": name, "content": content}


def get_template(name: str) -> dict:
    """获取模板"""
    templates = load_templates()
    if name in templates["templates"]:
        return {"ok": True, "name": name, **templates["templates"][name]}
    return {"ok": False, "error": f"模板不存在：{name}"}


def list_templates() -> dict:
    """列出模板"""
    templates = load_templates()
    return {"ok": True, "templates": templates["templates"], "count": len(templates["templates"])}


def remove_template(name: str) -> dict:
    """删除模板"""
    templates = load_templates()
    if name in templates["templates"]:
        del templates["templates"][name]
        save_templates(templates)
        return {"ok": True, "name": name}
    return {"ok": False, "error": f"模板不存在：{name}"}


def format_result(result: dict, action: str) -> str:
    """格式化结果"""
    if not result.get("ok"):
        return f"⚠️ 操作失败：{result.get('error')}"
    
    if action == "add":
        return f"✅ 已添加模板\n\n名称：{result['name']}\n\n内容：\n{result['content']}"
    
    if action == "get":
        desc = f"\n描述：{result['description']}" if result.get('description') else ""
        created = f"\n创建：{result['created'][:16]}" if result.get('created') else ""
        return f"📄 模板：{result['name']}{desc}{created}\n\n{result['content']}"
    
    if action == "list":
        if not result["templates"]:
            return "📄 模板列表\n\n暂无模板"
        
        lines = ["📄 模板列表\n"]
        for name, data in sorted(result["templates"].items()):
            desc = data.get("description", "")[:30]
            lines.append(f"{name:15} - {desc}")
        lines.append(f"\n共 {result['count']} 个模板")
        return "\n".join(lines)
    
    if action == "remove":
        return f"✅ 已删除模板：{result['name']}"
    
    return str(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python template.py <命令> [参数]",
            "commands": [
                "add <名称> <内容> [描述] - 添加模板",
                "get <名称> - 获取模板",
                "list - 列出所有模板",
                "remove <名称> - 删除模板"
            ],
            "examples": [
                "python template.py add email '尊敬的客户：\\n\\n您好！' '邮件开头'",
                "python template.py get email",
                "python template.py list"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "add":
        if len(sys.argv) < 4:
            print("用法：python template.py add <名称> <内容> [描述]")
            sys.exit(1)
        name = sys.argv[2]
        content = sys.argv[3]
        desc = sys.argv[4] if len(sys.argv) > 4 else ""
        content = content.replace("\\n", "\n")
        result = add_template(name, content, desc)
        print(format_result(result, "add"))
    
    elif command == "get":
        if len(sys.argv) < 3:
            print("用法：python template.py get <名称>")
            sys.exit(1)
        result = get_template(sys.argv[2])
        print(format_result(result, "get"))
    
    elif command == "list":
        result = list_templates()
        print(format_result(result, "list"))
    
    elif command == "remove":
        if len(sys.argv) < 3:
            print("用法：python template.py remove <名称>")
            sys.exit(1)
        result = remove_template(sys.argv[2])
        print(format_result(result, "remove"))
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)
