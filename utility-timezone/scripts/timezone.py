#!/usr/bin/env python3
"""
时区转换工具 - 世界时间查询、时区转换
完全本地计算，无需 API
"""

import sys
import json
from datetime import datetime, timedelta
import re

# 常见时区偏移（小时）
TIMEZONES = {
    "UTC": 0,
    "GMT": 0,
    "CST": 8,      # 中国标准时间
    "Beijing": 8,
    "Shanghai": 8,
    "Tokyo": 9,
    "Seoul": 9,
    "Singapore": 8,
    "HongKong": 8,
    "Taipei": 8,
    "Bangkok": 7,
    "Jakarta": 7,
    "Manila": 8,
    "KualaLumpur": 8,
    "Sydney": 10,
    "Melbourne": 10,
    "Auckland": 12,
    "London": 0,
    "Paris": 1,
    "Berlin": 1,
    "Rome": 1,
    "Madrid": 1,
    "Amsterdam": 1,
    "Moscow": 3,
    "Dubai": 4,
    "Mumbai": 5.5,
    "Karachi": 5,
    "Dhaka": 6,
    "NewYork": -5,
    "LosAngeles": -8,
    "Chicago": -6,
    "Houston": -6,
    "Phoenix": -7,
    "Toronto": -5,
    "Vancouver": -8,
    "MexicoCity": -6,
    "SaoPaulo": -3,
    "BuenosAires": -3,
    "Cairo": 2,
    "Johannesburg": 2,
    "Lagos": 1
}


def get_timezone_offset(tz_name: str) -> float:
    """获取时区偏移"""
    tz_name = tz_name.strip()
    
    # 检查预定义时区
    if tz_name in TIMEZONES:
        return TIMEZONES[tz_name]
    
    # 解析 +/-HH:MM 格式
    match = re.match(r'^([+-])(\d{1,2}):?(\d{2})?$', tz_name)
    if match:
        sign = 1 if match.group(1) == '+' else -1
        hours = int(match.group(2))
        minutes = int(match.group(3) or 0)
        return sign * (hours + minutes / 60)
    
    # 解析 +/-HH 格式
    match = re.match(r'^([+-])(\d{1,2})$', tz_name)
    if match:
        sign = 1 if match.group(1) == '+' else -1
        return sign * int(match.group(2))
    
    raise ValueError(f"未知时区：{tz_name}")


def convert_time(time_str: str, from_tz: str, to_tz: str) -> dict:
    """转换时间"""
    try:
        # 解析时间
        time_formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y/%m/%d %H:%M:%S",
            "%Y/%m/%d %H:%M",
            "%H:%M:%S",
            "%H:%M"
        ]
        
        parsed_time = None
        for fmt in time_formats:
            try:
                parsed_time = datetime.strptime(time_str, fmt)
                break
            except ValueError:
                continue
        
        if not parsed_time:
            return {"ok": False, "error": f"无法解析时间：{time_str}"}
        
        # 获取时区偏移
        from_offset = get_timezone_offset(from_tz)
        to_offset = get_timezone_offset(to_tz)
        
        # 计算时间差
        time_diff = to_offset - from_offset
        
        # 转换时间
        converted = parsed_time + timedelta(hours=time_diff)
        
        # 确定日期变化
        date_change = ""
        if converted.date() > parsed_time.date():
            date_change = "（+1 天）" if (converted.date() - parsed_time.date()).days == 1 else f"（+{converted.date() - parsed_time.date()}天）"
        elif converted.date() < parsed_time.date():
            date_change = "（-1 天）" if (parsed_time.date() - converted.date()).days == 1 else f"（-{parsed_time.date() - converted.date()}天）"
        
        return {
            "ok": True,
            "original": {
                "time": time_str,
                "timezone": from_tz,
                "offset": f"UTC{'+' if from_offset >= 0 else ''}{from_offset}"
            },
            "converted": {
                "time": converted.strftime("%Y-%m-%d %H:%M:%S") if parsed_time.year != 1900 else converted.strftime("%H:%M:%S"),
                "timezone": to_tz,
                "offset": f"UTC{'+' if to_offset >= 0 else ''}{to_offset}"
            },
            "time_diff": f"{time_diff:+.1f}小时",
            "date_change": date_change
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def current_time(tz_name: str) -> dict:
    """获取当前时间"""
    try:
        now = datetime.utcnow()
        offset = get_timezone_offset(tz_name)
        local_time = now + timedelta(hours=offset)
        
        # 判断是否周末
        is_weekend = local_time.weekday() >= 5
        weekday = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][local_time.weekday()]
        
        return {
            "ok": True,
            "timezone": tz_name,
            "offset": f"UTC{'+' if offset >= 0 else ''}{offset}",
            "time": local_time.strftime("%Y-%m-%d %H:%M:%S"),
            "weekday": weekday,
            "is_weekend": is_weekend
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def list_timezones() -> dict:
    """列出支持的时区"""
    return {
        "ok": True,
        "count": len(TIMEZONES),
        "timezones": TIMEZONES
    }


def format_result(result: dict, action: str) -> str:
    """格式化结果"""
    if not result.get("ok"):
        return f"⚠️ 操作失败：{result.get('error')}"
    
    if action == "convert":
        lines = [
            "🌍 时区转换",
            "",
            f"原始时间：{result['original']['time']} ({result['original']['timezone']} {result['original']['offset']})",
            f"转换后：{result['converted']['time']} ({result['converted']['timezone']} {result['converted']['offset']})",
            f"时差：{result['time_diff']}",
        ]
        if result.get('date_change'):
            lines.append(f"日期变化：{result['date_change']}")
        return "\n".join(lines)
    
    if action == "current":
        weekend = "（周末）" if result['is_weekend'] else ""
        return f"🌍 当前时间\n\n{result['timezone']} ({result['offset']})\n\n{result['time']}\n{result['weekday']}{weekend}"
    
    if action == "list":
        lines = [f"🌍 支持的时区（共{result['count']}个）\n"]
        for tz, offset in sorted(result['timezones'].items(), key=lambda x: x[1], reverse=True):
            lines.append(f"UTC{'+' if offset >= 0 else ''}{offset}: {tz}")
        return "\n".join(lines)
    
    return str(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python timezone.py <命令> [参数]",
            "commands": [
                "convert <时间> <from 时区> <to 时区>",
                "now <时区> - 当前时间",
                "list - 列出时区"
            ],
            "examples": [
                "python timezone.py convert '2026-03-11 12:00' Beijing NewYork",
                "python timezone.py now Tokyo",
                "python timezone.py list"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "convert":
        if len(sys.argv) < 5:
            print("用法：python timezone.py convert <时间> <from 时区> <to 时区>")
            sys.exit(1)
        time_str = sys.argv[2]
        from_tz = sys.argv[3]
        to_tz = sys.argv[4]
        result = convert_time(time_str, from_tz, to_tz)
        print(format_result(result, "convert"))
    
    elif command == "now":
        if len(sys.argv) < 3:
            print("用法：python timezone.py now <时区>")
            sys.exit(1)
        result = current_time(sys.argv[2])
        print(format_result(result, "current"))
    
    elif command == "list":
        result = list_timezones()
        print(format_result(result, "list"))
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)
