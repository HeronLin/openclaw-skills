#!/usr/bin/env python3
"""
颜色工具 - 颜色格式转换、调色板生成、颜色对比度
完全本地计算，无需 API
"""

import sys
import json
import re
import colorsys


def hex_to_rgb(hex_color: str) -> dict:
    """HEX 转 RGB"""
    try:
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        return {
            "ok": True,
            "hex": f"#{hex_color.upper()}",
            "rgb": f"rgb({r}, {g}, {b})",
            "r": r,
            "g": g,
            "b": b
        }
    except Exception as e:
        return {"ok": False, "error": f"颜色格式错误：{e}"}


def rgb_to_hex(r: int, g: int, b: int) -> dict:
    """RGB 转 HEX"""
    try:
        hex_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
        
        return {
            "ok": True,
            "rgb": f"rgb({r}, {g}, {b})",
            "hex": hex_color,
            "r": r,
            "g": g,
            "b": b
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def rgb_to_hsl(r: int, g: int, b: int) -> dict:
    """RGB 转 HSL"""
    try:
        r_norm = r / 255.0
        g_norm = g / 255.0
        b_norm = b / 255.0
        
        h, l, s = colorsys.rgb_to_hls(r_norm, g_norm, b_norm)
        
        return {
            "ok": True,
            "rgb": f"rgb({r}, {g}, {b})",
            "hsl": f"hsl({int(h*360)}, {int(s*100)}%, {int(l*100)}%)",
            "h": int(h * 360),
            "s": int(s * 100),
            "l": int(l * 100)
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def generate_palette(base_hex: str, count: int = 5, palette_type: str = "analogous") -> dict:
    """生成调色板"""
    try:
        # HEX 转 RGB
        hex_color = base_hex.lstrip('#')
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        
        # RGB 转 HSL
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        
        colors = []
        
        if palette_type == "analogous":
            # 类似色
            for i in range(count):
                new_h = (h + (i - count//2) * 0.05) % 1.0
                rgb = colorsys.hls_to_rgb(new_h, l, s)
                colors.append("#{:02X}{:02X}{:02X}".format(
                    int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)
                ))
        
        elif palette_type == "complementary":
            # 互补色
            for i in range(count):
                if i % 2 == 0:
                    new_h = h
                else:
                    new_h = (h + 0.5) % 1.0
                rgb = colorsys.hls_to_rgb(new_h, l, s)
                colors.append("#{:02X}{:02X}{:02X}".format(
                    int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)
                ))
        
        elif palette_type == "triadic":
            # 三色
            for i in range(count):
                new_h = (h + i * 0.33) % 1.0
                rgb = colorsys.hls_to_rgb(new_h, l, s)
                colors.append("#{:02X}{:02X}{:02X}".format(
                    int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)
                ))
        
        elif palette_type == "monochromatic":
            # 单色
            for i in range(count):
                new_l = max(0.1, min(0.9, l + (i - count//2) * 0.1))
                rgb = colorsys.hls_to_rgb(h, new_l, s)
                colors.append("#{:02X}{:02X}{:02X}".format(
                    int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)
                ))
        
        return {
            "ok": True,
            "base": f"#{hex_color.upper()}",
            "type": palette_type,
            "count": count,
            "colors": colors
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def check_contrast(hex1: str, hex2: str) -> dict:
    """检查颜色对比度"""
    try:
        # 简化版对比度计算
        def luminance(hex_color):
            hex_color = hex_color.lstrip('#')
            r = int(hex_color[0:2], 16) / 255.0
            g = int(hex_color[2:4], 16) / 255.0
            b = int(hex_color[4:6], 16) / 255.0
            return 0.2126 * r + 0.7152 * g + 0.0722 * b
        
        l1 = luminance(hex1)
        l2 = luminance(hex2)
        
        lighter = max(l1, l2)
        darker = min(l1, l2)
        
        contrast = (lighter + 0.05) / (darker + 0.05)
        
        if contrast >= 7.0:
            rating = "AAA (优秀)"
        elif contrast >= 4.5:
            rating = "AA (良好)"
        elif contrast >= 3.0:
            rating = "AA Large (可接受)"
        else:
            rating = "Fail (不足)"
        
        return {
            "ok": True,
            "color1": hex1,
            "color2": hex2,
            "contrast": f"{contrast:.2f}:1",
            "rating": rating
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def format_result(result: dict, action: str) -> str:
    """格式化结果"""
    if not result.get("ok"):
        return f"⚠️ 操作失败：{result.get('error')}"
    
    if action == "hex2rgb":
        return f"🎨 颜色转换\n\nHEX: {result['hex']}\nRGB: {result['rgb']}"
    
    if action == "rgb2hex":
        return f"🎨 颜色转换\n\nRGB: {result['rgb']}\nHEX: {result['hex']}"
    
    if action == "rgb2hsl":
        return f"🎨 颜色转换\n\nRGB: {result['rgb']}\nHSL: {result['hsl']}"
    
    if action == "palette":
        lines = [f"🎨 调色板（{result['type']}）\n\n基础色：{result['base']}\n"]
        for i, color in enumerate(result['colors'], 1):
            lines.append(f"{i}. {color}")
        return "\n".join(lines)
    
    if action == "contrast":
        return f"🎨 对比度检查\n\n颜色 1: {result['color1']}\n颜色 2: {result['color2']}\n\n对比度：{result['contrast']}\n评级：{result['rating']}"
    
    return str(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python color_tool.py <命令> [参数]",
            "commands": [
                "hex2rgb <HEX> - HEX 转 RGB",
                "rgb2hex <R> <G> <B> - RGB 转 HEX",
                "rgb2hsl <R> <G> <B> - RGB 转 HSL",
                "palette <HEX> [类型] [数量] - 生成调色板",
                "contrast <HEX1> <HEX2> - 检查对比度"
            ],
            "examples": [
                "python color_tool.py hex2rgb #FF5733",
                "python color_tool.py rgb2hex 255 87 51",
                "python color_tool.py palette #FF5733 analogous 5",
                "python color_tool.py contrast #FFFFFF #000000"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "hex2rgb":
        if len(sys.argv) < 3:
            print("请提供 HEX 颜色")
            sys.exit(1)
        result = hex_to_rgb(sys.argv[2])
        print(format_result(result, "hex2rgb"))
    
    elif command == "rgb2hex":
        if len(sys.argv) < 5:
            print("请提供 R G B 值")
            sys.exit(1)
        result = rgb_to_hex(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
        print(format_result(result, "rgb2hex"))
    
    elif command == "rgb2hsl":
        if len(sys.argv) < 5:
            print("请提供 R G B 值")
            sys.exit(1)
        result = rgb_to_hsl(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
        print(format_result(result, "rgb2hsl"))
    
    elif command == "palette":
        if len(sys.argv) < 3:
            print("请提供基础颜色")
            sys.exit(1)
        base = sys.argv[2]
        ptype = sys.argv[3] if len(sys.argv) > 3 else "analogous"
        count = int(sys.argv[4]) if len(sys.argv) > 4 else 5
        result = generate_palette(base, count, ptype)
        print(format_result(result, "palette"))
    
    elif command == "contrast":
        if len(sys.argv) < 4:
            print("请提供两个颜色")
            sys.exit(1)
        result = check_contrast(sys.argv[2], sys.argv[3])
        print(format_result(result, "contrast"))
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)
