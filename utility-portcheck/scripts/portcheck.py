#!/usr/bin/env python3
"""
端口占用查询 - 查看端口被哪个进程占用
完全本地查询，无需 API
"""

import sys
import json
import subprocess
import os


def check_port(port: int) -> dict:
    """检查端口占用情况"""
    try:
        # 使用 lsof 检查
        try:
            result = subprocess.run(
                ["lsof", "-i", f":{port}", "-n", "-P"],
                capture_output=True, text=True, timeout=5
            )
            
            if result.returncode == 0 and result.stdout.strip():
                lines = result.stdout.strip().split("\n")
                header = lines[0].split()
                processes = []
                
                for line in lines[1:]:
                    parts = line.split()
                    if len(parts) >= 9:
                        processes.append({
                            "command": parts[0],
                            "pid": parts[1],
                            "user": parts[2],
                            "type": parts[3],
                            "device": parts[4],
                            "protocol": parts[8].split(":")[0] if ":" in parts[8] else parts[8],
                            "state": parts[9] if len(parts) > 9 else "LISTEN"
                        })
                
                return {
                    "ok": True,
                    "port": port,
                    "status": "occupied",
                    "processes": processes,
                    "count": len(processes)
                }
            else:
                return {
                    "ok": True,
                    "port": port,
                    "status": "free",
                    "message": f"端口 {port} 未被占用"
                }
        except FileNotFoundError:
            # lsof 不可用，尝试 netstat
            return check_port_netstat(port)
            
    except Exception as e:
        return {"ok": False, "error": str(e)}


def check_port_netstat(port: int) -> dict:
    """使用 netstat 检查端口（备用方法）"""
    try:
        result = subprocess.run(
            ["netstat", "-tlnp"],
            capture_output=True, text=True, timeout=5
        )
        
        if result.returncode == 0:
            for line in result.stdout.split("\n"):
                if f":{port}" in line:
                    parts = line.split()
                    if len(parts) >= 7:
                        pid_program = parts[-1]
                        if "/" in pid_program:
                            pid, program = pid_program.split("/")
                        else:
                            pid, program = "-", pid_program
                        
                        return {
                            "ok": True,
                            "port": port,
                            "status": "occupied",
                            "processes": [{
                                "pid": pid,
                                "command": program,
                                "user": "-",
                                "state": "LISTEN"
                            }],
                            "count": 1
                        }
            
            return {
                "ok": True,
                "port": port,
                "status": "free",
                "message": f"端口 {port} 未被占用"
            }
        else:
            return {"ok": False, "error": "无法检查端口状态"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def list_listening_ports() -> dict:
    """列出所有监听中的端口"""
    try:
        result = subprocess.run(
            ["ss", "-tlnp"],
            capture_output=True, text=True, timeout=5
        )
        
        if result.returncode == 0:
            ports = []
            for line in result.stdout.split("\n")[1:]:  # 跳过标题行
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 5:
                        # 提取端口号
                        addr = parts[4]
                        if ":" in addr:
                            port = addr.split(":")[-1]
                            process = parts[-1] if len(parts) > 5 else "-"
                            ports.append({
                                "port": port,
                                "process": process
                            })
            
            return {
                "ok": True,
                "count": len(ports),
                "ports": ports[:50]  # 限制显示 50 个
            }
        else:
            # 尝试 netstat
            return list_listening_ports_netstat()
    except Exception as e:
        return {"ok": False, "error": str(e)}


def list_listening_ports_netstat() -> dict:
    """使用 netstat 列出监听端口（备用）"""
    try:
        result = subprocess.run(
            ["netstat", "-tlnp"],
            capture_output=True, text=True, timeout=5
        )
        
        if result.returncode == 0:
            ports = []
            for line in result.stdout.split("\n"):
                if "LISTEN" in line:
                    parts = line.split()
                    if len(parts) >= 6:
                        addr = parts[3]
                        if ":" in addr:
                            port = addr.split(":")[-1]
                            process = parts[-1] if len(parts) > 6 else "-"
                            ports.append({
                                "port": port,
                                "process": process
                            })
            
            return {
                "ok": True,
                "count": len(ports),
                "ports": ports[:50]
            }
        else:
            return {"ok": False, "error": "无法列出端口"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def format_result(result: dict, check_type: str) -> str:
    """格式化结果"""
    if not result.get("ok"):
        return f"⚠️ 查询失败：{result.get('error')}"
    
    if check_type == "check":
        if result.get("status") == "occupied":
            lines = [f"🔌 端口 {result['port']} 被占用\n"]
            lines.append(f"占用进程数：{result['count']}\n")
            
            for i, proc in enumerate(result['processes'][:5], 1):
                lines.append(f"{i}. 进程：{proc.get('command', 'Unknown')}")
                lines.append(f"   PID: {proc.get('pid', 'Unknown')}")
                lines.append(f"   用户：{proc.get('user', 'Unknown')}")
                lines.append(f"   状态：{proc.get('state', 'Unknown')}")
                lines.append("")
            
            return "\n".join(lines)
        else:
            return f"🔌 端口检查\n\n端口 {result['port']}: ✅ 空闲"
    
    if check_type == "list":
        lines = [f"🔌 监听中的端口（共{result['count']}个）\n"]
        for item in result['ports'][:20]:
            lines.append(f"端口 {item['port']}: {item['process']}")
        
        if result['count'] > 20:
            lines.append(f"\n... 还有 {result['count'] - 20} 个端口")
        
        return "\n".join(lines)
    
    return str(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python portcheck.py <命令> [参数]",
            "commands": [
                "check <端口> - 检查端口占用",
                "list - 列出所有监听端口"
            ],
            "examples": [
                "python portcheck.py check 80",
                "python portcheck.py check 3306",
                "python portcheck.py list"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "check":
        if len(sys.argv) < 3:
            print("请提供端口号")
            sys.exit(1)
        port = int(sys.argv[2])
        result = check_port(port)
        print(format_result(result, "check"))
    
    elif command == "list":
        result = list_listening_ports()
        print(format_result(result, "list"))
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)
