#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
持仓管理系统 - 快速版本（模拟价格用于测试）
"""

import json
import sys
from datetime import datetime
from pathlib import Path
import random

DATA_FILE = Path.home() / ".openclaw" / "workspace" / "main" / "memory" / "portfolio.json"


def load_portfolio():
    if not DATA_FILE.exists():
        return {"positions": [], "last_update": None}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"positions": [], "last_update": None}


def save_portfolio(data):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    data["last_update"] = datetime.now().isoformat()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_stock_price(code):
    """模拟价格（测试用）"""
    base_prices = {"600519": 1680.0, "000001": 10.8, "300750": 180.5}
    if code in base_prices:
        base = base_prices[code]
        return round(base * (1 + random.uniform(-0.05, 0.05)), 2)
    return round(random.uniform(5, 100), 2)


def add_position(code, cost_price, quantity):
    portfolio = load_portfolio()
    code = code.zfill(6)
    
    for pos in portfolio["positions"]:
        if pos["code"] == code:
            old_qty = pos["quantity"]
            old_cost = pos["cost_price"]
            new_qty = int(quantity)
            new_cost = float(cost_price)
            total_qty = old_qty + new_qty
            avg_cost = (old_qty * old_cost + new_qty * new_cost) / total_qty
            pos["cost_price"] = round(avg_cost, 2)
            pos["quantity"] = total_qty
            save_portfolio(portfolio)
            return f"✅ 已加仓 {code}\n平均成本：{avg_cost:.2f}\n总数量：{total_qty}"
    
    new_position = {
        "code": code,
        "cost_price": float(cost_price),
        "quantity": int(quantity),
        "add_date": datetime.now().isoformat()
    }
    portfolio["positions"].append(new_position)
    save_portfolio(portfolio)
    return f"✅ 已添加持仓 {code}\n成本价：{cost_price}\n数量：{quantity}"


def remove_position(code):
    portfolio = load_portfolio()
    code = code.zfill(6)
    for i, pos in enumerate(portfolio["positions"]):
        if pos["code"] == code:
            removed = portfolio["positions"].pop(i)
            save_portfolio(portfolio)
            return f"✅ 已删除持仓 {removed['code']}"
    return f"❌ 未找到持仓 {code}"


def show_positions():
    portfolio = load_portfolio()
    if not portfolio["positions"]:
        return "📊 持仓列表\n\n暂无持仓"
    lines = ["📊 持仓列表", ""]
    for pos in portfolio["positions"]:
        lines.append(f"• {pos['code']}: 成本 {pos['cost_price']:.2f} × {pos['quantity']}股")
    lines.append(f"\n共 {len(portfolio['positions'])} 只股票")
    return "\n".join(lines)


def analyze_portfolio():
    portfolio = load_portfolio()
    if not portfolio["positions"]:
        return "📊 持仓分析\n\n暂无持仓"
    
    lines = ["📊 持仓分析", ""]
    total_cost = 0
    total_value = 0
    total_profit = 0
    profit_count = 0
    loss_count = 0
    
    for pos in portfolio["positions"]:
        code = pos["code"]
        cost = pos["cost_price"]
        qty = pos["quantity"]
        current = get_stock_price(code)
        
        pos_cost = cost * qty
        pos_value = current * qty
        profit = pos_value - pos_cost
        profit_pct = (profit / pos_cost * 100) if pos_cost > 0 else 0
        
        total_cost += pos_cost
        total_value += pos_value
        total_profit += profit
        
        if profit >= 0:
            profit_count += 1
            direction = "📈"
        else:
            loss_count += 1
            direction = "📉"
        
        lines.append(f"{direction} {code}")
        lines.append(f"   成本：{cost:.2f} × {qty} = {pos_cost:.2f}")
        lines.append(f"   现价：{current:.2f} × {qty} = {pos_value:.2f}")
        lines.append(f"   盈亏：{profit:+.2f} ({profit_pct:+.2f}%)")
        lines.append("")
    
    total_pct = (total_profit / total_cost * 100) if total_cost > 0 else 0
    lines.append("=" * 40)
    lines.append("📊 总盈亏汇总")
    lines.append("=" * 40)
    lines.append(f"总成本：{total_cost:,.2f}")
    lines.append(f"总市值：{total_value:,.2f}")
    lines.append(f"总盈亏：{total_profit:+,.2f} ({total_pct:+.2f}%)")
    lines.append(f"盈利：{profit_count}只 | 亏损：{loss_count}只")
    lines.append("=" * 40)
    lines.append("🎉 总体盈利！" if total_profit >= 0 else "💪 加油！")
    
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python portfolio.py <命令> [参数]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "add":
        print(add_position(sys.argv[2], sys.argv[4], sys.argv[6]))
    elif cmd == "remove":
        print(remove_position(sys.argv[2]))
    elif cmd == "show":
        print(show_positions())
    elif cmd == "analyze":
        print(analyze_portfolio())
    else:
        print(f"未知命令：{cmd}")
