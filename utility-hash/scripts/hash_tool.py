#!/usr/bin/env python3
"""
哈希计算工具 - MD5、SHA1、SHA256 等哈希算法
完全本地计算，无需 API
"""

import sys
import json
import hashlib
from pathlib import Path


def hash_text(text: str, algorithm: str = "md5") -> dict:
    """计算文本哈希"""
    try:
        algorithms = {
            "md5": hashlib.md5,
            "sha1": hashlib.sha1,
            "sha256": hashlib.sha256,
            "sha512": hashlib.sha512
        }
        
        if algorithm.lower() not in algorithms:
            return {"ok": False, "error": f"不支持的算法：{algorithm}"}
        
        hash_obj = algorithms[algorithm.lower()](text.encode())
        
        return {
            "ok": True,
            "algorithm": algorithm.upper(),
            "text": text[:50] + "..." if len(text) > 50 else text,
            "hash": hash_obj.hexdigest(),
            "length": len(text)
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def hash_file(file_path: str, algorithm: str = "md5") -> dict:
    """计算文件哈希"""
    try:
        algorithms = {
            "md5": hashlib.md5,
            "sha1": hashlib.sha1,
            "sha256": hashlib.sha256,
            "sha512": hashlib.sha512
        }
        
        if algorithm.lower() not in algorithms:
            return {"ok": False, "error": f"不支持的算法：{algorithm}"}
        
        input_path = Path(file_path)
        if not input_path.exists():
            return {"ok": False, "error": f"文件不存在：{file_path}"}
        
        hash_obj = algorithms[algorithm.lower()]()
        
        # 分块读取大文件
        with open(input_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        
        file_size = input_path.stat().st_size
        
        return {
            "ok": True,
            "algorithm": algorithm.upper(),
            "file": file_path,
            "hash": hash_obj.hexdigest(),
            "size": f"{file_size / 1024:.1f}KB" if file_size < 1048576 else f"{file_size / 1048576:.1f}MB"
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def compare_hashes(hash1: str, hash2: str) -> dict:
    """比较两个哈希值"""
    match = hash1.lower().strip() == hash2.lower().strip()
    return {
        "ok": True,
        "hash1": hash1,
        "hash2": hash2,
        "match": match,
        "message": "✅ 哈希值匹配" if match else "❌ 哈希值不匹配"
    }


def format_result(result: dict) -> str:
    """格式化结果"""
    if not result.get("ok"):
        return f"⚠️ 操作失败：{result.get('error')}"
    
    if "hash" in result and "text" in result:
        return f"🔐 {result['algorithm']} 哈希\n\n文本：{result['text']}\n\n哈希值：\n{result['hash']}\n\n长度：{result['length']} 字符"
    
    if "hash" in result and "file" in result:
        return f"🔐 {result['algorithm']} 哈希（文件）\n\n文件：{result['file']}\n大小：{result['size']}\n\n哈希值：\n{result['hash']}"
    
    if "match" in result:
        status = "✅ 匹配" if result["match"] else "❌ 不匹配"
        return f"🔐 哈希比对\n\n哈希 1：{result['hash1']}\n哈希 2：{result['hash2']}\n\n结果：{status}"
    
    return str(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python hash_tool.py <命令> [参数]",
            "commands": [
                "text <文本> [算法] - 计算文本哈希（md5/sha1/sha256/sha512）",
                "file <文件> [算法] - 计算文件哈希",
                "compare <哈希 1> <哈希 2> - 比较哈希值"
            ],
            "examples": [
                "python hash_tool.py text 'Hello World'",
                "python hash_tool.py text 'Hello World' sha256",
                "python hash_tool.py file test.txt md5",
                "python hash_tool.py compare abc123 abc123"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "text":
        if len(sys.argv) < 3:
            print("请提供文本")
            sys.exit(1)
        text = sys.argv[2]
        algorithm = sys.argv[3] if len(sys.argv) > 3 else "md5"
        result = hash_text(text, algorithm)
    
    elif command == "file":
        if len(sys.argv) < 3:
            print("请提供文件路径")
            sys.exit(1)
        file_path = sys.argv[2]
        algorithm = sys.argv[3] if len(sys.argv) > 3 else "md5"
        result = hash_file(file_path, algorithm)
    
    elif command == "compare":
        if len(sys.argv) < 4:
            print("请提供两个哈希值")
            sys.exit(1)
        result = compare_hashes(sys.argv[2], sys.argv[3])
    
    else:
        result = {"ok": False, "error": f"未知命令：{command}"}
    
    print(format_result(result))
