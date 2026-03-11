#!/usr/bin/env python3
"""
实用计算器 - 数学计算、单位换算、日期计算
完全本地计算，无需 API
"""

import sys
import json
import math
import re
from datetime import datetime, timedelta


def calculate(expression: str) -> dict:
    """计算数学表达式"""
    try:
        # 安全的表达式求值
        allowed_chars = set('0123456789+-*/.() math.sin math.cos math.tan math.sqrt math.pow math.pi math.e')
        
        # 替换常用函数
        expr = expression.replace('^', '**')
        expr = expr.replace('sin', 'math.sin')
        expr = expr.replace('cos', 'math.cos')
        expr = expr.replace('tan', 'math.tan')
        expr = expr.replace('sqrt', 'math.sqrt')
        expr = expr.replace('pi', 'math.pi')
        
        # 安全检查
        result = eval(expr, {"__builtins__": {}, "math": math}, {})
        
        return {
            "ok": True,
            "expression": expression,
            "result": result
        }
    except Exception as e:
        return {"ok": False, "error": f"计算错误：{e}"}


def percentage(value: float, total: float) -> dict:
    """计算百分比"""
    try:
        pct = (value / total) * 100
        return {
            "ok": True,
            "value": value,
            "total": total,
            "percentage": f"{pct:.2f}%"
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def date_diff(date1: str, date2: str) -> dict:
    """计算日期差"""
    try:
        d1 = datetime.strptime(date1, "%Y-%m-%d")
        d2 = datetime.strptime(date2, "%Y-%m-%d")
        
        delta = d2 - d1
        days = delta.days
        
        return {
            "ok": True,
            "date1": date1,
            "date2": date2,
            "days": abs(days),
            "direction": "后" if days < 0 else "前"
        }
    except Exception as e:
        return {"ok": False, "error": f"日期格式错误，请使用 YYYY-MM-DD: {e}"}


def date_add(date: str, days: int) -> dict:
    """日期加减"""
    try:
        d = datetime.strptime(date, "%Y-%m-%d")
        new_date = d + timedelta(days=days)
        
        return {
            "ok": True,
            "original": date,
            "days": days,
            "result": new_date.strftime("%Y-%m-%d")
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def bmi(weight: float, height: float) -> dict:
    """计算 BMI"""
    try:
        # height 单位是 cm
        height_m = height / 100
        bmi_value = weight / (height_m ** 2)
        
        if bmi_value < 18.5:
            category = "偏瘦"
        elif bmi_value < 24:
            category = "正常"
        elif bmi_value < 28:
            category = "偏胖"
        else:
            category = "肥胖"
        
        return {
            "ok": True,
            "weight": weight,
            "height": height,
            "bmi": f"{bmi_value:.1f}",
            "category": category
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def format_result(result: dict, calc_type: str) -> str:
    """格式化结果"""
    if not result.get("ok"):
        return f"⚠️ 计算失败：{result.get('error')}"
    
    if calc_type == "calc":
        return f"🧮 计算结果\n\n{result['expression']} = {result['result']}"
    
    if calc_type == "percentage":
        return f"📊 百分比计算\n\n{result['value']} 占 {result['total']} 的 {result['percentage']}"
    
    if calc_type == "date_diff":
        return f"📅 日期差\n\n{result['date1']} 到 {result['date2']}\n相隔 {result['days']} 天{result.get('direction', '')}"
    
    if calc_type == "date_add":
        return f"📅 日期计算\n\n{result['original']} {'+' if result['days'] > 0 else ''}{result['days']}天 = {result['result']}"
    
    if calc_type == "bmi":
        return f"🏃 BMI 计算\n\n体重：{result['weight']}kg\n身高：{result['height']}cm\n\nBMI: {result['bmi']}\n类别：{result['category']}"
    
    return str(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python calc.py <命令> [参数]",
            "commands": [
                "calc <表达式> - 数学计算",
                "percent <值> <总数> - 百分比",
                "datediff <日期 1> <日期 2> - 日期差",
                "dateadd <日期> <天数> - 日期加减",
                "bmi <体重 kg> <身高 cm> - BMI 计算"
            ],
            "examples": [
                "python calc.py calc \"2+3*4\"",
                "python calc.py percent 50 200",
                "python calc.py datediff 2026-01-01 2026-12-31",
                "python calc.py bmi 70 175"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "calc":
        if len(sys.argv) < 3:
            print("请提供表达式")
            sys.exit(1)
        result = calculate(sys.argv[2])
        print(format_result(result, "calc"))
    
    elif command == "percent":
        if len(sys.argv) < 4:
            print("请提供值和总数")
            sys.exit(1)
        result = percentage(float(sys.argv[2]), float(sys.argv[3]))
        print(format_result(result, "percentage"))
    
    elif command == "datediff":
        if len(sys.argv) < 4:
            print("请提供两个日期")
            sys.exit(1)
        result = date_diff(sys.argv[2], sys.argv[3])
        print(format_result(result, "date_diff"))
    
    elif command == "dateadd":
        if len(sys.argv) < 4:
            print("请提供日期和天数")
            sys.exit(1)
        result = date_add(sys.argv[2], int(sys.argv[3]))
        print(format_result(result, "date_add"))
    
    elif command == "bmi":
        if len(sys.argv) < 4:
            print("请提供体重和身高")
            sys.exit(1)
        result = bmi(float(sys.argv[2]), float(sys.argv[3]))
        print(format_result(result, "bmi"))
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)
