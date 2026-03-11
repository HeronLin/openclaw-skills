#!/usr/bin/env python3
"""
Linux 系统信息工具 - 查看 CPU、内存、磁盘、网络等信息
完全本地查询，无需 API
"""

import sys
import json
import os
import platform
import subprocess
from datetime import datetime


def get_system_info() -> dict:
    """获取系统基本信息"""
    try:
        return {
            "ok": True,
            "system": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version()
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def get_cpu_info() -> dict:
    """获取 CPU 信息"""
    try:
        cpu_count = os.cpu_count()
        
        # 读取 /proc/cpuinfo
        cpu_model = "Unknown"
        cpu_cores = 0
        try:
            with open("/proc/cpuinfo", "r") as f:
                content = f.read()
                for line in content.split("\n"):
                    if "model name" in line:
                        cpu_model = line.split(":")[1].strip()
                        break
                cpu_cores = content.count("processor")
        except:
            pass
        
        # 负载
        load_avg = os.getloadavg()
        
        return {
            "ok": True,
            "model": cpu_model,
            "cores": cpu_cores,
            "logical_cores": cpu_count,
            "load_avg": f"{load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}"
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def get_memory_info() -> dict:
    """获取内存信息"""
    try:
        mem_info = {}
        try:
            with open("/proc/meminfo", "r") as f:
                for line in f:
                    parts = line.split(":")
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = parts[1].strip().replace("kB", "").strip()
                        mem_info[key] = int(value)
        except:
            pass
        
        total = mem_info.get("MemTotal", 0) * 1024
        available = mem_info.get("MemAvailable", 0) * 1024
        used = total - available
        usage_percent = (used / total * 100) if total > 0 else 0
        
        return {
            "ok": True,
            "total": f"{total / 1073741824:.1f}GB",
            "used": f"{used / 1073741824:.1f}GB",
            "available": f"{available / 1073741824:.1f}GB",
            "usage": f"{usage_percent:.1f}%"
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def get_disk_info() -> dict:
    """获取磁盘信息"""
    try:
        disk_usage = os.statvfs("/")
        
        total = disk_usage.f_blocks * disk_usage.f_frsize
        free = disk_usage.f_bfree * disk_usage.f_frsize
        available = disk_usage.f_bavail * disk_usage.f_frsize
        used = total - free
        usage_percent = (used / total * 100) if total > 0 else 0
        
        return {
            "ok": True,
            "mount_point": "/",
            "total": f"{total / 1073741824:.1f}GB",
            "used": f"{used / 1073741824:.1f}GB",
            "available": f"{available / 1073741824:.1f}GB",
            "usage": f"{usage_percent:.1f}%"
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def get_network_info() -> dict:
    """获取网络信息"""
    try:
        import socket
        hostname = socket.gethostname()
        
        # 获取 IP
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
        except:
            ip = "127.0.0.1"
        
        return {
            "ok": True,
            "hostname": hostname,
            "ip": ip
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def get_uptime() -> dict:
    """获取系统运行时间"""
    try:
        with open("/proc/uptime", "r") as f:
            uptime_seconds = float(f.readline().split()[0])
        
        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        
        return {
            "ok": True,
            "uptime_seconds": int(uptime_seconds),
            "uptime": f"{days}天 {hours}小时 {minutes}分钟"
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def format_result(result: dict, info_type: str) -> str:
    """格式化结果"""
    if not result.get("ok"):
        return f"⚠️ 获取失败：{result.get('error')}"
    
    if info_type == "system":
        return f"🖥️ 系统信息\n\n系统：{result['system']}\n主机名：{result['node']}\n内核：{result['release']}\n架构：{result['machine']}\nPython: {result['python_version']}"
    
    if info_type == "cpu":
        return f"🖥️ CPU 信息\n\n型号：{result['model']}\n物理核心：{result['cores']}\n逻辑核心：{result['logical_cores']}\n负载：{result['load_avg']}"
    
    if info_type == "memory":
        return f"📊 内存信息\n\n总计：{result['total']}\n已用：{result['used']}\n可用：{result['available']}\n使用率：{result['usage']}"
    
    if info_type == "disk":
        return f"💾 磁盘信息（/）\n\n总计：{result['total']}\n已用：{result['used']}\n可用：{result['available']}\n使用率：{result['usage']}"
    
    if info_type == "network":
        return f"🌐 网络信息\n\n主机名：{result['hostname']}\nIP 地址：{result['ip']}"
    
    if info_type == "uptime":
        return f"⏱️ 系统运行时间\n\n{result['uptime']}"
    
    return str(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python sysinfo.py <命令>",
            "commands": [
                "system - 系统信息",
                "cpu - CPU 信息",
                "memory - 内存信息",
                "disk - 磁盘信息",
                "network - 网络信息",
                "uptime - 运行时间",
                "all - 全部信息"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "system":
        result = get_system_info()
        print(format_result(result, "system"))
    elif command == "cpu":
        result = get_cpu_info()
        print(format_result(result, "cpu"))
    elif command == "memory":
        result = get_memory_info()
        print(format_result(result, "memory"))
    elif command == "disk":
        result = get_disk_info()
        print(format_result(result, "disk"))
    elif command == "network":
        result = get_network_info()
        print(format_result(result, "network"))
    elif command == "uptime":
        result = get_uptime()
        print(format_result(result, "uptime"))
    elif command == "all":
        print("🖥️ 完整系统信息\n")
        print(format_result(get_system_info(), "system"))
        print()
        print(format_result(get_cpu_info(), "cpu"))
        print()
        print(format_result(get_memory_info(), "memory"))
        print()
        print(format_result(get_disk_info(), "disk"))
        print()
        print(format_result(get_network_info(), "network"))
        print()
        print(format_result(get_uptime(), "uptime"))
    else:
        print(f"未知命令：{command}")
        sys.exit(1)
