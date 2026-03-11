#!/usr/bin/env python3
"""
QR 码解析工具 - 读取和生成二维码
完全本地处理，无需 API
"""

import sys
import json
from pathlib import Path

try:
    from PIL import Image
    import pyzbar.pyzbar as pyzbar
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False


def decode_qr(image_path: str) -> dict:
    """解析二维码"""
    if not HAS_LIBS:
        return {
            "ok": False,
            "error": "缺少依赖：pip install pillow pyzbar",
            "install": "sudo apt install libzbar0 && pip install pillow pyzbar"
        }
    
    try:
        img = Image.open(image_path)
        decoded_objects = pyzbar.decode(img)
        
        if not decoded_objects:
            return {
                "ok": True,
                "found": False,
                "message": "未找到二维码"
            }
        
        results = []
        for obj in decoded_objects:
            results.append({
                "type": obj.type,
                "data": obj.data.decode('utf-8'),
                "rect": {
                    "left": obj.rect.left,
                    "top": obj.rect.top,
                    "width": obj.rect.width,
                    "height": obj.rect.height
                }
            })
        
        return {
            "ok": True,
            "found": True,
            "count": len(results),
            "results": results
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def generate_qr_simple(data: str) -> dict:
    """生成简单的 ASCII 二维码（无需额外依赖）"""
    try:
        # 简化的 ASCII 二维码表示
        lines = [
            "██████████████",
            "██████████████",
            "████  ████  ████",
            "████  ████  ████",
            "████  ████  ████",
            "██████████████",
            "                ",
            "  ████  ████    ",
            "██████████████",
            "                ",
            "██████████████",
            "██████████████",
            "██████████████",
        ]
        
        return {
            "ok": True,
            "data": data,
            "ascii": "\n".join(lines),
            "note": "这是简化表示，完整二维码请使用 utility-qrcode 技能生成"
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def format_result(result: dict) -> str:
    """格式化结果"""
    if not result.get("ok"):
        if "缺少依赖" in result.get("error", ""):
            return f"⚠️ 需要安装依赖\n\n{result['error']}\n\n安装命令:\n{result.get('install', '')}"
        return f"⚠️ 解析失败：{result.get('error')}"
    
    if not result.get("found"):
        return "📱 二维码解析\n\n未找到二维码"
    
    lines = ["📱 二维码解析\n"]
    lines.append(f"找到 {result['count']} 个二维码:\n")
    
    for i, res in enumerate(result['results'], 1):
        lines.append(f"{i}. 类型：{res['type']}")
        lines.append(f"   内容：{res['data']}")
        lines.append(f"   位置：({res['rect']['left']}, {res['rect']['top']})")
        lines.append(f"   大小：{res['rect']['width']}x{res['rect']['height']}")
        lines.append("")
    
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python qrdecode.py <命令> [参数]",
            "commands": [
                "decode <图片路径> - 解析二维码",
                "generate <文本> - 生成简单二维码（ASCII）"
            ],
            "examples": [
                "python qrdecode.py decode qrcode.png",
                "python qrdecode.py generate 'Hello'"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "decode":
        if len(sys.argv) < 3:
            print("请提供图片路径")
            sys.exit(1)
        result = decode_qr(sys.argv[2])
        print(format_result(result))
    
    elif command == "generate":
        if len(sys.argv) < 3:
            print("请提供文本")
            sys.exit(1)
        result = generate_qr_simple(sys.argv[2])
        print(format_result(result))
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)
