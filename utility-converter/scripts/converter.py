#!/usr/bin/env python3
"""
单位转换器 - 长度、重量、温度、面积、体积等
完全本地计算，无需 API
"""

import sys
import json

# 转换率（相对于基本单位）
CONVERSIONS = {
    # 长度（基本单位：米）
    "length": {
        "m": 1,
        "km": 1000,
        "cm": 0.01,
        "mm": 0.001,
        "inch": 0.0254,
        "foot": 0.3048,
        "yard": 0.9144,
        "mile": 1609.34
    },
    # 重量（基本单位：克）
    "weight": {
        "g": 1,
        "kg": 1000,
        "mg": 0.001,
        "lb": 453.592,
        "oz": 28.3495,
        "jin": 500,  # 斤
        "liang": 50  # 两
    },
    # 温度（特殊处理）
    "temperature": {
        "c": "celsius",
        "f": "fahrenheit",
        "k": "kelvin"
    },
    # 面积（基本单位：平方米）
    "area": {
        "m2": 1,
        "km2": 1e6,
        "cm2": 0.0001,
        "hectare": 10000,
        "acre": 4046.86,
        "sqft": 0.0929  # 平方英尺
    },
    # 体积（基本单位：升）
    "volume": {
        "l": 1,
        "ml": 0.001,
        "m3": 1000,
        "gal": 3.78541,  # 加仑
        "qt": 0.946353,  # 夸脱
        "pt": 0.473176,  # 品脱
        "cup": 0.236588
    },
    # 速度（基本单位：米/秒）
    "speed": {
        "m/s": 1,
        "km/h": 0.277778,
        "mph": 0.44704,
        "knot": 0.514444
    },
    # 时间（基本单位：秒）
    "time": {
        "s": 1,
        "min": 60,
        "h": 3600,
        "day": 86400,
        "week": 604800,
        "month": 2592000,  # 30 天
        "year": 31536000
    }
}

# 中文别名
ALIASES = {
    "米": "m", "公里": "km", "厘米": "cm", "毫米": "mm",
    "英寸": "inch", "英尺": "foot", "码": "yard", "英里": "mile",
    "克": "g", "千克": "kg", "公斤": "kg", "毫克": "mg",
    "磅": "lb", "盎司": "oz", "斤": "jin", "两": "liang",
    "摄氏度": "c", "华氏度": "f", "开尔文": "k",
    "平方米": "m2", "平方公里": "km2", "平方厘米": "cm2",
    "公顷": "hectare", "英亩": "acre", "平方英尺": "sqft",
    "升": "l", "毫升": "ml", "立方米": "m3",
    "加仑": "gal", "夸脱": "qt", "品脱": "pt", "杯": "cup",
    "米每秒": "m/s", "千米每小时": "km/h", "英里每小时": "mph", "节": "knot",
    "秒": "s", "分钟": "min", "小时": "h", "天": "day", "周": "week", "月": "month", "年": "year"
}


def convert(value: float, from_unit: str, to_unit: str, category: str):
    """执行转换"""
    if category not in CONVERSIONS:
        return {"ok": False, "error": f"不支持的类别：{category}"}
    
    # 温度特殊处理
    if category == "temperature":
        return convert_temperature(value, from_unit, to_unit)
    
    units = CONVERSIONS[category]
    
    # 解析单位
    from_unit = ALIASES.get(from_unit, from_unit.lower())
    to_unit = ALIASES.get(to_unit, to_unit.lower())
    
    if from_unit not in units:
        return {"ok": False, "error": f"不支持的单位：{from_unit}"}
    if to_unit not in units:
        return {"ok": False, "error": f"不支持的单位：{to_unit}"}
    
    # 转换
    base_value = value * units[from_unit]
    result = base_value / units[to_unit]
    
    return {
        "ok": True,
        "result": round(result, 6),
        "from": f"{value} {from_unit}",
        "to": f"{result:.6g} {to_unit}",
        "category": category
    }


def convert_temperature(value: float, from_unit: str, to_unit: str):
    """温度转换"""
    from_unit = ALIASES.get(from_unit, from_unit.lower())
    to_unit = ALIASES.get(to_unit, to_unit.lower())
    
    # 先转成摄氏度
    if from_unit == "c":
        celsius = value
    elif from_unit == "f":
        celsius = (value - 32) * 5/9
    elif from_unit == "k":
        celsius = value - 273.15
    else:
        return {"ok": False, "error": f"不支持的温度单位：{from_unit}"}
    
    # 再转成目标单位
    if to_unit == "c":
        result = celsius
    elif to_unit == "f":
        result = celsius * 9/5 + 32
    elif to_unit == "k":
        result = celsius + 273.15
    else:
        return {"ok": False, "error": f"不支持的温度单位：{to_unit}"}
    
    return {
        "ok": True,
        "result": round(result, 2),
        "from": f"{value}°{from_unit.upper()}",
        "to": f"{result:.2f}°{to_unit.upper()}",
        "category": "temperature"
    }


def format_result(result: dict) -> str:
    """格式化结果"""
    if not result.get("ok"):
        return f"⚠️ 转换失败：{result.get('error')}"
    
    lines = [
        "🔄 转换结果",
        "",
        f"{result['from']} = {result['to']}",
        "",
        f"类别：{result['category']}"
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(json.dumps({
            "usage": "python converter.py <数值> <原单位> <目标单位> [类别]",
            "examples": [
                "python converter.py 100 cm m length",
                "python converter.py 1 kg 斤 weight",
                "python converter.py 32 f c temperature",
                "python converter.py 100 米 公里",
                "python converter.py 1 公斤 斤"
            ],
            "categories": list(CONVERSIONS.keys()),
            "aliases": ALIASES
        }, ensure_ascii=False))
        sys.exit(1)
    
    value = float(sys.argv[1])
    from_unit = sys.argv[2]
    to_unit = sys.argv[3]
    category = sys.argv[4] if len(sys.argv) > 4 else None
    
    # 自动检测类别
    if not category:
        from_unit_check = ALIASES.get(from_unit, from_unit.lower())
        for cat, units in CONVERSIONS.items():
            if from_unit_check in units:
                category = cat
                break
    
    if not category:
        print(json.dumps({"ok": False, "error": "无法自动检测类别，请指定类别"}))
        sys.exit(1)
    
    result = convert(value, from_unit, to_unit, category)
    print(format_result(result))
