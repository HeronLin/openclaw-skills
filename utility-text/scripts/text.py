#!/usr/bin/env python3
"""
文本处理工具 - 字数统计、文本格式化、编码转换等
完全本地处理，无需 API
"""

import sys
import json
import re
import base64
from datetime import datetime


def count_words(text: str) -> dict:
    """字数统计"""
    # 中文字符
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    # 英文字母
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    # 数字
    digits = len(re.findall(r'\d', text))
    # 标点符号
    punctuation = len(re.findall(r'[^\w\s\u4e00-\u9fff]', text))
    # 总字符
    total_chars = len(text)
    # 单词数（英文）
    english_words = len(re.findall(r'\b[a-zA-Z]+\b', text))
    # 行数
    lines = text.split('\n')
    line_count = len(lines)
    non_empty_lines = len([l for l in lines if l.strip()])
    
    return {
        "total_chars": total_chars,
        "chinese_chars": chinese_chars,
        "english_chars": english_chars,
        "digits": digits,
        "punctuation": punctuation,
        "english_words": english_words,
        "lines": line_count,
        "non_empty_lines": non_empty_lines
    }


def format_text(text: str, format_type: str = "uppercase") -> str:
    """文本格式化"""
    if format_type == "uppercase":
        return text.upper()
    elif format_type == "lowercase":
        return text.lower()
    elif format_type == "capitalize":
        return text.title()
    elif format_type == "reverse":
        return text[::-1]
    elif format_type == "remove_spaces":
        return text.replace(" ", "")
    elif format_type == "remove_newlines":
        return text.replace("\n", " ")
    elif format_type == "trim":
        return text.strip()
    else:
        return text


def encode_decode(text: str, operation: str = "base64_encode") -> dict:
    """编码/解码"""
    try:
        if operation == "base64_encode":
            encoded = base64.b64encode(text.encode()).decode()
            return {"ok": True, "operation": "Base64 编码", "result": encoded}
        elif operation == "base64_decode":
            decoded = base64.b64decode(text.encode()).decode()
            return {"ok": True, "operation": "Base64 解码", "result": decoded}
        elif operation == "url_encode":
            from urllib.parse import quote
            encoded = quote(text)
            return {"ok": True, "operation": "URL 编码", "result": encoded}
        elif operation == "url_decode":
            from urllib.parse import unquote
            decoded = unquote(text)
            return {"ok": True, "operation": "URL 解码", "result": decoded}
        else:
            return {"ok": False, "error": f"不支持的操作：{operation}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def find_replace(text: str, find: str, replace: str, case_sensitive: bool = True) -> dict:
    """查找替换"""
    try:
        if case_sensitive:
            count = text.count(find)
            result = text.replace(find, replace)
        else:
            pattern = re.compile(re.escape(find), re.IGNORECASE)
            count = len(pattern.findall(text))
            result = pattern.sub(replace, text)
        
        return {
            "ok": True,
            "find": find,
            "replace": replace,
            "count": count,
            "result": result
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def extract_info(text: str, info_type: str = "all") -> dict:
    """提取信息"""
    result = {"ok": True, "text": text[:100] + "..." if len(text) > 100 else text}
    
    if info_type in ["all", "email"]:
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        result["emails"] = list(set(emails))
    
    if info_type in ["all", "phone"]:
        phones = re.findall(r'\b1[3-9]\d{9}\b', text)
        result["phones"] = list(set(phones))
    
    if info_type in ["all", "url"]:
        urls = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', text)
        result["urls"] = list(set(urls))
    
    if info_type in ["all", "date"]:
        dates = re.findall(r'\d{4}-\d{2}-\d{2}', text)
        result["dates"] = list(set(dates))
    
    return result


def format_result(result: dict) -> str:
    """格式化结果"""
    if "total_chars" in result:
        lines = [
            "📊 字数统计",
            "",
            f"总字符：{result['total_chars']}",
            f"中文字符：{result['chinese_chars']}",
            f"英文字母：{result['english_chars']}",
            f"数字：{result['digits']}",
            f"标点符号：{result['punctuation']}",
            f"英文单词：{result['english_words']}",
            f"总行数：{result['lines']}",
            f"非空行：{result['non_empty_lines']}"
        ]
        return "\n".join(lines)
    
    if "operation" in result:
        if not result.get("ok"):
            return f"⚠️ 操作失败：{result.get('error')}"
        return f"🔄 {result['operation']}\n\n结果：{result['result']}"
    
    if "count" in result:
        return f"🔄 查找替换\n\n找到 \"{result['find']}\" {result['count']} 次\n\n替换后：\n{result['result'][:500]}"
    
    if "emails" in result:
        lines = ["📋 提取的信息", ""]
        if result.get("emails"):
            lines.append(f"📧 邮箱：{', '.join(result['emails'])}")
        if result.get("phones"):
            lines.append(f"📱 电话：{', '.join(result['phones'])}")
        if result.get("urls"):
            lines.append(f"🔗 链接：{', '.join(result['urls'])}")
        if result.get("dates"):
            lines.append(f"📅 日期：{', '.join(result['dates'])}")
        if not any([result.get("emails"), result.get("phones"), result.get("urls"), result.get("dates")]):
            lines.append("未找到相关信息")
        return "\n".join(lines)
    
    return str(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python text.py <命令> [参数]",
            "commands": [
                "count <文本> - 字数统计",
                "format <文本> <类型> - 格式化（uppercase/lowercase/capitalize/reverse）",
                "encode <文本> <类型> - 编码（base64/url）",
                "decode <文本> <类型> - 解码",
                "replace <文本> <查找> <替换> - 查找替换",
                "extract <文本> [类型] - 提取信息（email/phone/url/date/all）"
            ],
            "examples": [
                "python text.py count \"Hello World 你好世界\"",
                "python text.py format \"hello\" uppercase",
                "python text.py encode \"Hello\" base64",
                "python text.py replace \"Hello World\" \"World\" \"Python\""
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "count":
        if len(sys.argv) < 3:
            print("用法：python text.py count <文本>")
            sys.exit(1)
        text = sys.argv[2]
        result = count_words(text)
    
    elif command == "format":
        if len(sys.argv) < 4:
            print("用法：python text.py format <文本> <类型>")
            sys.exit(1)
        text = sys.argv[2]
        format_type = sys.argv[3]
        result = {"ok": True, "result": format_text(text, format_type)}
    
    elif command == "encode":
        if len(sys.argv) < 4:
            print("用法：python text.py encode <文本> <类型>")
            sys.exit(1)
        text = sys.argv[2]
        op_type = sys.argv[3]
        result = encode_decode(text, f"{op_type}_encode")
    
    elif command == "decode":
        if len(sys.argv) < 4:
            print("用法：python text.py decode <文本> <类型>")
            sys.exit(1)
        text = sys.argv[2]
        op_type = sys.argv[3]
        result = encode_decode(text, f"{op_type}_decode")
    
    elif command == "replace":
        if len(sys.argv) < 5:
            print("用法：python text.py replace <文本> <查找> <替换>")
            sys.exit(1)
        text = sys.argv[2]
        find = sys.argv[3]
        replace = sys.argv[4]
        result = find_replace(text, find, replace)
    
    elif command == "extract":
        if len(sys.argv) < 3:
            print("用法：python text.py extract <文本> [类型]")
            sys.exit(1)
        text = sys.argv[2]
        info_type = sys.argv[3] if len(sys.argv) > 3 else "all"
        result = extract_info(text, info_type)
    
    else:
        result = {"ok": False, "error": f"未知命令：{command}"}
    
    print(format_result(result))
