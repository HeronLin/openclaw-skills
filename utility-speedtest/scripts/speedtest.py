#!/usr/bin/env python3
"""
网络速度测试 - 测试下载/上传速度、延迟
完全本地测试，无需 API
"""

import sys
import json
import socket
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


def test_latency(host: str = "8.8.8.8", port: int = 53, count: int = 4) -> dict:
    """测试延迟"""
    try:
        latencies = []
        for i in range(count):
            start = time.time()
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((host, port))
                end = time.time()
                sock.close()
                latency = (end - start) * 1000  # 转换为毫秒
                latencies.append(latency)
            except Exception as e:
                latencies.append(None)
        
        valid_latencies = [l for l in latencies if l is not None]
        
        if not valid_latencies:
            return {"ok": False, "error": "无法连接到测试服务器"}
        
        avg_latency = sum(valid_latencies) / len(valid_latencies)
        min_latency = min(valid_latencies)
        max_latency = max(valid_latencies)
        
        return {
            "ok": True,
            "type": "latency",
            "host": f"{host}:{port}",
            "count": count,
            "success": len(valid_latencies),
            "failed": count - len(valid_latencies),
            "avg": f"{avg_latency:.2f}ms",
            "min": f"{min_latency:.2f}ms",
            "max": f"{max_latency:.2f}ms"
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def test_download_speed(url: str = "http://speedtest.tele2.net/1MB.zip", duration: int = 5) -> dict:
    """测试下载速度"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(duration + 2)
        
        start_time = time.time()
        total_bytes = 0
        
        try:
            sock.connect((url.split("/")[2], 80))
            request = f"GET {url} HTTP/1.1\r\nHost: {url.split('/')[2]}\r\nConnection: close\r\n\r\n"
            sock.send(request.encode())
            
            while time.time() - start_time < duration:
                data = sock.recv(8192)
                if not data:
                    break
                total_bytes += len(data)
        except socket.timeout:
            pass
        finally:
            sock.close()
        
        elapsed = time.time() - start_time
        speed_bps = total_bytes / elapsed if elapsed > 0 else 0
        speed_mbps = (speed_bps * 8) / 1048576  # 转换为 Mbps
        
        return {
            "ok": True,
            "type": "download",
            "url": url,
            "duration": f"{elapsed:.2f}s",
            "downloaded": f"{total_bytes / 1024:.1f}KB",
            "speed": f"{speed_mbps:.2f} Mbps"
        }
    except Exception as e:
        return {"ok": False, "error": f"下载测试失败：{e}"}


def test_upload_speed(host: str = "speedtest.tele2.net", duration: int = 5) -> dict:
    """测试上传速度（模拟）"""
    try:
        # 生成测试数据（1MB）
        test_data = b"x" * 1048576
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(duration + 2)
        
        start_time = time.time()
        total_sent = 0
        
        try:
            sock.connect((host, 80))
            
            while time.time() - start_time < duration and total_sent < len(test_data):
                chunk_size = min(8192, len(test_data) - total_sent)
                sent = sock.send(test_data[total_sent:total_sent + chunk_size])
                total_sent += sent
            
            sock.close()
        except socket.timeout:
            pass
        finally:
            sock.close()
        
        elapsed = time.time() - start_time
        speed_bps = total_sent / elapsed if elapsed > 0 else 0
        speed_mbps = (speed_bps * 8) / 1048576  # 转换为 Mbps
        
        return {
            "ok": True,
            "type": "upload",
            "host": host,
            "duration": f"{elapsed:.2f}s",
            "uploaded": f"{total_sent / 1024:.1f}KB",
            "speed": f"{speed_mbps:.2f} Mbps"
        }
    except Exception as e:
        return {"ok": False, "error": f"上传测试失败：{e}"}


def format_result(result: dict) -> str:
    """格式化结果"""
    if not result.get("ok"):
        return f"⚠️ 测试失败：{result.get('error')}"
    
    if result.get("type") == "latency":
        return f"🌐 延迟测试\n\n目标：{result['host']}\n测试次数：{result['count']}\n成功：{result['success']}\n失败：{result['failed']}\n\n平均延迟：{result['avg']}\n最小：{result['min']}\n最大：{result['max']}"
    
    if result.get("type") == "download":
        return f"📥 下载速度测试\n\n目标：{result['url']}\n时长：{result['duration']}\n下载：{result['downloaded']}\n\n速度：{result['speed']}"
    
    if result.get("type") == "upload":
        return f"📤 上传速度测试\n\n目标：{result['host']}\n时长：{result['duration']}\n上传：{result['uploaded']}\n\n速度：{result['speed']}"
    
    return str(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python speedtest.py <命令> [参数]",
            "commands": [
                "latency [主机] [端口] [次数] - 测试延迟",
                "download [URL] [时长] - 测试下载速度",
                "upload [主机] [时长] - 测试上传速度",
                "full - 完整测试（延迟 + 下载）"
            ],
            "examples": [
                "python speedtest.py latency",
                "python speedtest.py latency 8.8.8.8 53 4",
                "python speedtest.py download",
                "python speedtest.py full"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "latency":
        host = sys.argv[2] if len(sys.argv) > 2 else "8.8.8.8"
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 53
        count = int(sys.argv[4]) if len(sys.argv) > 4 else 4
        result = test_latency(host, port, count)
    
    elif command == "download":
        url = sys.argv[2] if len(sys.argv) > 2 else "http://speedtest.tele2.net/1MB.zip"
        duration = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        result = test_download_speed(url, duration)
    
    elif command == "upload":
        host = sys.argv[2] if len(sys.argv) > 2 else "speedtest.tele2.net"
        duration = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        result = test_upload_speed(host, duration)
    
    elif command == "full":
        print("🌐 完整网络测试\n")
        
        # 延迟测试
        print("1️⃣ 延迟测试...")
        latency_result = test_latency()
        print(format_result(latency_result))
        print()
        
        # 下载测试
        print("2️⃣ 下载速度测试...")
        download_result = test_download_speed()
        print(format_result(download_result))
        
        sys.exit(0)
    
    else:
        result = {"ok": False, "error": f"未知命令：{command}"}
    
    print(format_result(result))
