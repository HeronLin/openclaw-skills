#!/usr/bin/env python3
"""
智能制造工具 - 设备监控、生产统计、质量分析
符合深圳龙岗"龙虾十条"智能制造方向
"""

import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

DATA_FILE = Path.home() / ".openclaw" / "workspace" / "main" / "memory" / "manufacturing.json"


def load_data():
    """加载数据"""
    if not DATA_FILE.exists():
        return {"devices": [], "production": [], "quality": [], "energy": []}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"devices": [], "production": [], "quality": [], "energy": []}


def save_data(data):
    """保存数据"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_device(device_id: str, name: str, model: str, status: str = "running") -> dict:
    """添加设备"""
    data = load_data()
    
    device = {
        "device_id": device_id,
        "name": name,
        "model": model,
        "status": status,
        "add_time": datetime.now().isoformat(),
        "last_update": datetime.now().isoformat()
    }
    
    data["devices"].append(device)
    save_data(data)
    
    return {"ok": True, "device": device}


def update_device_status(device_id: str, status: str) -> dict:
    """更新设备状态"""
    data = load_data()
    
    for device in data["devices"]:
        if device["device_id"] == device_id:
            device["status"] = status
            device["last_update"] = datetime.now().isoformat()
            save_data(data)
            return {"ok": True, "device_id": device_id, "status": status}
    
    return {"ok": False, "error": f"设备不存在：{device_id}"}


def add_production_record(date: str, product: str, quantity: int, defect: int = 0) -> dict:
    """添加生产记录"""
    data = load_data()
    
    record = {
        "date": date,
        "product": product,
        "quantity": quantity,
        "defect": defect,
        "yield_rate": round((quantity - defect) / quantity * 100, 2) if quantity > 0 else 0,
        "timestamp": datetime.now().isoformat()
    }
    
    data["production"].append(record)
    save_data(data)
    
    return {"ok": True, "record": record}


def get_production_stats(days: int = 7) -> dict:
    """获取生产统计"""
    data = load_data()
    
    # 获取最近 N 天的数据
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    recent = [r for r in data["production"] if r["date"] >= cutoff_date]
    
    if not recent:
        return {"ok": True, "message": "暂无生产数据"}
    
    total_quantity = sum(r["quantity"] for r in recent)
    total_defect = sum(r["defect"] for r in recent)
    avg_yield = sum(r["yield_rate"] for r in recent) / len(recent)
    
    return {
        "ok": True,
        "period": f"最近{days}天",
        "total_quantity": total_quantity,
        "total_defect": total_defect,
        "avg_yield_rate": f"{avg_yield:.2f}%",
        "records_count": len(recent)
    }


def add_quality_check(product: str, batch: str, checked: int, passed: int, issues: list = None) -> dict:
    """添加质检记录"""
    data = load_data()
    
    record = {
        "product": product,
        "batch": batch,
        "checked": checked,
        "passed": passed,
        "pass_rate": round(passed / checked * 100, 2) if checked > 0 else 0,
        "issues": issues or [],
        "timestamp": datetime.now().isoformat()
    }
    
    data["quality"].append(record)
    save_data(data)
    
    return {"ok": True, "record": record}


def add_energy_record(date: str, electricity: float, water: float = 0) -> dict:
    """添加能耗记录"""
    data = load_data()
    
    record = {
        "date": date,
        "electricity": electricity,
        "water": water,
        "timestamp": datetime.now().isoformat()
    }
    
    data["energy"].append(record)
    save_data(data)
    
    return {"ok": True, "record": record}


def get_device_list() -> dict:
    """获取设备列表"""
    data = load_data()
    
    running = sum(1 for d in data["devices"] if d["status"] == "running")
    stopped = sum(1 for d in data["devices"] if d["status"] == "stopped")
    error = sum(1 for d in data["devices"] if d["status"] == "error")
    
    return {
        "ok": True,
        "total": len(data["devices"]),
        "running": running,
        "stopped": stopped,
        "error": error,
        "devices": data["devices"]
    }


def format_result(result: dict, action: str) -> str:
    """格式化结果"""
    if not result.get("ok"):
        return f"⚠️ 操作失败：{result.get('error')}"
    
    if action == "device_add":
        return f"✅ 已添加设备\n\n设备 ID: {result['device']['device_id']}\n名称：{result['device']['name']}\n型号：{result['device']['model']}\n状态：{result['device']['status']}"
    
    if action == "device_status":
        return f"✅ 已更新设备状态\n\n设备 ID: {result['device_id']}\n新状态：{result['status']}"
    
    if action == "device_list":
        lines = ["🏭 设备列表\n"]
        lines.append(f"总计：{result['total']}台")
        lines.append(f"🟢 运行中：{result['running']}台")
        lines.append(f"🔴 已停止：{result['stopped']}台")
        lines.append(f"⚠️ 故障：{result['error']}台\n")
        
        for device in result['devices'][:10]:
            status_icon = "🟢" if device["status"] == "running" else "🔴" if device["status"] == "stopped" else "⚠️"
            lines.append(f"{status_icon} {device['device_id']}: {device['name']} ({device['model']})")
        
        return "\n".join(lines)
    
    if action == "production_add":
        return f"✅ 已添加生产记录\n\n日期：{result['record']['date']}\n产品：{result['record']['product']}\n产量：{result['record']['quantity']}\n不良：{result['record']['defect']}\n良率：{result['record']['yield_rate']}%"
    
    if action == "production_stats":
        if "message" in result:
            return f"📊 生产统计\n\n{result['message']}"
        
        lines = ["📊 生产统计\n"]
        lines.append(f"统计周期：{result['period']}")
        lines.append(f"总产量：{result['total_quantity']}")
        lines.append(f"不良数：{result['total_defect']}")
        lines.append(f"平均良率：{result['avg_yield_rate']}")
        lines.append(f"记录数：{result['records_count']}")
        
        return "\n".join(lines)
    
    if action == "quality_add":
        return f"✅ 已添加质检记录\n\n产品：{result['record']['product']}\n批次：{result['record']['batch']}\n检验数：{result['record']['checked']}\n合格数：{result['record']['passed']}\n合格率：{result['record']['pass_rate']}%"
    
    if action == "energy_add":
        return f"✅ 已添加能耗记录\n\n日期：{result['record']['date']}\n用电：{result['record']['electricity']}度\n用水：{result['record']['water']}吨"
    
    return str(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python manufacturing.py <命令> [参数]",
            "commands": [
                "device add <ID> <名称> <型号> - 添加设备",
                "device status <ID> <状态> - 更新设备状态",
                "device list - 设备列表",
                "production add <日期> <产品> <产量> [不良数] - 生产记录",
                "production stats [天数] - 生产统计",
                "quality add <产品> <批次> <检验数> <合格数> - 质检记录",
                "energy add <日期> <用电> [用水] - 能耗记录"
            ],
            "examples": [
                "python manufacturing.py device add CNC001 数控机床 CK6150",
                "python manufacturing.py production add 2026-03-11 产品 A 1000 5",
                "python manufacturing.py quality add 产品 A B20260311 100 98"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "device":
        subcmd = sys.argv[2] if len(sys.argv) > 2 else ""
        if subcmd == "add":
            if len(sys.argv) < 5:
                print("用法：python manufacturing.py device add <ID> <名称> <型号>")
                sys.exit(1)
            result = add_device(sys.argv[3], sys.argv[4], sys.argv[5])
            print(format_result(result, "device_add"))
        elif subcmd == "status":
            if len(sys.argv) < 5:
                print("用法：python manufacturing.py device status <ID> <状态>")
                sys.exit(1)
            result = update_device_status(sys.argv[3], sys.argv[4])
            print(format_result(result, "device_status"))
        elif subcmd == "list":
            result = get_device_list()
            print(format_result(result, "device_list"))
    
    elif command == "production":
        subcmd = sys.argv[2] if len(sys.argv) > 2 else ""
        if subcmd == "add":
            if len(sys.argv) < 6:
                print("用法：python manufacturing.py production add <日期> <产品> <产量> [不良数]")
                sys.exit(1)
            defect = int(sys.argv[6]) if len(sys.argv) > 6 else 0
            result = add_production_record(sys.argv[3], sys.argv[4], int(sys.argv[5]), defect)
            print(format_result(result, "production_add"))
        elif subcmd == "stats":
            days = int(sys.argv[3]) if len(sys.argv) > 3 else 7
            result = get_production_stats(days)
            print(format_result(result, "production_stats"))
    
    elif command == "quality":
        subcmd = sys.argv[2] if len(sys.argv) > 2 else ""
        if subcmd == "add":
            if len(sys.argv) < 6:
                print("用法：python manufacturing.py quality add <产品> <批次> <检验数> <合格数>")
                sys.exit(1)
            result = add_quality_check(sys.argv[3], sys.argv[4], int(sys.argv[5]), int(sys.argv[6]))
            print(format_result(result, "quality_add"))
    
    elif command == "energy":
        subcmd = sys.argv[2] if len(sys.argv) > 2 else ""
        if subcmd == "add":
            if len(sys.argv) < 5:
                print("用法：python manufacturing.py energy add <日期> <用电> [用水]")
                sys.exit(1)
            water = float(sys.argv[5]) if len(sys.argv) > 5 else 0
            result = add_energy_record(sys.argv[3], float(sys.argv[4]), water)
            print(format_result(result, "energy_add"))
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)
