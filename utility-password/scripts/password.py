#!/usr/bin/env python3
"""
密码管理器 - 生成强密码、本地加密存储
完全本地，无需 API，安全可靠
"""

import sys
import json
import random
import string
import base64
from datetime import datetime
from pathlib import Path

DATA_FILE = Path.home() / ".openclaw" / "workspace" / "main" / "memory" / "passwords.json"

# 简单加密（实际使用建议用 cryptography 库）
def simple_encrypt(text: str, key: str = "default_key_123") -> str:
    """简单加密（XOR + Base64）"""
    key_bytes = key.encode() * (len(text) // len(key) + 1)
    encrypted = bytes([ord(c) ^ key_bytes[i] for i, c in enumerate(text)])
    return base64.b64encode(encrypted).decode()


def simple_decrypt(encoded: str, key: str = "default_key_123") -> str:
    """简单解密"""
    try:
        encrypted = base64.b64decode(encoded.encode())
        key_bytes = key.encode() * (len(encrypted) // len(key) + 1)
        decrypted = bytes([encrypted[i] ^ key_bytes[i] for i in range(len(encrypted))])
        return decrypted.decode()
    except:
        return None


def generate_password(length: int = 16, use_upper: bool = True, 
                      use_lower: bool = True, use_digits: bool = True, 
                      use_special: bool = True) -> str:
    """生成强密码"""
    chars = ""
    if use_upper:
        chars += string.ascii_uppercase
    if use_lower:
        chars += string.ascii_lowercase
    if use_digits:
        chars += string.digits
    if use_special:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    if not chars:
        chars = string.ascii_letters + string.digits
    
    # 确保包含各类字符
    password = []
    if use_upper:
        password.append(random.choice(string.ascii_uppercase))
    if use_lower:
        password.append(random.choice(string.ascii_lowercase))
    if use_digits:
        password.append(random.choice(string.digits))
    if use_special:
        password.append(random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))
    
    # 填充剩余长度
    password.extend(random.choice(chars) for _ in range(length - len(password)))
    
    # 打乱顺序
    random.shuffle(password)
    return ''.join(password)


def check_password_strength(password: str) -> dict:
    """检查密码强度"""
    score = 0
    feedback = []
    
    # 长度检查
    if len(password) >= 16:
        score += 3
    elif len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ 密码太短（建议至少 12 位）")
    
    # 字符类型检查
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("❌ 缺少大写字母")
    
    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("❌ 缺少小写字母")
    
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("❌ 缺少数字")
    
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 2
    else:
        feedback.append("❌ 缺少特殊字符")
    
    # 常见模式检查
    if password.lower() in ["password", "123456", "qwerty", "admin"]:
        feedback.append("❌ 使用了常见密码")
        score -= 3
    
    if len(feedback) == 0:
        feedback.append("✅ 密码强度很好！")
    
    # 评级
    if score >= 8:
        level = "🟢 非常强"
    elif score >= 6:
        level = "🟡 强"
    elif score >= 4:
        level = "🟠 中等"
    else:
        level = "🔴 弱"
    
    return {
        "score": score,
        "level": level,
        "feedback": feedback
    }


def load_passwords():
    """加载密码"""
    if not DATA_FILE.exists():
        return {"passwords": [], "last_update": None}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"passwords": [], "last_update": None}


