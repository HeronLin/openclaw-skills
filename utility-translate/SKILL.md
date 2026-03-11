---
name: utility-translate
description: 免费翻译技能，支持 100+ 语言。使用 MyMemory API，无需 Key。适用于文本翻译、语言学习、跨语言交流。Use when: 用户需要翻译文本。
---

# 翻译技能

## 🌐 核心特点

- ✅ **完全免费** - 无需 API Key
- ✅ **100+ 语言** - 全球主要语言
- ✅ **自动检测** - 智能识别源语言
- ✅ **简单快速** - 秒级返回

## 📖 支持的语言

| 代码 | 语言 | 代码 | 语言 |
|------|------|------|------|
| zh | 中文 | en | 英语 |
| ja | 日语 | ko | 韩语 |
| fr | 法语 | de | 德语 |
| es | 西班牙语 | ru | 俄语 |
| it | 意大利语 | pt | 葡萄牙语 |

## 📖 使用方法

### 基本翻译

```
把这句话翻译成英文：你好
翻译成中文：Hello World
```

### 脚本调用

```bash
# 中译英
python scripts/translate.py "你好" en

# 英译中
python scripts/translate.py "Hello" zh

# 日译中
python scripts/translate.py "こんにちは" zh
```

## 📊 输出示例

```
🌐 翻译结果

原文：Hello World

译文：你好世界

语言：en → zh
```

## 💡 使用技巧

- 自动检测源语言（可省略）
- 支持长文本（建议<500 字）
- 专业术语可能不够准确
- 每日免费 5000 字

---

**作者：** 白虎 🐯  
**版本：** 1.0  
**许可证：** MIT
