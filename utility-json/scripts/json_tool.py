#!/usr/bin/env python3
"""
JSON 处理工具 - 格式化、验证、提取、转换
完全本地处理，无需 API
"""

import sys
import json


def format_json(text: str, indent: int = 2) -> dict:
    """格式化 JSON"""
    try:
        data = json.loads(text)
        formatted = json.dumps(data, indent=indent, ensure_ascii=False)
        return {"ok": True, "formatted": formatted}
    except json.JSONDecodeError as e:
        return {"ok": False, "error": f"JSON 格式错误：{e}"}


def validate_json(text: str) -> dict:
    """验证 JSON"""
    try:
        json.loads(text)
        return {"ok": True, "message": "✅ JSON 格式正确"}
    except json.JSONDecodeError as e:
        return {"ok": False, "error": f"❌ JSON 格式错误：{e}"}


def extract_value(text: str, key_path: str) -> dict:
    """提取 JSON 值"""
    try:
        data = json.loads(text)
        keys = key_path.split(".")
        value = data
        for key in keys:
            if isinstance(value, dict):
                value = value[key]
            elif isinstance(value, list):
                value = value[int(key)]
            else:
                return {"ok": False, "error": f"路径错误：{key_path}"}
        return {"ok": True, "key": key_path, "value": value}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def json_to_csv(text: str) -> dict:
    """JSON 转 CSV"""
    try:
        data = json.loads(text)
        if not isinstance(data, list):
            data = [data]
        
        if not data:
            return {"ok": False, "error": "空数据"}
        
        # 获取所有键
        headers = set()
        for item in data:
            if isinstance(item, dict):
                headers.update(item.keys())
        headers = sorted(headers)
        
        # 生成 CSV
        lines = [",".join(headers)]
        for item in data:
            if isinstance(item, dict):
                row = [str(item.get(h, "")) for h in headers]
                lines.append(",".join(row))
        
        return {"ok": True, "csv": "\n".join(lines)}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def minify_json(text: str) -> dict:
    """压缩 JSON"""
    try:
        data = json.loads(text)
        minified = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
        original_len = len(text)
        new_len = len(minified)
        compression = (1 - new_len / original_len) * 100
        return {
            "ok": True,
            "minified": minified,
            "original_len": original_len,
            "new_len": new_len,
            "compression": f"{compression:.1f}%"
        }
    except json.JSONDecodeError as e:
        return {"ok": False, "error": f"JSON 格式错误：{e}"}


def format_result(result: dict) -> str:
    """格式化结果"""
    if not result.get("ok"):
        return f"⚠️ 操作失败：{result.get('error')}"
    
    if "formatted" in result:
        return f"📄 JSON 格式化\n\n{result['formatted']}"
    
    if "message" in result:
        return f"📄 JSON 验证\n\n{result['message']}"
    
    if "value" in result:
        value_str = json.dumps(result["value"], ensure_ascii=False) if isinstance(result["value"], (dict, list)) else str(result["value"])
        return f"📄 提取值\n\n路径：{result['key']}\n值：{value_str}"
    
    if "csv" in result:
        return f"📄 JSON 转 CSV\n\n{result['csv']}"
    
    if "minified" in result:
        return f"📄 JSON 压缩\n\n原始：{result['original_len']} 字节\n压缩后：{result['new_len']} 字节\n压缩率：{result['compression']}\n\n结果：{result['minified']}"
    
    return str(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python json_tool.py <命令> [参数]",
            "commands": [
                "format <JSON> - 格式化 JSON",
                "validate <JSON> - 验证 JSON",
                "extract <JSON> <路径> - 提取值（如：data.items.0.name）",
                "tocsv <JSON> - JSON 转 CSV",
                "minify <JSON> - 压缩 JSON"
            ],
            "examples": [
                "python json_tool.py format '{\"name\":\"test\",\"value\":123}'",
                "python json_tool.py extract '{\"user\":{\"name\":\"John\"}}' user.name"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if len(sys.argv) < 3:
        print("请提供 JSON 数据")
        sys.exit(1)
    
    json_text = sys.argv[2]
    
    if command == "format":
        result = format_json(json_text)
    elif command == "validate":
        result = validate_json(json_text)
    elif command == "extract":
        if len(sys.argv) < 4:
            print("请提供路径")
            sys.exit(1)
        result = extract_value(json_text, sys.argv[3])
    elif command == "tocsv":
        result = json_to_csv(json_text)
    elif command == "minify":
        result = minify_json(json_text)
    else:
        result = {"ok": False, "error": f"未知命令：{command}"}
    
    print(format_result(result))
