#!/usr/bin/env python3
"""
Base64 编解码工具 - 编码、解码、文件处理
完全本地处理，无需 API
"""

import sys
import json
import base64
from pathlib import Path


def encode_text(text: str) -> dict:
    """编码文本"""
    try:
        encoded = base64.b64encode(text.encode()).decode()
        return {
            "ok": True,
            "operation": "Base64 编码",
            "original": text,
            "encoded": encoded,
            "original_len": len(text),
            "encoded_len": len(encoded)
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def decode_text(encoded: str) -> dict:
    """解码文本"""
    try:
        decoded = base64.b64decode(encoded.encode()).decode()
        return {
            "ok": True,
            "operation": "Base64 解码",
            "encoded": encoded,
            "decoded": decoded,
            "encoded_len": len(encoded),
            "decoded_len": len(decoded)
        }
    except Exception as e:
        return {"ok": False, "error": f"解码失败：{e}"}


def encode_file(file_path: str, output_path: str = None) -> dict:
    """编码文件"""
    try:
        input_path = Path(file_path)
        if not input_path.exists():
            return {"ok": False, "error": f"文件不存在：{file_path}"}
        
        with open(input_path, "rb") as f:
            file_data = f.read()
        
        encoded = base64.b64encode(file_data).decode()
        
        if not output_path:
            output_path = str(input_path) + ".b64"
        
        with open(output_path, "w") as f:
            f.write(encoded)
        
        original_size = len(file_data)
        encoded_size = len(encoded)
        
        return {
            "ok": True,
            "operation": "文件 Base64 编码",
            "input": file_path,
            "output": output_path,
            "original_size": f"{original_size / 1024:.1f}KB",
            "encoded_size": f"{encoded_size / 1024:.1f}KB"
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def decode_file(encoded_path: str, output_path: str = None) -> dict:
    """解码文件"""
    try:
        input_path = Path(encoded_path)
        if not input_path.exists():
            return {"ok": False, "error": f"文件不存在：{encoded_path}"}
        
        with open(input_path, "r") as f:
            encoded_data = f.read().strip()
        
        decoded_data = base64.b64decode(encoded_data)
        
        if not output_path:
            # 移除 .b64 后缀
            output_path = str(input_path)[:-4] if str(input_path).endswith(".b64") else str(input_path) + ".decoded"
        
        with open(output_path, "wb") as f:
            f.write(decoded_data)
        
        return {
            "ok": True,
            "operation": "文件 Base64 解码",
            "input": encoded_path,
            "output": output_path,
            "decoded_size": f"{len(decoded_data) / 1024:.1f}KB"
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def format_result(result: dict) -> str:
    """格式化结果"""
    if not result.get("ok"):
        return f"⚠️ 操作失败：{result.get('error')}"
    
    if "encoded" in result and "decoded" not in result:
        return f"🔐 Base64 编码\n\n原始：{result['original'][:50]}{'...' if len(result['original']) > 50 else ''}\n\n编码后：\n{result['encoded']}\n\n原始长度：{result['original_len']} 字节\n编码后：{result['encoded_len']} 字节"
    
    if "decoded" in result:
        return f"🔓 Base64 解码\n\n解码后：\n{result['decoded']}\n\n原始长度：{result['encoded_len']} 字节\n解码后：{result['decoded_len']} 字节"
    
    if "output" in result:
        return f"✅ {result['operation']}\n\n输入：{result['input']}\n输出：{result['output']}\n大小：{result.get('original_size', result.get('decoded_size', 'N/A'))}"
    
    return str(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python base64_tool.py <命令> [参数]",
            "commands": [
                "encode <文本> - 编码文本",
                "decode <Base64> - 解码文本",
                "encodefile <文件> [输出] - 编码文件",
                "decodefile <文件> [输出] - 解码文件"
            ],
            "examples": [
                "python base64_tool.py encode 'Hello World'",
                "python base64_tool.py decode 'SGVsbG8gV29ybGQ='",
                "python base64_tool.py encodefile test.txt",
                "python base64_tool.py decodefile test.txt.b64"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "encode":
        if len(sys.argv) < 3:
            print("请提供要编码的文本")
            sys.exit(1)
        result = encode_text(sys.argv[2])
    
    elif command == "decode":
        if len(sys.argv) < 3:
            print("请提供 Base64 编码")
            sys.exit(1)
        result = decode_text(sys.argv[2])
    
    elif command == "encodefile":
        if len(sys.argv) < 3:
            print("请提供文件路径")
            sys.exit(1)
        output = sys.argv[3] if len(sys.argv) > 3 else None
        result = encode_file(sys.argv[2], output)
    
    elif command == "decodefile":
        if len(sys.argv) < 3:
            print("请提供文件路径")
            sys.exit(1)
        output = sys.argv[3] if len(sys.argv) > 3 else None
        result = decode_file(sys.argv[2], output)
    
    else:
        result = {"ok": False, "error": f"未知命令：{command}"}
    
    print(format_result(result))
