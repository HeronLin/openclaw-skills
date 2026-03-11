#!/usr/bin/env python3
"""
智慧医疗工具 - 健康管理、病历管理、预约挂号
符合深圳龙岗"龙虾十条"智慧医疗方向
"""

import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

DATA_FILE = Path.home() / ".openclaw" / "workspace" / "main" / "memory" / "healthcare.json"


def load_data():
    """加载数据"""
    if not DATA_FILE.exists():
        return {"patients": [], "records": [], "appointments": [], "medications": []}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"patients": [], "records": [], "appointments": [], "medications": []}


def save_data(data):
    """保存数据"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def create_patient(name: str, gender: str, birth: str, phone: str = "") -> dict:
    """创建患者档案"""
    data = load_data()
    
    patient_id = f"PAT{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    patient = {
        "patient_id": patient_id,
        "name": name,
        "gender": gender,
        "birth": birth,
        "phone": phone,
        "create_time": datetime.now().isoformat()
    }
    
    data["patients"].append(patient)
    save_data(data)
    
    return {"ok": True, "patient": patient}


def add_medical_record(patient_id: str, diagnosis: str, doctor: str, prescription: str = "") -> dict:
    """添加病历记录"""
    data = load_data()
    
    record_id = f"REC{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    record = {
        "record_id": record_id,
        "patient_id": patient_id,
        "diagnosis": diagnosis,
        "doctor": doctor,
        "prescription": prescription,
        "create_time": datetime.now().isoformat()
    }
    
    data["records"].append(record)
    save_data(data)
    
    return {"ok": True, "record": record}


def get_patient_records(patient_id: str) -> dict:
    """获取患者病历"""
    data = load_data()
    
    records = [r for r in data["records"] if r["patient_id"] == patient_id]
    
    return {
        "ok": True,
        "patient_id": patient_id,
        "count": len(records),
        "records": records
    }


def create_appointment(patient_id: str, patient_name: str, department: str, doctor: str, time: str) -> dict:
    """创建预约"""
    data = load_data()
    
    appointment_id = f"APT{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    appointment = {
        "appointment_id": appointment_id,
        "patient_id": patient_id,
        "patient_name": patient_name,
        "department": department,
        "doctor": doctor,
        "time": time,
        "status": "scheduled",
        "create_time": datetime.now().isoformat()
    }
    
    data["appointments"].append(appointment)
    save_data(data)
    
    return {"ok": True, "appointment": appointment}


def update_appointment_status(appointment_id: str, status: str) -> dict:
    """更新预约状态"""
    data = load_data()
    
    for appointment in data["appointments"]:
        if appointment["appointment_id"] == appointment_id:
            appointment["status"] = status
            appointment["update_time"] = datetime.now().isoformat()
            save_data(data)
            return {"ok": True, "appointment_id": appointment_id, "status": status}
    
    return {"ok": False, "error": f"预约不存在：{appointment_id}"}


def get_appointment_list(department: str = None) -> dict:
    """获取预约列表"""
    data = load_data()
    
    appointments = data["appointments"]
    if department:
        appointments = [a for a in appointments if a["department"] == department]
    
    scheduled = sum(1 for a in appointments if a["status"] == "scheduled")
    completed = sum(1 for a in appointments if a["status"] == "completed")
    cancelled = sum(1 for a in appointments if a["status"] == "cancelled")
    
    return {
        "ok": True,
        "total": len(appointments),
        "scheduled": scheduled,
        "completed": completed,
        "cancelled": cancelled,
        "appointments": sorted(appointments, key=lambda x: x["time"], reverse=True)[:10]
    }


def add_medication(patient_id: str, patient_name: str, medicine: str, dosage: str, frequency: str, days: int) -> dict:
    """添加用药计划"""
    data = load_data()
    
    medication_id = f"MED{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    start_date = datetime.now()
    end_date = start_date + timedelta(days=days)
    
    medication = {
        "medication_id": medication_id,
        "patient_id": patient_id,
        "patient_name": patient_name,
        "medicine": medicine,
        "dosage": dosage,
        "frequency": frequency,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "status": "active",
        "create_time": datetime.now().isoformat()
    }
    
    data["medications"].append(medication)
    save_data(data)
    
    return {"ok": True, "medication": medication}


def get_medication_list(patient_id: str = None) -> dict:
    """获取用药计划列表"""
    data = load_data()
    
    medications = data["medications"]
    if patient_id:
        medications = [m for m in medications if m["patient_id"] == patient_id]
    
    active = sum(1 for m in medications if m["status"] == "active")
    completed = sum(1 for m in medications if m["status"] == "completed")
    
    return {
        "ok": True,
        "total": len(medications),
        "active": active,
        "completed": completed,
        "medications": medications[-10:]
    }


def format_result(result: dict, action: str) -> str:
    """格式化结果"""
    if not result.get("ok"):
        return f"⚠️ 操作失败：{result.get('error')}"
    
    if action == "patient_create":
        return f"✅ 已创建健康档案\n\n档案号：{result['patient']['patient_id']}\n姓名：{result['patient']['name']}\n性别：{result['patient']['gender']}\n生日：{result['patient']['birth']}"
    
    if action == "record_add":
        return f"✅ 已添加病历记录\n\n病历号：{result['record']['record_id']}\n患者 ID: {result['record']['patient_id']}\n诊断：{result['record']['diagnosis']}\n医生：{result['record']['doctor']}"
    
    if action == "record_get":
        lines = ["📋 病历记录\n"]
        lines.append(f"患者 ID: {result['patient_id']}")
        lines.append(f"病历数：{result['count']}\n")
        
        for record in result['records'][:5]:
            lines.append(f"📄 {record['record_id']}")
            lines.append(f"   诊断：{record['diagnosis']}")
            lines.append(f"   医生：{record['doctor']}")
            lines.append(f"   时间：{record['create_time'][:16]}")
            lines.append("")
        
        return "\n".join(lines)
    
    if action == "appointment_create":
        return f"✅ 已创建预约\n\n预约号：{result['appointment']['appointment_id']}\n患者：{result['appointment']['patient_name']}\n科室：{result['appointment']['department']}\n医生：{result['appointment']['doctor']}\n时间：{result['appointment']['time']}"
    
    if action == "appointment_status":
        return f"✅ 已更新预约状态\n\n预约号：{result['appointment_id']}\n新状态：{result['status']}"
    
    if action == "appointment_list":
        lines = ["📅 预约列表\n"]
        lines.append(f"总计：{result['total']}个")
        lines.append(f"🟢 已预约：{result['scheduled']}个")
        lines.append(f"✅ 已完成：{result['completed']}个")
        lines.append(f"❌ 已取消：{result['cancelled']}个\n")
        
        for apt in result['appointments']:
            status_icon = "🟢" if apt["status"] == "scheduled" else "✅" if apt["status"] == "completed" else "❌"
            lines.append(f"{status_icon} {apt['appointment_id']}: {apt['patient_name']} - {apt['department']} - {apt['time']}")
        
        return "\n".join(lines)
    
    if action == "medication_add":
        return f"✅ 已添加用药计划\n\n计划号：{result['medication']['medication_id']}\n患者：{result['medication']['patient_name']}\n药品：{result['medication']['medicine']}\n剂量：{result['medication']['dosage']}\n频次：{result['medication']['frequency']}\n周期：{result['medication']['start_date']} 至 {result['medication']['end_date']}"
    
    if action == "medication_list":
        lines = ["💊 用药计划\n"]
        lines.append(f"总计：{result['total']}个")
        lines.append(f"🟢 进行中：{result['active']}个")
        lines.append(f"✅ 已完成：{result['completed']}个\n")
        
        for med in result['medications']:
            status_icon = "🟢" if med["status"] == "active" else "✅"
            lines.append(f"{status_icon} {med['medication_id']}: {med['patient_name']} - {med['medicine']}")
            lines.append(f"   {med['dosage']} {med['frequency']}")
            lines.append("")
        
        return "\n".join(lines)
    
    return str(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python healthcare.py <命令> [参数]",
            "commands": [
                "patient create <姓名> <性别> <生日> [电话] - 创建健康档案",
                "record add <患者 ID> <诊断> <医生> [处方] - 添加病历",
                "record get <患者 ID> - 获取病历",
                "appointment create <患者 ID> <姓名> <科室> <医生> <时间> - 创建预约",
                "appointment status <预约号> <状态> - 更新预约状态",
                "appointment list [科室] - 预约列表",
                "medication add <患者 ID> <姓名> <药品> <剂量> <频次> <天数> - 用药计划",
                "medication list [患者 ID] - 用药计划列表"
            ],
            "examples": [
                "python healthcare.py patient create 张三 男 1990-01-01 13800138000",
                "python healthcare.py record add PAT20260311 感冒 李医生 感冒药",
                "python healthcare.py appointment create PAT20260311 张三 内科 王医生 2026-03-12 10:00"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "patient":
        subcmd = sys.argv[2] if len(sys.argv) > 2 else ""
        if subcmd == "create":
            if len(sys.argv) < 5:
                print("用法：python healthcare.py patient create <姓名> <性别> <生日>")
                sys.exit(1)
            phone = sys.argv[5] if len(sys.argv) > 5 else ""
            result = create_patient(sys.argv[3], sys.argv[4], sys.argv[5], phone)
            print(format_result(result, "patient_create"))
    
    elif command == "record":
        subcmd = sys.argv[2] if len(sys.argv) > 2 else ""
        if subcmd == "add":
            if len(sys.argv) < 6:
                print("用法：python healthcare.py record add <患者 ID> <诊断> <医生>")
                sys.exit(1)
            prescription = sys.argv[6] if len(sys.argv) > 6 else ""
            result = add_medical_record(sys.argv[3], sys.argv[4], sys.argv[5], prescription)
            print(format_result(result, "record_add"))
        elif subcmd == "get":
            if len(sys.argv) < 4:
                print("用法：python healthcare.py record get <患者 ID>")
                sys.exit(1)
            result = get_patient_records(sys.argv[3])
            print(format_result(result, "record_get"))
    
    elif command == "appointment":
        subcmd = sys.argv[2] if len(sys.argv) > 2 else ""
        if subcmd == "create":
            if len(sys.argv) < 7:
                print("用法：python healthcare.py appointment create <患者 ID> <姓名> <科室> <医生> <时间>")
                sys.exit(1)
            result = create_appointment(sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
            print(format_result(result, "appointment_create"))
        elif subcmd == "status":
            if len(sys.argv) < 5:
                print("用法：python healthcare.py appointment status <预约号> <状态>")
                sys.exit(1)
            result = update_appointment_status(sys.argv[3], sys.argv[4])
            print(format_result(result, "appointment_status"))
        elif subcmd == "list":
            dept = sys.argv[3] if len(sys.argv) > 3 else None
            result = get_appointment_list(dept)
            print(format_result(result, "appointment_list"))
    
    elif command == "medication":
        subcmd = sys.argv[2] if len(sys.argv) > 2 else ""
        if subcmd == "add":
            if len(sys.argv) < 8:
                print("用法：python healthcare.py medication add <患者 ID> <姓名> <药品> <剂量> <频次> <天数>")
                sys.exit(1)
            result = add_medication(sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], int(sys.argv[8]))
            print(format_result(result, "medication_add"))
        elif subcmd == "list":
            patient_id = sys.argv[3] if len(sys.argv) > 3 else None
            result = get_medication_list(patient_id)
            print(format_result(result, "medication_list"))
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)
