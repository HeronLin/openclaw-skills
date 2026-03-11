---
name: utility-markdown
description: Markdown 处理工具，支持转 HTML、统计元素、提取目录、格式化。完全本地处理，无需 API。适用于文档编辑、博客写作。Use when: 用户需要处理 Markdown 文档。
---

# Markdown 处理工具

## 📝 核心功能

- ✅ **转 HTML** - Markdown 转 HTML 代码
- ✅ **元素统计** - 统计标题、链接、代码块等
- ✅ **提取目录** - 自动生成 TOC
- ✅ **格式化** - 清理多余空行和空格

## 📖 使用方法

### Markdown 转 HTML

```
把这段 Markdown 转 HTML：# Hello
```

**脚本调用：**
```bash
python scripts/markdown_tool.py tohtml "# Hello World"
```

### 统计元素

```
统计这个文档的元素
```

**脚本调用：**
```bash
python scripts/markdown_tool.py count "# Title\n\nContent"
```

### 提取目录

```
生成目录
```

**脚本调用：**
```bash
python scripts/markdown_tool.py toc "# Title\n## Section 1\n## Section 2"
```

### 格式化

```
格式化这段 Markdown
```

**脚本调用：**
```bash
python scripts/markdown_tool.py format "# Title\n\n\n\nContent"
```

## 📊 输出示例

### 元素统计
```
📊 Markdown 统计

标题：5
链接：10
图片：3
代码块：2
列表：8
引用：2
粗体：15
斜体：5

字数：1250
字符：5680
行数：120
```

### 提取目录
```
📑 目录

- [Title](#title)
  - [Section 1](#section-1)
  - [Section 2](#section-2)
```

## 💡 使用技巧

- 快速生成文档目录
- 统计文章字数
- 清理格式问题
- 转换为 HTML 预览

---

**作者：** 白虎 🐯  
**版本：** 1.0  
**许可证：** MIT
