---
name: duck-search
description: 完全免费的多功能网络搜索技能，使用 DuckDuckGo。支持文字/图片/新闻/视频搜索。无需 API Key，无需注册。适用于搜索网络信息、查找图片、获取最新资讯。Use when: 用户需要搜索网络信息、图片、新闻或视频但不想配置 API Key。
---

# DuckDuckGo Search Skill

## 🦆 核心特点

- ✅ **完全免费** - 无需 API Key
- ✅ **无需注册** - 开箱即用
- ✅ **隐私保护** - DuckDuckGo 不追踪用户
- ✅ **多功能** - 支持文字/图片/新闻/视频搜索
- ✅ **简单易用** - 和普通搜索一样

## 🛠️ 安装依赖

使用前需要安装 `duckduckgo_search` 库：

```bash
pip install duckduckgo_search
```

## 📖 使用方法

### 🔍 文字搜索

```
"帮我搜索 Python 教程"
"查找 AI 工具推荐"
"搜索 React hooks 文档"
```

**脚本调用：**
```bash
python scripts/duck_search_enhanced.py text "Python tutorial" 5
```

### 🖼️ 图片搜索

```
"帮我找些 Python 相关的图片"
"搜索 AI 生成的图片"
"找一些风景壁纸"
```

**脚本调用：**
```bash
python scripts/duck_search_enhanced.py image "Python logo" 5
```

**输出格式：**
```json
[
  {
    "type": "image",
    "title": "图片标题",
    "image": "https://.../image.jpg",
    "source": "来源网站",
    "url": "来源页面"
  }
]
```

### 📰 新闻搜索

```
"帮我看看最新的 AI 新闻"
"搜索今天的科技新闻"
"找关于 Python 的最新消息"
```

**脚本调用：**
```bash
python scripts/duck_search_enhanced.py news "AI news" 5
```

**输出格式：**
```json
[
  {
    "type": "news",
    "title": "新闻标题",
    "url": "https://...",
    "source": "新闻来源",
    "date": "2025-03-11",
    "snippet": "摘要"
  }
]
```

### 🎬 视频搜索

```
"帮我找 Python 教程视频"
"搜索 AI 相关的视频"
"找些教学视频"
```

**脚本调用：**
```bash
python scripts/duck_search_enhanced.py video "Python tutorial" 5
```

**输出格式：**
```json
[
  {
    "type": "video",
    "title": "视频标题",
    "url": "https://...",
    "source": "视频来源",
    "duration": "10:25",
    "thumbnail": "缩略图 URL"
  }
]
```

## ⚙️ 配置选项

| 参数 | 默认值 | 说明 |
|------|--------|------|
| max_results | 5 | 最大搜索结果数 |
| timeout | 10s | 搜索超时时间 |

## 📝 最佳实践

### ✅ 推荐

- 用英文关键词搜索（结果更准确）
- 限制结果数量（5-10 个足够）
- 结合 `web_fetch` 抓取详细内容

### ❌ 避免

- 不要频繁搜索（可能触发限流）
- 不要依赖实时新闻（DuckDuckGo 索引有延迟）
- 不要用于学术研究（结果质量一般）

## 🔄 与 web-search 技能对比

| 特性 | duck-search | web-search (Perplexity) |
|------|-------------|------------------------|
| 费用 | 免费 | 需要 API Key |
| 注册 | 不需要 | 需要 |
| 结果质量 | 一般 | 优秀 |
| 实时性 | 一般 | 好 |
| 适合场景 | 日常搜索 | 专业研究 |

## 💡 使用示例

### 示例 1：文字搜索 - 技术教程

**用户：** "帮我找个 Python 异步编程的教程"

**技能执行：**
```bash
python scripts/duck_search_enhanced.py text "Python async programming tutorial" 5
```

**返回结果：**
> 找到以下教程：
> 1. [Real Python - Async IO](https://realpython.com/async-io-python/)
> 2. [Python 官方文档](https://docs.python.org/3/library/asyncio.html)
> ...

### 示例 2：图片搜索 - 找素材

**用户：** "帮我找些 Python 的 logo 图片"

**技能执行：**
```bash
python scripts/duck_search_enhanced.py image "Python logo" 5
```

**返回结果：**
> 找到以下图片：
> 1. Python 官方 Logo - 高清 PNG
> 2. Python 图标 - SVG 格式
> ...

### 示例 3：新闻搜索 - 最新资讯

**用户：** "看看今天有什么 AI 新闻"

**技能执行：**
```bash
python scripts/duck_search_enhanced.py news "AI news" 5
```

**返回结果：**
> 最新新闻：
> 1. [新闻标题] - 来源：TechCrunch - 2025-03-11
> 2. [新闻标题] - 来源：The Verge - 2025-03-11
> ...

### 示例 4：视频搜索 - 学习资源

**用户：** "帮我找 Python 入门视频"

**技能执行：**
```bash
python scripts/duck_search_enhanced.py video "Python tutorial for beginners" 5
```

**返回结果：**
> 找到以下视频：
> 1. [Python 入门教程] - YouTube - 时长：2:30:15
> 2. [Python 快速入门] - Bilibili - 时长：45:20
> ...

### 示例 5：组合使用

**用户：** "帮我研究一下 Tesla 的最新动态，包括新闻和相关图片"

**技能执行：**
1. 搜索新闻：`duck_search_enhanced.py news "Tesla news" 5`
2. 搜索图片：`duck_search_enhanced.py image "Tesla latest" 5`
3. 整合结果汇报

### 示例 6：搜索后抓取详情

**用户：** "帮我看看 Next.js 15 有什么新功能"

**技能执行：**
1. 先用 `duck_search` 搜索 "Next.js 15 new features"
2. 从结果中选择最相关的 URL
3. 用 `web_fetch` 抓取详细内容

## 🐛 故障排除

### 问题：搜索结果为空

**原因：** 网络连接问题或关键词太冷门

**解决：**
- 检查网络连接
- 换用英文关键词
- 简化搜索词

### 问题：提示库未安装

**解决：**
```bash
pip install duckduckgo_search
```

### 问题：搜索速度慢

**原因：** DuckDuckGo 服务器响应慢

**解决：**
- 减少结果数量
- 检查网络环境

## 📚 参考资源

- [duckduckgo_search GitHub](https://github.com/deedy5/duckduckgo_search)
- [DuckDuckGo 官网](https://duckduckgo.com)
- 搜索技巧：见 `references/search-tips.md`

---

**作者：** 白虎 🐯  
**版本：** 1.0  
**许可证：** MIT
