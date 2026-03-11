#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
持仓管理系统 - 支持总盈亏汇总
功能：添加/删除/显示持仓，计算总盈亏
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# 持仓数据文件
DATA_FILE = Path.home() / ".openclaw" / "workspace" / "main" / "memory" / "portfolio.json"


def load_portfolio():
    """加载持仓数据"""
    if not DATA_FILE.exists():
        return {"positions": [], "last_update": None}
    
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"positions": [], "last_update": None}


def save_portfolio(data):
    """保存持仓数据"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    data["last_update"] = datetime.now().isoformat()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_stock_prices(codes):
    """批量获取股票价格"""
    try:
        import akshare as ak
        df = ak.stock_zh_a_spot_em()
        price_dict = {}
        for _, row in df.iterrows():
            code = str(row['代码']).zfill(6)
            if code in codes:
                try:
                    price_dict[code] = float(row['最新价'])
                except (ValueError, TypeError):
                    price_dict[code] = None
        return price_dict
    except Exception as e:
        print(f"⚠️ 获取价格失败：{e}", file=sys.stderr)
        return {code: None for code in codes}


def add_position(code, cost_price, quantity):
    """添加持仓"""
    portfolio = load_portfolio()
    
    # 检查是否已存在
    for pos in portfolio["positions"]:
        if pos["code"] == code:
            # 已有持仓，计算平均成本
            old_qty = pos["quantity"]
            old_cost = pos["cost_price"]
            new_qty = int(quantity)
            new_cost = float(cost_price)
            
            total_qty = old_qty + new_qty
            avg_cost = (old_qty * old_cost + new_qty * new_cost) / total_qty
            
            pos["cost_price"] = round(avg_cost, 2)
            pos["quantity"] = total_qty
            pos["last_add"] = datetime.now().isoformat()
            
            save_portfolio(portfolio)
            return f"✅ 已加仓 {code}\n平均成本：{avg_cost:.2f}\n总数量：{total_qty}"
    
    # 新建持仓
    new_position = {
        "code": code,
        "cost_price": float(cost_price),
        "quantity": int(quantity),
        "add_date": datetime.now().isoformat(),
        "last_add": datetime.now().isoformat()
    }
    
    portfolio["positions"].append(new_position)
    save_portfolio(portfolio)
    
    return f"✅ 已添加持仓 {code}\n成本价：{cost_price}\n数量：{quantity}"


def remove_position(code):
    """删除持仓"""
    portfolio = load_portfolio()
    
    for i, pos in enumerate(portfolio["positions"]):
        if pos["code"] == code:
            removed = portfolio["positions"].pop(i)
            save_portfolio(portfolio)
            return f"✅ 已删除持仓 {removed['code']}\n成本价：{removed['cost_price']}\n数量：{removed['quantity']}"
    
    return f"❌ 未找到持仓 {code}"


def show_positions():
    """显示所有持仓（不含盈亏）"""
    portfolio = load_portfolio()
    
    if not portfolio["positions"]:
        return "📊 持仓列表\n\n暂无持仓"
    
    lines = ["📊 持仓列表", ""]
    for pos in portfolio["positions"]:
        code = pos["code"]
        cost = pos["cost_price"]
        qty = pos["quantity"]
        lines.append(f"• {code}: 成本 {cost:.2f} × {qty}股")
    
    lines.append(f"\n共 {len(portfolio['positions'])} 只股票")
    return "\n".join(lines)


def analyze_portfolio():
    """分析持仓 - 包含总盈亏汇总"""
    portfolio = load_portfolio()
    
    if not portfolio["positions"]:
        return "📊 持仓分析\n\n暂无持仓"
    
    lines = ["📊 持仓分析", ""]
    
    # 批量获取价格
    codes = [pos["code"] for pos in portfolio["positions"]]
    prices = get_stock_prices(codes)
    
    total_cost = 0
    total_market_value = 0
    total_profit_loss = 0
    profit_count = 0
    loss_count = 0
    
    for pos in portfolio["positions"]:
        code = pos["code"]
        cost_price = pos["cost_price"]
        quantity = pos["quantity"]
        
        # 获取实时价格
        current_price = prices.get(code)
        
        if current_price is None:
            lines.append(f"⚠️ {code}: 获取价格失败")
            continue
        
        # 计算盈亏
        position_cost = cost_price * quantity
        position_value = current_price * quantity
        position_profit = position_value - position_cost
        position_profit_pct = (position_profit / position_cost) * 100 if position_cost > 0 else 0
        
        total_cost += position_cost
        total_market_value += position_value
        total_profit_loss += position_profit
        
        if position_profit >= 0:
            profit_count += 1
            direction = "📈"
        else:
            loss_count += 1
            direction = "📉"
        
        lines.append(f"{direction} {code}")
        lines.append(f"   成本：{cost_price:.2f} × {quantity} = {position_cost:.2f}")
        lines.append(f"   现价：{current_price:.2f} × {quantity} = {position_value:.2f}")
        lines.append(f"   盈亏：{position_profit:+.2f} ({position_profit_pct:+.2f}%)")
        lines.append("")
    
    # 总盈亏汇总
    total_profit_pct = (total_profit_loss / total_cost * 100) if total_cost > 0 else 0
    
    lines.append("=" * 40)
    lines.append("📊 总盈亏汇总")
    lines.append("=" * 40)
    lines.append(f"总成本：{total_cost:,.2f}")
    lines.append(f"总市值：{total_market_value:,.2f}")
    lines.append(f"总盈亏：{total_profit_loss:+,.2f} ({total_profit_pct:+.2f}%)")
    lines.append(f"盈利：{profit_count}只 | 亏损：{loss_count}只")
    lines.append("=" * 40)
    
    if total_profit_loss >= 0:
        lines.append("🎉 总体盈利！继续保持！")
    else:
        lines.append("💪 暂时亏损，加油！")
    
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("用法：python portfolio.py <命令> [参数]")
        print("命令:")
        print("  add <代码> --cost <成本> --qty <数量>  添加持仓")
        print("  remove <代码>                          删除持仓")
        print("  show                                   显示持仓列表")
        print("  analyze                                持仓分析（含盈亏）")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "add":
        if len(sys.argv) < 6:
            print("用法：python portfolio.py add <代码> --cost <成本> --qty <数量>")
            sys.exit(1)
        code = sys.argv[2].zfill(6)
        cost = sys.argv[4]
        qty = sys.argv[6]
        print(add_position(code, cost, qty))
    
    elif command == "remove":
        if len(sys.argv) < 3:
            print("用法：python portfolio.py remove <代码>")
            sys.exit(1)
        code = sys.argv[2].zfill(6)
        print(remove_position(code))
    
    elif command == "show":
        print(show_positions())
    
    elif command == "analyze":
        print(analyze_portfolio())
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
