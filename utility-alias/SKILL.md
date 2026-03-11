---
name: utility-alias
description: 快捷别名工具，为常用命令创建别名。解决命令太长记不住的问题。适用于提高命令行效率。Use when: 用户需要创建命令别名。
---

# 快捷别名工具

## ⚡ 核心功能

- ✅ **创建别名** - 为长命令创建短别名
- ✅ **删除别名** - 移除不需要的别名
- ✅ **列出别名** - 查看所有别名
- ✅ **查询别名** - 查看某个别名的命令

## 📖 使用方法

### 创建别名

```
给 ls -la 创建别名 ll
给 git status 创建别名 gs
```

**脚本调用：**
```bash
python scripts/alias.py add ll "ls -la"
python scripts/alias.py add gs "git status"
```

### 列出别名

```
查看所有别名
```

**脚本调用：**
```bash
python scripts/alias.py list
```

### 删除别名

```
删除 ll 别名
```

**脚本调用：**
```bash
python scripts/alias.py remove ll
```

## 📊 输出示例

```
📋 别名列表

ll              => ls -la
gs              => git status
gc              => git commit
gco             => git checkout

共 4 个别名
```

## 💡 常用别名推荐

| 别名 | 命令 | 用途 |
|------|------|------|
| ll | ls -la | 详细列表 |
| gs | git status | Git 状态 |
| ga | git add | Git 添加 |
| gc | git commit | Git 提交 |
| gco | git checkout | Git 切换 |
| gp | git push | Git 推送 |
| gl | git pull | Git 拉取 |
| .. | cd .. | 返回上级 |
| ... | cd ../.. | 返回上两级 |

---

**作者：** 白虎 🐯  
**版本：** 1.0  
**许可证：** MIT
