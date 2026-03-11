#!/usr/bin/env python3
"""
图片处理 - 压缩、转换、调整大小、添加水印
使用 Pillow 库
"""

import sys
import os
from pathlib import Path
from datetime import datetime

try:
    from PIL import Image
except ImportError:
    print(json.dumps({"error": "Pillow 未安装", "install": "pip install Pillow"}))
    sys.exit(1)

import json


def compress_image(input_path: str, output_path: str, quality: int = 80):
    """压缩图片"""
    try:
        img = Image.open(input_path)
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        
        img.save(output_path, 'JPEG', quality=quality, optimize=True)
        
        original_size = os.path.getsize(input_path)
        new_size = os.path.getsize(output_path)
        compression = (1 - new_size / original_size) * 100
        
        return {
            "ok": True,
            "message": f"✅ 压缩成功",
            "original_size": f"{original_size / 1024:.1f}KB",
            "new_size": f"{new_size / 1024:.1f}KB",
            "compression": f"{compression:.1f}%"
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def convert_format(input_path: str, output_format: str):
    """转换图片格式"""
    try:
        img = Image.open(input_path)
        input_name = Path(input_path).stem
        output_path = f"{input_name}.{output_format.lower()}"
        
        if output_format.upper() == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        
        img.save(output_path, output_format.upper())
        
        return {
            "ok": True,
            "message": f"✅ 格式转换成功",
            "output": output_path,
            "format": output_format.upper()
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def resize_image(input_path: str, width: int = None, height: int = None):
    """调整图片大小"""
    try:
        img = Image.open(input_path)
        orig_width, orig_height = img.size
        
        if width and height:
            new_size = (width, height)
        elif width:
            ratio = width / orig_width
            new_size = (width, int(orig_height * ratio))
        elif height:
            ratio = height / orig_height
            new_size = (int(orig_width * ratio), height)
        else:
            return {"ok": False, "error": "请指定宽度或高度"}
        
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        input_name = Path(input_path).stem
        output_path = f"{input_name}_{width}x{height}.jpg"
        img.save(output_path, 'JPEG', quality=85)
        
        return {
            "ok": True,
            "message": f"✅ 调整大小成功",
            "output": output_path,
            "original": f"{orig_width}x{orig_height}",
            "new": f"{new_size[0]}x{new_size[1]}"
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def add_watermark(input_path: str, text: str, position: str = "br"):
    """添加文字水印"""
    try:
        img = Image.open(input_path)
        from PIL import ImageDraw, ImageFont
        
        # 创建透明图层
        txt_layer = Image.new('RGBA', img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)
        
        # 尝试加载中文字体
        font_paths = [
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "C:/Windows/Fonts/simhei.ttf"
        ]
        
        font = None
        for fp in font_paths:
            if os.path.exists(fp):
                font = ImageFont.truetype(fp, 36)
                break
        
        if not font:
            font = ImageFont.load_default()
        
        # 获取文字大小
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # 计算位置
        padding = 20
        if position == "br":  # 右下
            x = img.width - text_width - padding
            y = img.height - text_height - padding
        elif position == "bl":  # 左下
            x = padding
            y = img.height - text_height - padding
        elif position == "tr":  # 右上
            x = img.width - text_width - padding
            y = padding
        else:  # tl 左上
            x = padding
            y = padding
        
        # 绘制文字
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 180))
        
        # 合并图层
        img = img.convert('RGBA')
        watermarked = Image.alpha_composite(img, txt_layer)
        
        input_name = Path(input_path).stem
        output_path = f"{input_name}_watermarked.png"
        watermarked.save(output_path, 'PNG')
        
        return {
            "ok": True,
            "message": f"✅ 添加水印成功",
            "output": output_path,
            "text": text,
            "position": position
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python image.py <命令> [参数]",
            "commands": [
                "compress <图片路径> [质量 1-100]",
                "convert <图片路径> <格式 jpg/png/webp>",
                "resize <图片路径> --width <宽> --height <高>",
                "watermark <图片路径> <文字> [位置 tl/tr/bl/br]"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "compress":
        if len(sys.argv) < 3:
            print("用法：python image.py compress <图片路径> [质量]")
            sys.exit(1)
        input_path = sys.argv[2]
        quality = int(sys.argv[3]) if len(sys.argv) > 3 else 80
        output_path = Path(input_path).stem + "_compressed.jpg"
        result = compress_image(input_path, output_path, quality)
    
    elif command == "convert":
        if len(sys.argv) < 4:
            print("用法：python image.py convert <图片路径> <格式>")
            sys.exit(1)
        input_path = sys.argv[2]
        output_format = sys.argv[3]
        result = convert_format(input_path, output_format)
    
    elif command == "resize":
        if len(sys.argv) < 3:
            print("用法：python image.py resize <图片路径> --width <宽> --height <高>")
            sys.exit(1)
        input_path = sys.argv[2]
        width = int(sys.argv[4]) if "--width" in sys.argv else None
        height = int(sys.argv[6]) if "--height" in sys.argv else None
        result = resize_image(input_path, width, height)
    
    elif command == "watermark":
        if len(sys.argv) < 4:
            print("用法：python image.py watermark <图片路径> <文字> [位置]")
            sys.exit(1)
        input_path = sys.argv[2]
        text = sys.argv[3]
        position = sys.argv[4] if len(sys.argv) > 4 else "br"
        result = add_watermark(input_path, text, position)
    
    else:
        result = {"ok": False, "error": f"未知命令：{command}"}
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
