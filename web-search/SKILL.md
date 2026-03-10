---
name: web-search
description: 网络搜索和信息获取技能。使用 web_search 和 web_fetch 工具进行高效网络研究。适用于搜索网络信息、查找资料、研究主题、获取最新数据、验证事实、查找文档或教程。
---

# Web Search Skill

## 核心能力

本技能提供以下网络搜索能力：

1. **web_search** - 使用 Perplexity Search API 搜索网络
2. **web_fetch** - 抓取网页内容并提取为 Markdown/文本

## 工具使用

### web_search

用于搜索网络获取结构化结果。

```python
# 基本搜索
web_search(query="Python 异步编程教程")

# 高级搜索参数
web_search(
    query="AI agent framework",
    count=5,                    # 结果数量 (1-10)
    freshness="week",           # 时间过滤：day|week|month|year
    language="en",              # 语言：en|zh|de|fr 等
    country="US",               # 地区：US|CN|DE 等
    max_tokens=50000,           # 总 token 预算
    max_tokens_per_page=2048,   # 每页 token 上限
    domain_filter=["-reddit.com"]  # 域名过滤
)
```

**参数说明：**

| 参数 | 类型 | 说明 |
|------|------|------|
| query | string | 搜索关键词（必需） |
| count | number | 结果数量，默认 5，最大 10 |
| freshness | string | 时间过滤：day/week/month/year |
| language | string | ISO 639-1 语言代码 |
| country | string | 2 字母国家代码 |
| max_tokens | number | 总 token 预算，默认 25000 |
| domain_filter | array | 域名白名单或黑名单（如 `-reddit.com`） |

### web_fetch

用于抓取单个网页并提取内容。

```python
# 基本抓取
web_fetch(url="https://example.com/article")

# 指定提取模式
web_fetch(
    url="https://example.com/article",
    extractMode="markdown",  # 或 "text"
    maxChars=10000           # 最大字符数
)
```

## 搜索策略

### 1. 选择工具

- **web_search** → 需要多个来源、比较信息、找最新内容
- **web_fetch** → 已有具体 URL、需要深度内容

### 2. 搜索优化

**好的查询：**
- 具体明确：`"Python asyncio tutorial 2025"`
- 包含上下文：`"best React state management for large apps"`
- 使用引号：`"exact phrase to match"`

**避免：**
- 太宽泛：`"Python"` → 改为 `"Python web framework comparison"`
- 缺少上下文：`"error fix"` → 改为 `"Django 404 error middleware fix"`

### 3. 迭代搜索

如果首次搜索结果不理想：

1. 调整关键词（更具体或换角度）
2. 添加时间过滤（`freshness="week"`）
3. 排除低质量来源（`domain_filter=["-reddit.com", "-quora.com"]`）
4. 切换语言/地区

## 结果处理

### web_search 返回结构

```json
{
  "results": [
    {
      "title": "页面标题",
      "url": "https://...",
      "snippet": "摘要内容"
    }
  ]
}
```

### 深度抓取流程

1. 先用 `web_search` 找相关页面
2. 从结果中选择最相关的 URL
3. 用 `web_fetch` 抓取完整内容
4. 提取关键信息回答用户

## 最佳实践

### ✅ 推荐做法

- 搜索前思考：用户真正需要什么信息？
- 优先用 `web_search` 探索，再用 `web_fetch` 深入
- 对技术问题添加年份确保信息新鲜度
- 多来源交叉验证重要信息
- 引用来源 URL 让用户可以查证

### ❌ 避免

- 不要盲目相信第一个搜索结果
- 不要抓取整个网站（用 `maxChars` 限制）
- 不要忽略时间敏感性（新闻、价格、版本信息）
- 不要返回原始 JSON，要整理成人类可读格式

## 特殊场景

### 学术研究

```python
web_search(
    query="quantum computing error correction",
    domain_filter=["nature.com", "arxiv.org", "ieee.org"],
    freshness="year"
)
```

### 技术文档

```python
web_search(
    query="Next.js 15 server components documentation",
    freshness="month"
)
```

### 新闻/事件

```python
web_search(
    query="AI regulation EU",
    freshness="week",
    count=10
)
```

### 产品对比

```python
# 先搜索对比文章
web_search(query="VS Code vs Cursor AI IDE comparison 2025")

# 再抓取具体内容
web_fetch(url="https://...")
```

## 错误处理

- **无结果** → 调整关键词或扩大搜索范围
- **内容过长** → 用 `maxChars` 或 `max_tokens` 限制
- **付费墙** → 尝试找替代来源或摘要
- **过期信息** → 添加 `freshness` 过滤

## 输出格式

向用户汇报时：

1. **总结核心发现**（2-3 句）
2. **列出关键来源**（带链接）
3. **标注时间敏感性**（如"这是 2024 年的数据"）
4. **提供下一步建议**（如需更深入研究）

**示例：**

> 根据搜索结果，Next.js 15 的主要变化包括：
> 
> 1. **Turbopack 默认启用** - 构建速度提升 3-5 倍
> 2. **Server Actions 稳定版** - 无需实验性标志
> 3. **新的路由约定** - 支持并行路由
> 
> 来源：
> - [Next.js 15 官方发布](https://nextjs.org/blog/next-15)
> - [迁移指南](https://nextjs.org/docs/app/building-your-application/upgrading/version-15)
> 
> 需要我帮你抓取具体的迁移步骤吗？

---

**参考文档：**
- 搜索技巧：见 `references/search-techniques.md`
- 示例查询：见 `references/example-queries.md`
