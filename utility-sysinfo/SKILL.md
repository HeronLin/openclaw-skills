---
name: utility-sysinfo
description: Linux 系统信息工具，支持查看 CPU、内存、磁盘、网络、运行时间等。完全本地查询，无需 API。适用于系统监控、故障排查。Use when: 用户需要查看系统信息。
---

# Linux 系统信息工具

## 🖥️ 核心功能

- ✅ **系统信息** - 操作系统、内核、架构
- ✅ **CPU 信息** - 型号、核心数、负载
- ✅ **内存信息** - 总量、使用量、使用率
- ✅ **磁盘信息** - 容量、使用量、使用率
- ✅ **网络信息** - 主机名、IP 地址
- ✅ **运行时间** - 系统 uptime

## 📖 使用方法

### 查看系统信息

```
查看系统信息
```

**脚本调用：**
```bash
python scripts/sysinfo.py system
```

### 查看 CPU 信息

```
查看 CPU 信息
```

**脚本调用：**
```bash
python scripts/sysinfo.py cpu
```

### 查看内存信息

```
查看内存使用情况
```

**脚本调用：**
```bash
python scripts/sysinfo.py memory
```

### 查看磁盘信息

```
查看磁盘空间
```

**脚本调用：**
```bash
python scripts/sysinfo.py disk
```

### 查看网络信息

```
查看我的 IP
```

**脚本调用：**
```bash
python scripts/sysinfo.py network
```

### 查看运行时间

```
系统运行了多久
```

**脚本调用：**
```bash
python scripts/sysinfo.py uptime
```

### 完整信息

```
完整系统信息
```

**脚本调用：**
```bash
python scripts/sysinfo.py all
```

## 📊 输出示例

### 系统信息
```
🖥️ 系统信息

系统：Linux
主机名：myserver
内核：5.15.0-91-generic
架构：x86_64
Python: 3.10.12
```

### 内存信息
```
📊 内存信息

总计：16.0GB
已用：8.5GB
可用：7.5GB
使用率：53.1%
```

### 运行时间
```
⏱️ 系统运行时间

15 天 8 小时 32 分钟
```

## 💡 使用技巧

- 快速检查系统资源使用情况
- 排查性能问题时查看负载
- 监控磁盘空间防止爆满
- 查看 uptime 了解系统稳定性

---

**作者：** 白虎 🐯  
**版本：** 1.0  
**许可证：** MIT
