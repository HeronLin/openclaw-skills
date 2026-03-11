---
name: utility-ip
description: IP 地址工具，支持本地/公网 IP 查询、域名解析、反向 DNS、端口扫描。完全本地处理，无需 API。适用于网络诊断、IP 查询。Use when: 用户需要查询 IP 或域名信息。
---

# IP 地址工具

## 🌐 核心功能

- ✅ **本地 IP 查询** - 获取局域网 IP
- ✅ **公网 IP 查询** - 获取外网 IP
- ✅ **域名解析** - 域名转 IP
- ✅ **反向 DNS** - IP 转域名
- ✅ **端口扫描** - 检查端口状态

## 📖 使用方法

### 查询本地 IP

```
我的本地 IP 是多少
```

**脚本调用：**
```bash
python scripts/ip_tool.py local
```

### 查询公网 IP

```
我的公网 IP 是多少
```

**脚本调用：**
```bash
python scripts/ip_tool.py public
```

### 域名解析

```
解析 google.com
```

**脚本调用：**
```bash
python scripts/ip_tool.py resolve google.com
```

### 反向 DNS 查询

```
查询 8.8.8.8 的域名
```

**脚本调用：**
```bash
python scripts/ip_tool.py reverse 8.8.8.8
```

### 端口扫描

```
扫描 localhost 的 22 端口
```

**脚本调用：**
```bash
python scripts/ip_tool.py scan localhost 22
```

## 📊 输出示例

### 本地 IP
```
🌐 本地 IP 信息

主机名：mycomputer
本地 IP: 127.0.1.1
局域网 IP: 192.168.1.100
```

### 公网 IP
```
🌐 公网 IP 信息

公网 IP: 113.91.146.134
来源：OpenDNS
```

### 域名解析
```
🌐 域名解析

域名：google.com
主机名：google.com
IP 地址:
  - 142.250.185.46
  - 142.250.185.47
```

### 端口扫描
```
🟢 端口扫描

主机：localhost
端口：22
状态：open
服务：SSH
```

## 💡 使用技巧

- 公网 IP 查询需要网络连接
- 端口扫描可用于检查服务是否运行
- 反向 DNS 查询识别 IP 来源
- 常见端口自动识别服务

## 🔒 常见端口

| 端口 | 服务 |
|------|------|
| 22 | SSH |
| 80 | HTTP |
| 443 | HTTPS |
| 3306 | MySQL |
| 6379 | Redis |
| 8080 | HTTP 代理 |

---

**作者：** 白虎 🐯  
**版本：** 1.0  
**许可证：** MIT
