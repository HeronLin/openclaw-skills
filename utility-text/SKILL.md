---
name: utility-text
description: 文本处理工具，支持字数统计、文本格式化、编码解码、查找替换、信息提取。完全本地处理，无需 API。适用于文本编辑、数据处理。Use when: 用户需要处理文本。
---

# 文本处理工具

## 📝 核心功能

- ✅ **字数统计** - 中英文、数字、标点分别统计
- ✅ **文本格式化** - 大小写转换、反转、去空格
- ✅ **编码解码** - Base64、URL 编码
- ✅ **查找替换** - 批量替换文本
- ✅ **信息提取** - 提取邮箱、电话、链接、日期

## 📖 使用方法

### 字数统计

```
统计这段话的字数：Hello World 你好世界
```

**脚本调用：**
```bash
python scripts/text.py count "Hello World 你好世界"
```

### 文本格式化

```
转成大写：hello world
转成小写：HELLO WORLD
反转文本：Hello
```

**脚本调用：**
```bash
python scripts/text.py format "hello" uppercase
python scripts/text.py format "HELLO" lowercase
python scripts/text.py format "Hello" reverse
```

### 编码解码

```
Base64 编码：Hello
Base64 解码：SGVsbG8=
URL 编码：你好
```

**脚本调用：**
```bash
python scripts/text.py encode "Hello" base64
python scripts/text.py decode "SGVsbG8=" base64
python scripts/text.py encode "你好" url
```

### 查找替换

```
把这段话的 World 替换成 Python：Hello World
```

**脚本调用：**
```bash
python scripts/text.py replace "Hello World" "World" "Python"
```

### 信息提取

```
从这段话提取邮箱和电话：联系我 email@example.com 或 13800138000
```

**脚本调用：**
```bash
python scripts/text.py extract "联系我 email@example.com 或 13800138000"
```

## 📊 输出示例

### 字数统计
```
📊 字数统计

总字符：20
中文字符：4
英文字母：10
数字：2
标点符号：1
英文单词：2
总行数：1
非空行：1
```

### 信息提取
```
📋 提取的信息

📧 邮箱：email@example.com
📱 电话：13800138000
```

## 💡 使用技巧

- 字数统计支持中英文混合
- Base64 用于简单加密
- URL 编码用于网络传输
- 信息提取支持正则匹配

---

**作者：** 白虎 🐯  
**版本：** 1.0  
**许可证：** MIT
