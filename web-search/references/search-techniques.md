# 搜索技巧参考

## 高级搜索语法

### 精确匹配
```
"exact phrase"     # 精确匹配短语
```

### 排除词汇
```
python -tutorial   # 搜索 python 但排除 tutorial
```

### 站内搜索
```
site:github.com    # 只在 github.com 内搜索
```

### 文件类型
```
filetype:pdf       # 只搜索 PDF 文件
```

## 领域过滤策略

### 学术/研究
```
domain_filter: ["nature.com", "science.org", "arxiv.org", "ieee.org", "acm.org"]
```

### 技术文档
```
domain_filter: ["dev.to", "medium.com", "official-docs"]
```

### 排除低质量
```
domain_filter: ["-reddit.com", "-quora.com", "-pinterest.com"]
```

## 时间敏感搜索

| 场景 | freshness | 说明 |
|------|-----------|------|
| 突发新闻 | `day` | 24 小时内 |
| 本周动态 | `week` | 7 天内 |
| 月度总结 | `month` | 30 天内 |
| 年度回顾 | `year` | 1 年内 |

## 多语言搜索

```python
# 中文内容
web_search(query="人工智能发展", language="zh", country="CN")

# 英文技术文档
web_search(query="AI agent architecture", language="en", country="US")

# 多语言对比
web_search(query="electric vehicle market", language="en", country="ALL")
```

## Token 优化

- **count=5** 通常足够，避免不必要的大量结果
- **max_tokens_per_page=2048** 平衡深度和广度
- 需要深度分析时提高 **max_tokens**
