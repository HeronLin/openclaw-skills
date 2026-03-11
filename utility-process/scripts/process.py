#!/usr/bin/env python3
"""
进程管理工具 - 查看、搜索、管理进程
完全本地查询，无需 API
"""

import sys
import json
import subprocess
import os


def list_processes(limit: int = 20, sort_by: str = "cpu") -> dict:
    """列出进程"""
    try:
        # 使用 ps 命令
        if sort_by == "cpu":
            cmd = ["ps", "aux", "--sort=-%cpu"]
        elif sort_by == "memory":
            cmd = ["ps", "aux", "--sort=-%mem"]
        else:
            cmd = ["ps", "aux"]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            header = lines[0].split()
            processes = []
            
            for line in lines[1:limit+1]:
                parts = line.split(None, 10)
                if len(parts) >= 11:
                    processes.append({
                        "user": parts[0],
                        "pid": parts[1],
                        "cpu": parts[2],
                        "mem": parts[3],
                        "vsz": parts[4],
                        "rss": parts[5],
                        "tty": parts[6],
                        "stat": parts[7],
                        "start": parts[8],
                        "time": parts[9],
                        "command": parts[10]
                    })
            
            return {
                "ok": True,
                "count": len(processes),
                "sort_by": sort_by,
                "processes": processes
            }
        else:
            return {"ok": False, "error": "获取进程列表失败"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def search_processes(keyword: str) -> dict:
    """搜索进程"""
    try:
        result = subprocess.run(
            ["ps", "aux"],
            capture_output=True, text=True, timeout=5
        )
        
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            matched = []
            
            for line in lines[1:]:  # 跳过标题
                if keyword.lower() in line.lower():
                    parts = line.split(None, 10)
                    if len(parts) >= 11:
                        matched.append({
                            "user": parts[0],
                            "pid": parts[1],
                            "cpu": parts[2],
                            "mem": parts[3],
                            "command": parts[10]
                        })
            
            return {
                "ok": True,
                "keyword": keyword,
                "count": len(matched),
                "processes": matched
            }
        else:
            return {"ok": False, "error": "搜索失败"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def get_process_info(pid: str) -> dict:
    """获取进程详细信息"""
    try:
        # 使用 ps 获取详细信息
        result = subprocess.run(
            ["ps", "-p", pid, "-o", "pid,ppid,user,%cpu,%mem,vsz,rss,stat,start,time,cmd"],
            capture_output=True, text=True, timeout=5
        )
        
        if result.returncode == 0 and result.stdout.strip():
            lines = result.stdout.strip().split("\n")
            if len(lines) >= 2:
                parts = lines[1].split()
                return {
                    "ok": True,
                    "pid": parts[0],
                    "ppid": parts[1],
                    "user": parts[2],
                    "cpu": parts[3],
                    "mem": parts[4],
                    "vsz": parts[5],
                    "rss": parts[6],
                    "stat": parts[7],
                    "start": parts[8],
                    "time": parts[9],
                    "cmd": parts[10] if len(parts) > 10 else "Unknown"
                }
        
        return {"ok": False, "error": f"未找到进程 {pid}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def kill_process(pid: str, signal: str = "TERM") -> dict:
    """终止进程"""
    try:
        result = subprocess.run(
            ["kill", f"-{signal}", pid],
            capture_output=True, text=True, timeout=5
        )
        
        if result.returncode == 0:
            return {
                "ok": True,
                "pid": pid,
                "signal": signal,
                "message": f"已发送 {signal} 信号到进程 {pid}"
            }
        else:
            return {"ok": False, "error": result.stderr.strip()}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def format_result(result: dict, action: str) -> str:
    """格式化结果"""
    if not result.get("ok"):
        return f"⚠️ 操作失败：{result.get('error')}"
    
    if action == "list":
        lines = [f"📊 进程列表（按{result['sort_by']}排序，前{result['count']}个）\n"]
        lines.append(f"{'PID':<8} {'USER':<10} {'CPU%':<6} {'MEM%':<6} {'COMMAND':<50}")
        lines.append("-" * 80)
        
        for proc in result['processes']:
            cmd = proc['command'][:47] + "..." if len(proc['command']) > 50 else proc['command']
            lines.append(f"{proc['pid']:<8} {proc['user']:<10} {proc['cpu']:<6} {proc['mem']:<6} {cmd:<50}")
        
        return "\n".join(lines)
    
    if action == "search":
        lines = [f"🔍 搜索进程 \"{result['keyword']}\"（找到{result['count']}个）\n"]
        
        for proc in result['processes'][:10]:
            lines.append(f"PID: {proc['pid']} | USER: {proc['user']} | CPU: {proc['cpu']}% | MEM: {proc['mem']}%")
            lines.append(f"   命令：{proc['command']}")
            lines.append("")
        
        if result['count'] > 10:
            lines.append(f"... 还有 {result['count'] - 10} 个进程")
        
        return "\n".join(lines)
    
    if action == "info":
        return f"📊 进程信息\n\nPID: {result['pid']}\nPPID: {result['ppid']}\n用户：{result['user']}\nCPU: {result['cpu']}%\n内存：{result['mem']}%\nVSZ: {result['vsz']}\nRSS: {result['rss']}\n状态：{result['stat']}\n启动：{result['start']}\n时间：{result['time']}\n命令：{result['cmd']}"
    
    if action == "kill":
        return f"✅ {result['message']}"
    
    return str(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python process.py <命令> [参数]",
            "commands": [
                "list [cpu|memory] [数量] - 列出进程",
                "search <关键词> - 搜索进程",
                "info <PID> - 查看进程详情",
                "kill <PID> [信号] - 终止进程"
            ],
            "examples": [
                "python process.py list cpu 10",
                "python process.py search python",
                "python process.py info 1234",
                "python process.py kill 1234"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "list":
        sort_by = sys.argv[2] if len(sys.argv) > 2 else "cpu"
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 20
        result = list_processes(limit, sort_by)
        print(format_result(result, "list"))
    
    elif command == "search":
        if len(sys.argv) < 3:
            print("请提供关键词")
            sys.exit(1)
        result = search_processes(sys.argv[2])
        print(format_result(result, "search"))
    
    elif command == "info":
        if len(sys.argv) < 3:
            print("请提供 PID")
            sys.exit(1)
        result = get_process_info(sys.argv[2])
        print(format_result(result, "info"))
    
    elif command == "kill":
        if len(sys.argv) < 3:
            print("请提供 PID")
            sys.exit(1)
        pid = sys.argv[2]
        signal = sys.argv[3] if len(sys.argv) > 3 else "TERM"
        result = kill_process(pid, signal)
        print(format_result(result, "kill"))
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)
