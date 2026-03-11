#!/usr/bin/env python3
"""
二维码生成 - 生成 URL、文本、WiFi 等二维码
支持自定义颜色、Logo、尺寸
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

try:
    import qrcode
    from qrcode.constants import ERROR_CORRECT_H
except ImportError:
    print(json.dumps({"error": "qrcode 未安装", "install": "pip install qrcode[pil]"}))
    sys.exit(1)


def generate_qrcode(data: str, output_path: str = None, size: int = 10, 
                    fill_color: str = "black", back_color: str = "white"):
    """生成二维码"""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=ERROR_CORRECT_H,
            box_size=size,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"qrcode_{timestamp}.png"
        
        img.save(output_path)
        
        return {
            "ok": True,
            "message": "✅ 二维码生成成功",
            "output": output_path,
            "data": data[:50] + "..." if len(data) > 50 else data,
            "size": f"{img.size[0]}x{img.size[1]}"
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def generate_wifi_qrcode(ssid: str, password: str, encryption: str = "WPA", output_path: str = None):
    """生成 WiFi 二维码"""
    try:
        # WiFi 二维码格式
        wifi_data = f"WIFI:T:{encryption};S:{ssid};P:{password};;"
        return generate_qrcode(wifi_data, output_path)
    except Exception as e:
        return {"ok": False, "error": str(e)}


def generate_vcard_qrcode(name: str, phone: str, email: str = None, output_path: str = None):
    """生成名片二维码"""
    try:
        vcard = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nTEL:{phone}"
        if email:
            vcard += f"\nEMAIL:{email}"
        vcard += "\nEND:VCARD"
        return generate_qrcode(vcard, output_path)
    except Exception as e:
        return {"ok": False, "error": str(e)}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python qrcode.py <类型> <内容> [参数]",
            "types": [
                "text <文本> - 生成文本二维码",
                "url <网址> - 生成 URL 二维码",
                "wifi <SSID> <密码> [加密方式] - 生成 WiFi 二维码",
                "vcard <姓名> <电话> [邮箱] - 生成名片二维码"
            ],
            "options": [
                "--output <路径> - 输出文件路径",
                "--size <1-20> - 二维码大小（默认 10）",
                "--color <颜色> - 前景色（默认 black）",
                "--bg <颜色> - 背景色（默认 white）"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    qrcode_type = sys.argv[1]
    
    if qrcode_type == "text":
        if len(sys.argv) < 3:
            print("用法：python qrcode.py text <文本>")
            sys.exit(1)
        data = sys.argv[2]
        result = generate_qrcode(data)
    
    elif qrcode_type == "url":
        if len(sys.argv) < 3:
            print("用法：python qrcode.py url <网址>")
            sys.exit(1)
        data = sys.argv[2]
        result = generate_qrcode(data)
    
    elif qrcode_type == "wifi":
        if len(sys.argv) < 4:
            print("用法：python qrcode.py wifi <SSID> <密码> [加密方式]")
            sys.exit(1)
        ssid = sys.argv[2]
        password = sys.argv[3]
        encryption = sys.argv[4] if len(sys.argv) > 4 else "WPA"
        result = generate_wifi_qrcode(ssid, password, encryption)
    
    elif qrcode_type == "vcard":
        if len(sys.argv) < 4:
            print("用法：python qrcode.py vcard <姓名> <电话> [邮箱]")
            sys.exit(1)
        name = sys.argv[2]
        phone = sys.argv[3]
        email = sys.argv[4] if len(sys.argv) > 4 else None
        result = generate_vcard_qrcode(name, phone, email)
    
    else:
        result = {"ok": False, "error": f"未知类型：{qrcode_type}"}
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
