#!/usr/bin/env python3
"""
日历/倒计时 - 日期计算、倒数日、重要日期提醒
完全本地计算，无需 API
"""

import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

DATA_FILE = Path.home() / ".openclaw" / "workspace" / "main" / "memory" / "important_dates.json"


def load_dates():
    """加载重要日期"""
    if not DATA_FILE.exists():
        return {"dates": [], "last_update": None}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"dates": [], "last_update": None}


def save_dates(data):
    """保存重要日期"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    data["last_update"] = datetime.now().isoformat()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_weekday(date_str: str = None):
    """获取日期是星期几"""
    if not date_str:
        date_obj = datetime.now()
    else:
        try:
            # 支持多种格式
            for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d", "%Y 年%m 月%d 日"]:
                try:
                    date_obj = datetime.strptime(date_str, fmt)
                    break
                except ValueError:
                    continue
            else:
                return {"ok": False, "error": "日期格式错误，请使用 YYYY-MM-DD"}
        except Exception as e:
            return {"ok": False, "error": f"日期解析失败：{e}"}
    
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday = weekdays[date_obj.weekday()]
    
    return {
        "ok": True,
        "date": date_str or datetime.now().strftime("%Y-%m-%d"),
        "weekday": weekday,
        "is_weekend": date_obj.weekday() >= 5
    }


def days_between(date1: str, date2: str = None):
    """计算两个日期之间的天数"""
    try:
        d1 = datetime.strptime(date1, "%Y-%m-%d")
        d2 = datetime.strptime(date2, "%Y-%m-%d") if date2 else datetime.now()
        
        delta = d2 - d1
        days = delta.days
        
        return {
            "ok": True,
            "date1": date1,
            "date2": date2 or datetime.now().strftime("%Y-%m-%d"),
            "days": abs(days),
            "direction": "后" if days < 0 else "前"
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def countdown(target_date: str, event_name: str = "目标日期"):
    """倒计时"""
    try:
        target = datetime.strptime(target_date, "%Y-%m-%d")
        now = datetime.now()
        
        delta = target - now
        days = delta.days
        
        if days < 0:
            result = f"已经过去 {abs(days)} 天"
        elif days == 0:
            result = "就是今天！"
        else:
            result = f"还有 {days} 天"
        
        return {
            "ok": True,
            "event": event_name,
            "target": target_date,
            "result": result,
            "days": days
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def add_important_date(date: str, event: str, recurring: bool = False):
    """添加重要日期"""
    dates = load_dates()
    
    new_date = {
        "date": date,
        "event": event,
        "recurring": recurring,
        "added": datetime.now().isoformat()
    }
    
    dates["dates"].append(new_date)
    save_dates(dates)
    
    return f"✅ 已添加重要日期\n{date}：{event}{'（每年重复）' if recurring else ''}"


def list_important_dates():
    """列出重要日期"""
    dates = load_dates()
    
    if not dates["dates"]:
        return "📅 重要日期\n\n暂无记录"
    
    today = datetime.now()
    lines = ["📅 重要日期", ""]
    
    # 排序
    sorted_dates = sorted(dates["dates"], key=lambda x: x["date"])
    
    for d in sorted_dates:
        target = datetime.strptime(d["date"], "%Y-%m-%d")
        delta = target - today
        days = delta.days
        
        if days < 0:
            status = f"已过 {abs(days)} 天"
        elif days == 0:
            status = "🎉 就是今天！"
        else:
            status = f"还有 {days} 天"
        
        recurring = "🔄 " if d.get("recurring") else ""
        lines.append(f"{recurring}{d['date']}：{d['event']} - {status}")
    
    return "\n".join(lines)


def get_calendar(year: int = None, month: int = None):
    """获取日历"""
    if not year:
        year = datetime.now().year
    if not month:
        month = datetime.now().month
    
    # 生成日历文本
    import calendar
    cal = calendar.month(year, month)
    
    return {
        "ok": True,
        "year": year,
        "month": month,
        "calendar": cal
    }


def format_result(result: dict) -> str:
    """格式化结果"""
    if not result.get("ok"):
        return f"⚠️ 操作失败：{result.get('error')}"
    
    if "calendar" in result:
        return f"📅 {result['year']}年{result['month']}月\n\n{result['calendar']}"
    
    if "weekday" in result:
        weekend = "（周末）" if result.get("is_weekend") else ""
        return f"📅 {result['date']}\n{result['weekday']}{weekend}"
    
    if "days" in result and "date1" in result:
        return f"📅 {result['date1']} 到 {result['date2']}\n相隔 {result['days']} 天{result.get('direction', '')}"
    
    if "event" in result:
        return f"⏳ {result['event']}倒计时\n目标：{result['target']}\n{result['result']}"
    
    if "dates" in result:
        return result.get("text", "")
    
    return str(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python calendar.py <命令> [参数]",
            "commands": [
                "weekday [日期] - 获取星期几",
                "days <日期 1> [日期 2] - 计算相隔天数",
                "countdown <日期> <事件名> - 倒计时",
                "add <日期> <事件> [--recurring] - 添加重要日期",
                "list - 列出重要日期",
                "calendar [年] [月] - 显示日历"
            ],
            "examples": [
                "python calendar.py weekday",
                "python calendar.py weekday 2026-12-25",
                "python calendar.py days 2026-01-01",
                "python calendar.py countdown 2026-12-25 圣诞节",
                "python calendar.py add 2026-12-25 圣诞节",
                "python calendar.py calendar 2026 12"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "weekday":
        date = sys.argv[2] if len(sys.argv) > 2 else None
        result = get_weekday(date)
    
    elif command == "days":
        if len(sys.argv) < 3:
            print("用法：python calendar.py days <日期 1> [日期 2]")
            sys.exit(1)
        date1 = sys.argv[2]
        date2 = sys.argv[3] if len(sys.argv) > 3 else None
        result = days_between(date1, date2)
    
    elif command == "countdown":
        if len(sys.argv) < 3:
            print("用法：python calendar.py countdown <日期> [事件名]")
            sys.exit(1)
        target = sys.argv[2]
        event = sys.argv[3] if len(sys.argv) > 3 else "目标日期"
        result = countdown(target, event)
    
    elif command == "add":
        if len(sys.argv) < 4:
            print("用法：python calendar.py add <日期> <事件> [--recurring]")
            sys.exit(1)
        date = sys.argv[2]
        event = sys.argv[3]
        recurring = "--recurring" in sys.argv
        print(add_important_date(date, event, recurring))
        sys.exit(0)
    
    elif command == "list":
        print(list_important_dates())
        sys.exit(0)
    
    elif command == "calendar":
        year = int(sys.argv[2]) if len(sys.argv) > 2 else None
        month = int(sys.argv[3]) if len(sys.argv) > 3 else None
        result = get_calendar(year, month)
    
    else:
        result = {"ok": False, "error": f"未知命令：{command}"}
    
    print(format_result(result))
