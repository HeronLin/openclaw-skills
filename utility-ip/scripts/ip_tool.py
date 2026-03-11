#!/usr/bin/env python3
"""
IP 地址工具 - IP 查询、域名解析、端口扫描
完全本地处理，无需 API
"""

import sys
import json
import socket
import re
from datetime import datetime


def get_local_ip() -> dict:
    """获取本地 IP 地址"""
    try:
        # 获取所有网络接口的 IP
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        # 尝试获取真实局域网 IP
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            real_ip = s.getsockname()[0]
            s.close()
        except:
            real_ip = local_ip
        
        return {
            "ok": True,
            "hostname": hostname,
            "local_ip": local_ip,
            "real_ip": real_ip
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def get_public_ip() -> dict:
    """获取公网 IP（通过 DNS 查询）"""
    try:
        # 使用 OpenDNS 查询公网 IP
        resolver = socket.resolver.Resolver()
        resolver.nameservers = ['resolver1.opendns.com']
        response = resolver.resolve('myip.opendns.com', 'A')
        public_ip = response[0].to_text()
        
        return {
            "ok": True,
            "public_ip": public_ip,
            "source": "OpenDNS"
        }
    except Exception as e:
        return {"ok": False, "error": f"无法获取公网 IP: {e}"}


def resolve_domain(domain: str) -> dict:
    """域名解析"""
    try:
        ip_addresses = socket.gethostbyname_ex(domain)
        
        return {
            "ok": True,
            "domain": domain,
            "hostname": ip_addresses[0],
            "aliases": ip_addresses[1],
            "ip_addresses": ip_addresses[2]
        }
    except Exception as e:
        return {"ok": False, "error": f"解析失败：{e}"}


def reverse_lookup(ip: str) -> dict:
    """反向 DNS 查询"""
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return {
            "ok": True,
            "ip": ip,
            "hostname": hostname
        }
    except Exception as e:
        return {"ok": False, "error": f"反向查询失败：{e}"}


def scan_port(host: str, port: int, timeout: float = 1.0) -> dict:
    """扫描单个端口"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        
        return {
            "port": port,
            "status": "open" if result == 0 else "closed",
            "service": get_common_service(port)
        }
    except Exception as e:
        return {"port": port, "status": "unknown", "error": str(e)}


def get_common_service(port: int) -> str:
    """获取常见端口对应的服务"""
    common_ports = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        993: "IMAPS",
        995: "POP3S",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        6379: "Redis",
        8080: "HTTP-Proxy",
        27017: "MongoDB"
    }
    return common_ports.get(port, "Unknown")


def format_result(result: dict) -> str:
    """格式化结果"""
    if not result.get("ok"):
        return f"⚠️ 操作失败：{result.get('error')}"
    
    if "local_ip" in result:
        return f"🌐 本地 IP 信息\n\n主机名：{result['hostname']}\n本地 IP: {result['local_ip']}\n局域网 IP: {result['real_ip']}"
    
    if "public_ip" in result:
        return f"🌐 公网 IP 信息\n\n公网 IP: {result['public_ip']}\n来源：{result['source']}"
    
    if "ip_addresses" in result:
        ips = "\n".join([f"  - {ip}" for ip in result['ip_addresses']])
        return f"🌐 域名解析\n\n域名：{result['domain']}\n主机名：{result['hostname']}\nIP 地址:\n{ips}"
    
    if "hostname" in result and "ip" in result:
        return f"🌐 反向 DNS 查询\n\nIP: {result['ip']}\n域名：{result['hostname']}"
    
    return str(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python ip_tool.py <命令> [参数]",
            "commands": [
                "local - 获取本地 IP",
                "public - 获取公网 IP",
                "resolve <域名> - 域名解析",
                "reverse <IP> - 反向 DNS 查询",
                "scan <主机> <端口> - 扫描端口"
            ],
            "examples": [
                "python ip_tool.py local",
                "python ip_tool.py public",
                "python ip_tool.py resolve google.com",
                "python ip_tool.py reverse 8.8.8.8",
                "python ip_tool.py scan localhost 22"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "local":
        result = get_local_ip()
    elif command == "public":
        result = get_public_ip()
    elif command == "resolve":
        if len(sys.argv) < 3:
            print("请提供域名")
            sys.exit(1)
        result = resolve_domain(sys.argv[2])
    elif command == "reverse":
        if len(sys.argv) < 3:
            print("请提供 IP 地址")
            sys.exit(1)
        result = reverse_lookup(sys.argv[2])
    elif command == "scan":
        if len(sys.argv) < 4:
            print("请提供主机和端口")
            sys.exit(1)
        host = sys.argv[2]
        port = int(sys.argv[3])
        result = scan_port(host, port)
        if result.get("ok", True):
            status_icon = "🟢" if result.get("status") == "open" else "🔴"
            print(f"{status_icon} 端口扫描\n\n主机：{host}\n端口：{port}\n状态：{result.get('status')}\n服务：{result.get('service', 'Unknown')}")
            sys.exit(0)
    else:
        result = {"ok": False, "error": f"未知命令：{command}"}
    
    print(format_result(result))
