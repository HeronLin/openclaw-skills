#!/usr/bin/env python3
"""
智慧政务工具 - 公文处理、行政审批、数据报表
符合深圳龙岗"龙虾十条"智慧政务方向
"""

import sys
import json
from datetime import datetime
from pathlib import Path

DATA_FILE = Path.home() / ".openclaw" / "workspace" / "main" / "memory" / "government.json"


def load_data():
    """加载数据"""
    if not DATA_FILE.exists():
        return {"documents": [], "approvals": [], "reports": [], "notices": []}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"documents": [], "approvals": [], "reports": [], "notices": []}


def save_data(data):
    """保存数据"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def create_document(title: str, type: str, department: str, content: str = "") -> dict:
    """创建公文"""
    data = load_data()
    
    doc_id = f"DOC{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    doc = {
        "doc_id": doc_id,
        "title": title,
        "type": type,
        "department": department,
        "content": content,
        "status": "draft",
        "create_time": datetime.now().isoformat(),
        "create_by": "system"
    }
    
    data["documents"].append(doc)
    save_data(data)
    
    return {"ok": True, "document": doc}


def update_document_status(doc_id: str, status: str) -> dict:
    """更新公文状态"""
    data = load_data()
    
    for doc in data["documents"]:
        if doc["doc_id"] == doc_id:
            doc["status"] = status
            doc["update_time"] = datetime.now().isoformat()
            save_data(data)
            return {"ok": True, "doc_id": doc_id, "status": status}
    
    return {"ok": False, "error": f"公文不存在：{doc_id}"}


def get_document_list(department: str = None) -> dict:
    """获取公文列表"""
    data = load_data()
    
    docs = data["documents"]
    if department:
        docs = [d for d in docs if d["department"] == department]
    
    # 按状态统计
    draft = sum(1 for d in docs if d["status"] == "draft")
    reviewing = sum(1 for d in docs if d["status"] == "reviewing")
    approved = sum(1 for d in docs if d["status"] == "approved")
    archived = sum(1 for d in docs if d["status"] == "archived")
    
    return {
        "ok": True,
        "total": len(docs),
        "draft": draft,
        "reviewing": reviewing,
        "approved": approved,
        "archived": archived,
        "documents": docs[-10:]  # 最近 10 条
    }


def create_approval(title: str, applicant: str, department: str, details: str = "") -> dict:
    """创建审批"""
    data = load_data()
    
    approval_id = f"APP{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    approval = {
        "approval_id": approval_id,
        "title": title,
        "applicant": applicant,
        "department": department,
        "details": details,
        "status": "pending",
        "create_time": datetime.now().isoformat(),
        "steps": [
            {"step": 1, "name": "部门审核", "status": "pending"},
            {"step": 2, "name": "领导审批", "status": "waiting"},
            {"step": 3, "name": "归档", "status": "waiting"}
        ]
    }
    
    data["approvals"].append(approval)
    save_data(data)
    
    return {"ok": True, "approval": approval}


def update_approval_step(approval_id: str, step: int, status: str) -> dict:
    """更新审批步骤"""
    data = load_data()
    
    for approval in data["approvals"]:
        if approval["approval_id"] == approval_id:
            if step <= len(approval["steps"]):
                approval["steps"][step - 1]["status"] = status
                
                # 更新下一步
                if step < len(approval["steps"]):
                    approval["steps"][step]["status"] = "pending"
                
                # 如果是最后一步，更新整体状态
                if step == len(approval["steps"]) and status == "approved":
                    approval["status"] = "completed"
                elif status == "rejected":
                    approval["status"] = "rejected"
                else:
                    approval["status"] = "processing"
                
                approval["update_time"] = datetime.now().isoformat()
                save_data(data)
                
                return {"ok": True, "approval_id": approval_id, "step": step, "status": status}
    
    return {"ok": False, "error": f"审批不存在：{approval_id}"}


def get_approval_stats() -> dict:
    """获取审批统计"""
    data = load_data()
    
    pending = sum(1 for a in data["approvals"] if a["status"] == "pending")
    processing = sum(1 for a in data["approvals"] if a["status"] == "processing")
    completed = sum(1 for a in data["approvals"] if a["status"] == "completed")
    rejected = sum(1 for a in data["approvals"] if a["status"] == "rejected")
    
    return {
        "ok": True,
        "total": len(data["approvals"]),
        "pending": pending,
        "processing": processing,
        "completed": completed,
        "rejected": rejected
    }


def create_notice(title: str, department: str, content: str, level: str = "normal") -> dict:
    """创建通知"""
    data = load_data()
    
    notice_id = f"NOT{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    notice = {
        "notice_id": notice_id,
        "title": title,
        "department": department,
        "content": content,
        "level": level,
        "publish_time": datetime.now().isoformat(),
        "view_count": 0
    }
    
    data["notices"].append(notice)
    save_data(data)
    
    return {"ok": True, "notice": notice}


def get_notice_list() -> dict:
    """获取通知列表"""
    data = load_data()
    
    urgent = [n for n in data["notices"] if n["level"] == "urgent"]
    normal = [n for n in data["notices"] if n["level"] == "normal"]
    
    return {
        "ok": True,
        "total": len(data["notices"]),
        "urgent_count": len(urgent),
        "normal_count": len(normal),
        "notices": sorted(data["notices"], key=lambda x: x["publish_time"], reverse=True)[:10]
    }


def format_result(result: dict, action: str) -> str:
    """格式化结果"""
    if not result.get("ok"):
        return f"⚠️ 操作失败：{result.get('error')}"
    
    if action == "doc_create":
        return f"✅ 已创建公文\n\n文号：{result['document']['doc_id']}\n标题：{result['document']['title']}\n类型：{result['document']['type']}\n部门：{result['document']['department']}\n状态：{result['document']['status']}"
    
    if action == "doc_status":
        return f"✅ 已更新公文状态\n\n文号：{result['doc_id']}\n新状态：{result['status']}"
    
    if action == "doc_list":
        lines = ["📄 公文列表\n"]
        lines.append(f"总计：{result['total']}份")
        lines.append(f"📝 草稿：{result['draft']}份")
        lines.append(f"🔄 审核中：{result['reviewing']}份")
        lines.append(f"✅ 已通过：{result['approved']}份")
        lines.append(f"🗄️ 已归档：{result['archived']}份\n")
        
        for doc in result['documents']:
            status_icon = "📝" if doc["status"] == "draft" else "🔄" if doc["status"] == "reviewing" else "✅" if doc["status"] == "approved" else "🗄️"
            lines.append(f"{status_icon} {doc['doc_id']}: {doc['title']} ({doc['department']})")
        
        return "\n".join(lines)
    
    if action == "approval_create":
        return f"✅ 已创建审批\n\n审批号：{result['approval']['approval_id']}\n标题：{result['approval']['title']}\n申请人：{result['approval']['applicant']}\n部门：{result['approval']['department']}\n状态：{result['approval']['status']}"
    
    if action == "approval_step":
        return f"✅ 已更新审批步骤\n\n审批号：{result['approval_id']}\n步骤：{result['step']}\n状态：{result['status']}"
    
    if action == "approval_stats":
        lines = ["📊 审批统计\n"]
        lines.append(f"总计：{result['total']}件")
        lines.append(f"⏳ 待处理：{result['pending']}件")
        lines.append(f"🔄 处理中：{result['processing']}件")
        lines.append(f"✅ 已完成：{result['completed']}件")
        lines.append(f"❌ 已驳回：{result['rejected']}件")
        
        return "\n".join(lines)
    
    if action == "notice_create":
        level_text = "🔴 紧急" if result['notice']['level'] == "urgent" else "🔵 普通"
        return f"✅ 已发布通知\n\n编号：{result['notice']['notice_id']}\n标题：{result['notice']['title']}\n部门：{result['notice']['department']}\n级别：{level_text}"
    
    if action == "notice_list":
        lines = ["📢 通知列表\n"]
        lines.append(f"总计：{result['total']}条")
        lines.append(f"🔴 紧急：{result['urgent_count']}条")
        lines.append(f"🔵 普通：{result['normal_count']}条\n")
        
        for notice in result['notices']:
            level_icon = "🔴" if notice["level"] == "urgent" else "🔵"
            lines.append(f"{level_icon} {notice['notice_id']}: {notice['title']} ({notice['department']})")
        
        return "\n".join(lines)
    
    return str(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python government.py <命令> [参数]",
            "commands": [
                "doc create <标题> <类型> <部门> - 创建公文",
                "doc status <文号> <状态> - 更新公文状态",
                "doc list [部门] - 公文列表",
                "approval create <标题> <申请人> <部门> - 创建审批",
                "approval step <审批号> <步骤> <状态> - 更新审批步骤",
                "approval stats - 审批统计",
                "notice create <标题> <部门> <内容> [级别] - 创建通知",
                "notice list - 通知列表"
            ],
            "examples": [
                "python government.py doc create 关于 XXX 的通知 通知 办公室",
                "python government.py approval create 采购申请 张三 采购部",
                "python government.py notice create 会议通知 办公室 明天开会 urgent"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "doc":
        subcmd = sys.argv[2] if len(sys.argv) > 2 else ""
        if subcmd == "create":
            if len(sys.argv) < 5:
                print("用法：python government.py doc create <标题> <类型> <部门>")
                sys.exit(1)
            result = create_document(sys.argv[3], sys.argv[4], sys.argv[5])
            print(format_result(result, "doc_create"))
        elif subcmd == "status":
            if len(sys.argv) < 5:
                print("用法：python government.py doc status <文号> <状态>")
                sys.exit(1)
            result = update_document_status(sys.argv[3], sys.argv[4])
            print(format_result(result, "doc_status"))
        elif subcmd == "list":
            dept = sys.argv[3] if len(sys.argv) > 3 else None
            result = get_document_list(dept)
            print(format_result(result, "doc_list"))
    
    elif command == "approval":
        subcmd = sys.argv[2] if len(sys.argv) > 2 else ""
        if subcmd == "create":
            if len(sys.argv) < 5:
                print("用法：python government.py approval create <标题> <申请人> <部门>")
                sys.exit(1)
            result = create_approval(sys.argv[3], sys.argv[4], sys.argv[5])
            print(format_result(result, "approval_create"))
        elif subcmd == "step":
            if len(sys.argv) < 6:
                print("用法：python government.py approval step <审批号> <步骤> <状态>")
                sys.exit(1)
            result = update_approval_step(sys.argv[3], int(sys.argv[4]), sys.argv[5])
            print(format_result(result, "approval_step"))
        elif subcmd == "stats":
            result = get_approval_stats()
            print(format_result(result, "approval_stats"))
    
    elif command == "notice":
        subcmd = sys.argv[2] if len(sys.argv) > 2 else ""
        if subcmd == "create":
            if len(sys.argv) < 5:
                print("用法：python government.py notice create <标题> <部门> <内容> [级别]")
                sys.exit(1)
            level = sys.argv[5] if len(sys.argv) > 5 else "normal"
            result = create_notice(sys.argv[3], sys.argv[4], sys.argv[5], level)
            print(format_result(result, "notice_create"))
        elif subcmd == "list":
            result = get_notice_list()
            print(format_result(result, "notice_list"))
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)
