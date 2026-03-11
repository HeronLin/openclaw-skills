#!/usr/bin/env python3
"""
汇率转换工具 - 货币转换、汇率查询
使用固定汇率（离线模式），无需 API
"""

import sys
import json
from datetime import datetime

# 近似汇率（相对于 USD，实际使用应更新）
EXCHANGE_RATES = {
    "USD": 1.0,
    "CNY": 7.23,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 149.5,
    "KRW": 1320.0,
    "HKD": 7.82,
    "TWD": 31.5,
    "SGD": 1.34,
    "THB": 35.8,
    "MYR": 4.72,
    "INR": 83.0,
    "IDR": 15650.0,
    "PHP": 56.0,
    "VND": 24500.0,
    "AUD": 1.53,
    "NZD": 1.63,
    "CAD": 1.36,
    "CHF": 0.88,
    "SEK": 10.5,
    "NOK": 10.7,
    "DKK": 6.87,
    "RUB": 92.0,
    "BRL": 4.97,
    "MXN": 17.1,
    "ZAR": 19.2,
    "TRY": 31.5,
    "AED": 3.67,
    "SAR": 3.75
}


def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """货币转换"""
    try:
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        if from_currency not in EXCHANGE_RATES:
            return {"ok": False, "error": f"不支持的货币：{from_currency}"}
        if to_currency not in EXCHANGE_RATES:
            return {"ok": False, "error": f"不支持的货币：{to_currency}"}
        
        # 转换为 USD，再转换为目标货币
        usd_amount = amount / EXCHANGE_RATES[from_currency]
        result_amount = usd_amount * EXCHANGE_RATES[to_currency]
        
        # 计算汇率
        exchange_rate = EXCHANGE_RATES[to_currency] / EXCHANGE_RATES[from_currency]
        
        return {
            "ok": True,
            "amount": amount,
            "from": from_currency,
            "to": to_currency,
            "result": round(result_amount, 2),
            "rate": round(exchange_rate, 4),
            "note": "汇率为近似值，实际汇率请以银行为准"
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def get_rate(currency: str) -> dict:
    """获取汇率"""
    try:
        currency = currency.upper()
        
        if currency not in EXCHANGE_RATES:
            return {"ok": False, "error": f"不支持的货币：{currency}"}
        
        rate = EXCHANGE_RATES[currency]
        
        return {
            "ok": True,
            "currency": currency,
            "rate_to_usd": rate,
            "rate_from_cny": rate / EXCHANGE_RATES["CNY"],
            "last_update": "2026-03-11"
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def list_currencies() -> dict:
    """列出支持的货币"""
    return {
        "ok": True,
        "count": len(EXCHANGE_RATES),
        "currencies": EXCHANGE_RATES
    }


def format_result(result: dict, action: str) -> str:
    """格式化结果"""
    if not result.get("ok"):
        return f"⚠️ 操作失败：{result.get('error')}"
    
    if action == "convert":
        return f"💱 货币转换\n\n{result['amount']} {result['from']} = {result['result']} {result['to']}\n\n汇率：1 {result['from']} = {result['rate']} {result['to']}\n\n⚠️ {result['note']}"
    
    if action == "rate":
        return f"💱 汇率查询\n\n{result['currency']}\n\n对 USD: {result['rate_to_usd']}\n对 CNY: {result['rate_from_cny']:.2f}\n\n最后更新：{result['last_update']}"
    
    if action == "list":
        lines = [f"💱 支持的货币（共{result['count']}种）\n"]
        lines.append("货币代码 | 对 USD 汇率")
        lines.append("-" * 30)
        for code, rate in sorted(result['currencies'].items()):
            lines.append(f"{code:8} | {rate:.4f}")
        return "\n".join(lines)
    
    return str(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python currency.py <命令> [参数]",
            "commands": [
                "convert <金额> <from> <to> - 货币转换",
                "rate <货币> - 查询汇率",
                "list - 列出支持的货币"
            ],
            "examples": [
                "python currency.py convert 100 USD CNY",
                "python currency.py convert 1000 CNY USD",
                "python currency.py rate EUR",
                "python currency.py list"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "convert":
        if len(sys.argv) < 5:
            print("用法：python currency.py convert <金额> <from> <to>")
            sys.exit(1)
        amount = float(sys.argv[2])
        from_curr = sys.argv[3]
        to_curr = sys.argv[4]
        result = convert_currency(amount, from_curr, to_curr)
        print(format_result(result, "convert"))
    
    elif command == "rate":
        if len(sys.argv) < 3:
            print("用法：python currency.py rate <货币>")
            sys.exit(1)
        result = get_rate(sys.argv[2])
        print(format_result(result, "rate"))
    
    elif command == "list":
        result = list_currencies()
        print(format_result(result, "list"))
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)
