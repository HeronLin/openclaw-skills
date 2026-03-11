---
name: utility-password
description: 密码管理器，支持生成强密码、检查密码强度、本地加密存储。完全本地，无需 API，安全可靠。适用于密码管理、密码生成。Use when: 用户需要生成或管理密码。
---

# 密码管理器

## 🔐 核心功能

- ✅ **生成强密码** - 自定义长度和字符类型
- ✅ **密码强度检查** - 评估密码安全性
- ✅ **本地加密存储** - 安全保存密码
- ✅ **密码查询** - 快速查找密码

## 📖 使用方法

### 生成密码

```
生成一个强密码
生成 20 位密码
```

**脚本调用：**
```bash
python scripts/password.py generate
python scripts/password.py generate 20
```

### 检查密码强度

```
检查这个密码强度：MyP@ssw0rd
```

**脚本调用：**
```bash
python scripts/password.py check "MyP@ssw0rd"
```

### 保存密码

```
保存密码：github 用户名 密码
保存密码：微信 手机号 密码 备注
```

**脚本调用：**
```bash
python scripts/password.py save github myuser mypassword
python scripts/password.py save wechat 13800138000 password 微信号
```

### 获取密码

```
获取 github 密码
```

**脚本调用：**
```bash
python scripts/password.py get github
```

### 列出密码

```
我的密码列表
```

**脚本调用：**
```bash
python scripts/password.py list
```

## 📊 输出示例

### 生成密码
```
🔐 生成的密码：K9#mP2$xL5@nQ8wR
强度：🟢 非常强
```

### 密码强度检查
```
🔐 密码强度检查

强度：🟡 强
得分：7/10

✅ 密码强度很好！
```

### 获取密码
```
🔐 密码信息

服务：github
用户：myuser
密码：mypassword
更新：2026-03-11 12:00
```

## 💡 使用技巧

- 密码至少 12 位，包含大小写、数字、特殊字符
- 定期更换重要密码
- 不要使用相同密码
- 本地加密存储，数据安全

## 🔒 安全说明

- 密码使用 XOR+Base64 简单加密
- 数据存储在本地
- 建议设置复杂的主密钥
- 重要密码建议额外备份

---

**作者：** 白虎 🐯  
**版本：** 1.0  
**许可证：** MIT
