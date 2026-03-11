---
name: utility-process
description: 进程管理工具，支持查看进程列表、搜索进程、查看进程详情、终止进程。完全本地查询，无需 API。适用于系统管理、进程监控。Use when: 用户需要管理或查看进程。
---

# 进程管理工具

## 📊 核心功能

- ✅ **进程列表** - 按 CPU/内存排序查看进程
- ✅ **搜索进程** - 根据关键词查找进程
- ✅ **进程详情** - 查看进程详细信息
- ✅ **终止进程** - 发送信号终止进程

## 📖 使用方法

### 查看进程列表

```
查看占用 CPU 最多的进程
查看占用内存最多的进程
```

**脚本调用：**
```bash
python scripts/process.py list cpu 10
python scripts/process.py list memory 10
```

### 搜索进程

```
查找 python 进程
查找 nginx 进程
```

**脚本调用：**
```bash
python scripts/process.py search python
python scripts/process.py search nginx
```

### 查看进程详情

```
查看进程 1234 的详细信息
```

**脚本调用：**
```bash
python scripts/process.py info 1234
```

### 终止进程

```
终止进程 1234
强制终止进程 1234
```

**脚本调用：**
```bash
python scripts/process.py kill 1234
python scripts/process.py kill 1234 KILL
```

## 📊 输出示例

### 进程列表
```
📊 进程列表（按 cpu 排序，前 10 个）

PID      USER       CPU%   MEM%   COMMAND                                             
--------------------------------------------------------------------------------
1234     root       15.2   2.5    /usr/bin/python3 app.py                             
5678     www-data   8.5    5.2    nginx: worker process                               
...
```

### 搜索进程
```
🔍 搜索进程 "python"（找到 3 个）

PID: 1234 | USER: root | CPU: 15.2% | MEM: 2.5%
   命令：/usr/bin/python3 app.py
```

### 进程详情
```
📊 进程信息

PID: 1234
PPID: 1
用户：root
CPU: 15.2%
内存：2.5%
VSZ: 123456
RSS: 78901
状态：S
启动：10:30
时间：01:23:45
命令：/usr/bin/python3 app.py
```

## 💡 使用技巧

- 快速找到占用资源高的进程
- 搜索特定服务进程
- 查看进程详细信息排查问题
- 终止无响应的进程

## ⚠️ 注意事项

- 终止进程需要相应权限
- 使用 KILL 信号前请先尝试 TERM
- 不要随意终止系统关键进程
- 建议先查看进程详情再操作

---

**作者：** 白虎 🐯  
**版本：** 1.0  
**许可证：** MIT
