---
name: utility-hash
description: 哈希计算工具，支持 MD5、SHA1、SHA256、SHA512。完全本地计算，无需 API。适用于文件校验、密码哈希、数据完整性验证。Use when: 用户需要计算哈希值。
---

# 哈希计算工具

## 🔐 支持的算法

| 算法 | 输出长度 | 用途 |
|------|---------|------|
| **MD5** | 32 字符 | 快速校验（不推荐用于安全） |
| **SHA1** | 40 字符 | 一般校验 |
| **SHA256** | 64 字符 | 推荐，安全性好 |
| **SHA512** | 128 字符 | 高安全性需求 |

## 📖 使用方法

### 计算文本哈希

```
计算 MD5：Hello World
计算 SHA256：Hello World
```

**脚本调用：**
```bash
python scripts/hash_tool.py text "Hello World"
python scripts/hash_tool.py text "Hello World" sha256
```

### 计算文件哈希

```
计算文件的 MD5：test.txt
计算文件的 SHA256：test.txt
```

**脚本调用：**
```bash
python scripts/hash_tool.py file test.txt md5
python scripts/hash_tool.py file test.txt sha256
```

### 比较哈希值

```
比较两个哈希值是否相同
```

**脚本调用：**
```bash
python scripts/hash_tool.py compare abc123... abc123...
```

## 📊 输出示例

### 文本哈希
```
🔐 MD5 哈希

文本：Hello World

哈希值：
b10a8db164e0754105b7a99be72e3fe5

长度：11 字符
```

### 文件哈希
```
🔐 SHA256 哈希（文件）

文件：test.txt
大小：2.5KB

哈希值：
a591a6d40bf420404a011733cfb7b190...
```

## 💡 使用技巧

- MD5 最快但不安全
- SHA256 推荐用于一般用途
- SHA512 最安全但计算较慢
- 大文件分块计算，不占内存

## 🔒 应用场景

- 文件完整性校验
- 下载文件验证
- 密码存储（加盐）
- 数据去重
- 数字签名

---

**作者：** 白虎 🐯  
**版本：** 1.0  
**许可证：** MIT
