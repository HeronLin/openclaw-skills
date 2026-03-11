---
name: utility-template
description: 快捷模板工具，为常用文本创建模板。解决重复输入的问题。适用于邮件、报告、文档等重复内容。Use when: 用户需要创建或使用文本模板。
---

# 快捷模板工具

## 📄 核心功能

- ✅ **创建模板** - 保存常用文本
- ✅ **获取模板** - 快速调用模板
- ✅ **列出模板** - 查看所有模板
- ✅ **删除模板** - 移除不需要的模板

## 📖 使用方法

### 创建模板

```
创建邮件开头模板
创建报告模板
```

**脚本调用：**
```bash
python scripts/template.py add email_start "尊敬的客户：\n\n您好！" "邮件开头"
python scripts/template.py add report "项目报告\n\n一、项目概述\n二、进展情况" "报告模板"
```

### 获取模板

```
获取邮件模板
```

**脚本调用：**
```bash
python scripts/template.py get email_start
```

### 列出模板

```
查看所有模板
```

**脚本调用：**
```bash
python scripts/template.py list
```

### 删除模板

```
删除邮件模板
```

**脚本调用：**
```bash
python scripts/template.py remove email_start
```

## 📊 输出示例

### 模板列表
```
📄 模板列表

email_start     - 邮件开头
report          - 报告模板
meeting_note    - 会议纪要

共 3 个模板
```

### 获取模板
```
📄 模板：email_start

描述：邮件开头
创建：2026-03-11 14:30

尊敬的客户：

您好！
```

## 💡 常用模板推荐

| 模板名 | 用途 | 内容 |
|--------|------|------|
| email_start | 邮件开头 | 尊敬的客户：您好！ |
| email_end | 邮件结尾 | 此致 敬礼 |
| meeting_note | 会议纪要 | 时间、地点、参会人员 |
| bug_report | Bug 报告 | 环境、复现步骤、期望结果 |
| pr_template | PR 模板 | 变更内容、测试情况 |

---

**作者：** 白虎 🐯  
**版本：** 1.0  
**许可证：** MIT
