---
name: utility-base64
description: Base64 编解码工具，支持文本和文件的编码解码。完全本地处理，无需 API。适用于数据编码、文件传输。Use when: 用户需要 Base64 编解码。
---

# Base64 编解码工具

## 🔐 核心功能

- ✅ **文本编码** - 将文本转为 Base64
- ✅ **文本解码** - 将 Base64 还原为文本
- ✅ **文件编码** - 编码任意文件
- ✅ **文件解码** - 还原 Base64 文件

## 📖 使用方法

### 文本编码

```
Base64 编码：Hello World
```

**脚本调用：**
```bash
python scripts/base64_tool.py encode "Hello World"
```

### 文本解码

```
Base64 解码：SGVsbG8gV29ybGQ=
```

**脚本调用：**
```bash
python scripts/base64_tool.py decode "SGVsbG8gV29ybGQ="
```

### 文件编码

```
编码这个文件：test.txt
```

**脚本调用：**
```bash
python scripts/base64_tool.py encodefile test.txt
```

### 文件解码

```
解码这个文件：test.txt.b64
```

**脚本调用：**
```bash
python scripts/base64_tool.py decodefile test.txt.b64
```

## 📊 输出示例

### 文本编码
```
🔐 Base64 编码

原始：Hello World

编码后：
SGVsbG8gV29ybGQ=

原始长度：11 字节
编码后：16 字节
```

### 文件编码
```
✅ 文件 Base64 编码

输入：test.txt
输出：test.txt.b64
大小：2.5KB
```

## 💡 使用技巧

- Base64 编码后体积增加约 33%
- 可用于在文本中传输二进制数据
- 支持任意文件类型
- 编码后可安全通过邮件发送

## 🔒 应用场景

- 邮件附件编码
- 在 JSON/XML 中嵌入二进制数据
- 简单的数据混淆
- 图片转文本存储

---

**作者：** 白虎 🐯  
**版本：** 1.0  
**许可证：** MIT
