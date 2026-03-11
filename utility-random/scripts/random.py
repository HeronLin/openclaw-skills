#!/usr/bin/env python3
"""
随机决策工具 - 掷骰子、抽签、随机数、抛硬币
完全本地计算，无需 API
"""

import sys
import json
import random
from datetime import datetime


def roll_dice(sides: int = 6, count: int = 1):
    """掷骰子"""
    results = [random.randint(1, sides) for _ in range(count)]
    total = sum(results)
    
    return {
        "ok": True,
        "type": "dice",
        "sides": sides,
        "count": count,
        "results": results,
        "total": total
    }


def flip_coin(count: int = 1):
    """抛硬币"""
    results = []
    heads = 0
    tails = 0
    
    for _ in range(count):
        if random.random() < 0.5:
            results.append("正面")
            heads += 1
        else:
            results.append("反面")
            tails += 1
    
    return {
        "ok": True,
        "type": "coin",
        "count": count,
        "results": results,
        "heads": heads,
        "tails": tails
    }


def draw_lottery(options: list, count: int = 1):
    """抽签/随机选择"""
    if count > len(options):
        return {"ok": False, "error": f"选项不足，只有{len(options)}个选项"}
    
    results = random.sample(options, count)
    
    return {
        "ok": True,
        "type": "lottery",
        "options": options,
        "count": count,
        "results": results
    }


def generate_random(min_val: int = 1, max_val: int = 100, count: int = 1, unique: bool = True):
    """生成随机数"""
    if unique and (max_val - min_val + 1) < count:
        return {"ok": False, "error": "范围内的唯一随机数不足"}
    
    if unique:
        results = random.sample(range(min_val, max_val + 1), count)
    else:
        results = [random.randint(min_val, max_val) for _ in range(count)]
    
    return {
        "ok": True,
        "type": "random",
        "range": f"{min_val}-{max_val}",
        "count": count,
        "unique": unique,
        "results": results
    }


def shuffle_list(items: list):
    """打乱列表"""
    shuffled = items.copy()
    random.shuffle(shuffled)
    
    return {
        "ok": True,
        "type": "shuffle",
        "original": items,
        "shuffled": shuffled
    }


def format_result(result: dict) -> str:
    """格式化结果"""
    if not result.get("ok"):
        return f"⚠️ 操作失败：{result.get('error')}"
    
    rtype = result.get("type")
    lines = []
    
    if rtype == "dice":
        lines.append(f"🎲 掷骰子（{result['sides']}面 x{result['count']}）")
        lines.append("")
        lines.append(f"结果：{result['results']}")
        lines.append(f"总和：{result['total']}")
    
    elif rtype == "coin":
        lines.append(f"🪙 抛硬币（x{result['count']}）")
        lines.append("")
        lines.append(f"结果：{', '.join(result['results'])}")
        lines.append(f"正面：{result['heads']} 反面：{result['tails']}")
    
    elif rtype == "lottery":
        lines.append(f"🎯 随机选择")
        lines.append("")
        lines.append(f"选项：{', '.join(result['options'])}")
        lines.append(f"结果：{', '.join(result['results'])}")
    
    elif rtype == "random":
        lines.append(f"🔢 随机数（{result['range']} x{result['count']}）")
        lines.append("")
        lines.append(f"结果：{result['results']}")
    
    elif rtype == "shuffle":
        lines.append(f"🔀 打乱顺序")
        lines.append("")
        lines.append(f"原始：{', '.join(result['original'])}")
        lines.append(f"结果：{', '.join(result['shuffled'])}")
    
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python random.py <命令> [参数]",
            "commands": [
                "dice [面数] [数量] - 掷骰子（默认 6 面 1 个）",
                "coin [数量] - 抛硬币（默认 1 次）",
                "draw <选项 1>,<选项 2>,... [数量] - 抽签",
                "number [最小] [最大] [数量] - 随机数",
                "shuffle <项 1>,<项 2>,... - 打乱顺序"
            ],
            "examples": [
                "python random.py dice",
                "python random.py dice 20 3",
                "python random.py coin 5",
                "python random.py draw 吃饭，睡觉，打游戏",
                "python random.py number 1 100 5",
                "python random.py shuffle A,B,C,D"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "dice":
        sides = int(sys.argv[2]) if len(sys.argv) > 2 else 6
        count = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        result = roll_dice(sides, count)
    
    elif command == "coin":
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        result = flip_coin(count)
    
    elif command == "draw":
        if len(sys.argv) < 3:
            print("用法：python random.py draw <选项 1>,<选项 2>,... [数量]")
            sys.exit(1)
        options = sys.argv[2].split(",")
        count = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        result = draw_lottery(options, count)
    
    elif command == "number":
        min_val = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        max_val = int(sys.argv[3]) if len(sys.argv) > 3 else 100
        count = int(sys.argv[4]) if len(sys.argv) > 4 else 1
        result = generate_random(min_val, max_val, count)
    
    elif command == "shuffle":
        if len(sys.argv) < 3:
            print("用法：python random.py shuffle <项 1>,<项 2>,...")
            sys.exit(1)
        items = sys.argv[2].split(",")
        result = shuffle_list(items)
    
    else:
        result = {"ok": False, "error": f"未知命令：{command}"}
    
    print(format_result(result))
