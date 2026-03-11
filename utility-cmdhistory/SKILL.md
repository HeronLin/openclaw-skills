---
name: utility-cmdhistory
description: 命令历史工具，记录和搜索使用过的命令。解决找不到之前命令的问题。适用于快速查找用过的命令。Use when: 用户需要查找或使用过的命令。
---

# 命令历史工具

## 📋 核心功能

- ✅ **记录命令** - 自动记录使用过的命令
- ✅ **搜索历史** - 按关键词搜索命令
- ✅ **列出最近** - 查看最近使用的命令
- ✅ **清空历史** - 清除所有记录

## 📖 使用方法

### 记录命令

```
记录这个命令
```

**脚本调用：**
```bash
python scripts/cmdhistory.py add "git commit -m 'fix bug'"
```

### 搜索历史

```
查找 git 相关的命令
```

**脚本调用：**
```bash
python scripts/cmdhistory.py search git
```

### 列出最近

```
查看最近用过的命令
```

**脚本调用：**
```bash
python scripts/cmdhistory.py list 10
```

### 清空历史

```
清空命令历史
```

**脚本调用：**
```bash
python scripts/cmdhistory.py clear
```

## 📊 输出示例

### 搜索历史
```
🔍 搜索 "git"（找到 3 条）

1. [2026-03-11 14:30] git commit -m "fix bug"
2. [2026-03-11 14:25] git status
3. [2026-03-11 14:20] git add .
```

### 列出最近
```
📋 最近命令

1. [2026-03-11 14:30] git commit -m "fix bug"
2. [2026-03-11 14:25] git status
3. [2026-03-11 14:20] git add .
4. [2026-03-11 14:15] npm install
5. [2026-03-11 14:10] python test.py
```

## 💡 使用技巧

- 自动记录所有命令
- 支持关键词搜索
- 最多保存 1000 条记录
- 定期清理敏感命令

---

**作者：** 白虎 🐯  
**版本：** 1.0  
**许可证：** MIT
