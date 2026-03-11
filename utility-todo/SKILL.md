---
name: utility-todo
description: 待办事项管理技能，支持添加/完成/删除任务，优先级设置，截止日期提醒。适用于任务管理、日程安排、目标追踪。Use when: 用户需要管理待办事项。
---

# 待办事项管理

## ✅ 核心功能

- ✅ **添加任务** - 支持优先级和截止日期
- ✅ **完成任务** - 标记为已完成
- ✅ **删除任务** - 移除不需要的任务
- ✅ **任务分析** - 统计完成情况

## 📖 使用方法

### 添加待办

```
添加待办：明天开会
添加高优先级任务：完成报告 --priority high
添加带截止日期的任务：买机票 --due 2026-03-15
```

**脚本调用：**
```bash
python scripts/todo.py add "明天开会"
python scripts/todo.py add "完成报告" --priority high
python scripts/todo.py add "买机票" --due 2026-03-15
```

### 完成任务

```
完成任务 1
```

**脚本调用：**
```bash
python scripts/todo.py complete 1
```

### 删除任务

```
删除任务 1
```

**脚本调用：**
```bash
python scripts/todo.py delete 1
```

### 查看待办

```
我的待办
查看所有任务
```

**脚本调用：**
```bash
python scripts/todo.py list
python scripts/todo.py list --all
```

### 任务分析

```
分析我的任务完成情况
```

**脚本调用：**
```bash
python scripts/todo.py analyze
```

## 📊 输出示例

```
📋 待办事项

🔴 进行中:
  🔴 #3: 完成报告 (截止：2026-03-12)
  🟡 #2: 明天开会
  🟢 #1: 买咖啡

总计：3 进行中 / 5 已完成
```

## 💡 使用技巧

- 优先级：high/medium/low
- 截止日期格式：YYYY-MM-DD
- 定期清理已完成任务
- 使用 analyze 查看完成情况

---

**作者：** 白虎 🐯  
**版本：** 1.0  
**许可证：** MIT