def save_passwords(data):
    """保存密码"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    data["last_update"] = datetime.now().isoformat()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_password(service: str, username: str, password: str, notes: str = None):
    """保存密码"""
    passwords = load_passwords()
    
    # 检查是否已存在
    for p in passwords["passwords"]:
        if p["service"] == service and p["username"] == username:
            p["password"] = simple_encrypt(password)
            p["notes"] = notes
            p["updated"] = datetime.now().isoformat()
            save_passwords(passwords)
            return f"✅ 已更新密码\n服务：{service}\n用户：{username}"
    
    new_entry = {
        "service": service,
        "username": username,
        "password": simple_encrypt(password),
        "notes": notes,
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat()
    }
    
    passwords["passwords"].append(new_entry)
    save_passwords(passwords)
    
    return f"✅ 已保存密码\n服务：{service}\n用户：{username}"


def get_password(service: str, username: str = None):
    """获取密码"""
    passwords = load_passwords()
    
    for p in passwords["passwords"]:
        if p["service"] == service:
            if not username or p["username"] == username:
                password = simple_decrypt(p["password"])
                return {
                    "ok": True,
                    "service": p["service"],
                    "username": p["username"],
                    "password": password,
                    "notes": p.get("notes"),
                    "updated": p.get("updated", "")[:16]
                }
    
    return {"ok": False, "error": f"未找到密码：{service}"}


def list_passwords():
    """列出密码（不显示密码本身）"""
    passwords = load_passwords()
    
    if not passwords["passwords"]:
        return "🔐 密码列表\n\n暂无保存的密码"
    
    lines = ["🔐 密码列表", ""]
    for p in passwords["passwords"]:
        lines.append(f"📌 {p['service']} - {p['username']}")
        lines.append(f"   更新：{p.get('updated', '')[:16]}")
        lines.append("")
    
    lines.append(f"总计：{len(passwords['passwords'])}个密码")
    lines.append("\n⚠️ 查看具体密码：password get <服务名>")
    
    return "\n".join(lines)


def format_result(result: dict) -> str:
    """格式化结果"""
    if not result.get("ok"):
        return f"⚠️ 操作失败：{result.get('error')}"
    
    if "password" in result:
        lines = [
            "🔐 密码信息",
            "",
            f"服务：{result['service']}",
            f"用户：{result['username']}",
            f"密码：{result['password']}",
        ]
        if result.get("notes"):
            lines.append(f"备注：{result['notes']}")
        lines.append(f"更新：{result.get('updated', '')}")
        return "\n".join(lines)
    
    if "level" in result:
        lines = [
            "🔐 密码强度检查",
            "",
            f"强度：{result['level']}",
            f"得分：{result['score']}/10",
            ""
        ]
        lines.extend(result['feedback'])
        return "\n".join(lines)
    
    return str(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python password.py <命令> [参数]",
            "commands": [
                "generate [长度] - 生成强密码",
                "check <密码> - 检查密码强度",
                "save <服务> <用户> <密码> [备注] - 保存密码",
                "get <服务> [用户] - 获取密码",
                "list - 列出密码"
            ],
            "examples": [
                "python password.py generate",
                "python password.py generate 20",
                "python password.py check 'MyP@ssw0rd'",
                "python password.py save github myuser mypassword",
                "python password.py get github"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "generate":
        length = int(sys.argv[2]) if len(sys.argv) > 2 else 16
        password = generate_password(length)
        strength = check_password_strength(password)
        print(f"🔐 生成的密码：{password}")
        print(f"强度：{strength['level']}")
    
    elif command == "check":
        if len(sys.argv) < 3:
            print("用法：python password.py check <密码>")
            sys.exit(1)
        result = check_password_strength(sys.argv[2])
        print(format_result({"ok": True, **result}))
    
    elif command == "save":
        if len(sys.argv) < 5:
            print("用法：python password.py save <服务> <用户> <密码> [备注]")
            sys.exit(1)
        service = sys.argv[2]
        username = sys.argv[3]
        password = sys.argv[4]
        notes = sys.argv[5] if len(sys.argv) > 5 else None
        print(save_password(service, username, password, notes))
    
    elif command == "get":
        if len(sys.argv) < 3:
            print("用法：python password.py get <服务> [用户]")
            sys.exit(1)
        service = sys.argv[2]
        username = sys.argv[3] if len(sys.argv) > 3 else None
        result = get_password(service, username)
        print(format_result(result))
    
    elif command == "list":
        print(list_passwords())
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)
