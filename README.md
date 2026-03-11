# OpenClaw Skills Collection

🦞 龙虾军团的 OpenClaw 技能集合

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skills](https://img.shields.io/badge/skills-1-blue)](#skills)

## 📦 安装

```bash
npx skills install https://github.com/HeronLin/openclaw-skills
```

## 🚀 已发布的技能

### 🦆 duck-search ⭐ 推荐

**完全免费**的多功能搜索技能！

**功能：**
- 🔍 **文字搜索** - 网页、文档、教程
- 🖼️ **图片搜索** - 找素材、壁纸、图标
- 📰 **新闻搜索** - 最新资讯、行业动态
- 🎬 **视频搜索** - 教程、演讲、演示

**特点：**
- ✅ 无需 API Key
- ✅ 无需注册
- ✅ 开箱即用
- ✅ 隐私保护

**安装依赖：**
```bash
pip install ddgs
```

**示例：**
```
"帮我搜索 Python 教程"        # 文字搜索
"找些 Python 的图片"           # 图片搜索
"看看最新的 AI 新闻"           # 新闻搜索
"帮我找 Python 入门视频"       # 视频搜索
```

📖 [查看安装指南](./duck-search/INSTALL.md)

---

### 🔍 web-search

专业的网络搜索技能（需要 Perplexity API Key）

**功能：**
- 使用 Perplexity API 进行高效网络搜索
- 支持时间/语言/地区过滤
- 网页内容抓取和提取为 Markdown

**示例：**
```
"帮我搜索 2025 年最好的 AI IDE"
"查找 Next.js 15 的迁移指南"
```

📖 [查看详细文档](./web-search/SKILL.md)

## 📋 技能列表

### 🔍 搜索类

| 技能 | 描述 | 状态 |
|------|------|------|
| [duck-search](./duck-search/) | 免费网络搜索（文字/图片/新闻/视频） | ✅ 已发布 |
| [web-search](./web-search/) | 专业搜索（需要 Perplexity API Key） | ✅ 已发布 |

### 🛠️ 工具类

| 技能 | 描述 | 状态 |
|------|------|------|
| [utility-weather](./utility-weather/) | 天气查询（免费，全球支持） | ✅ 已发布 |
| [utility-image](./utility-image/) | 图片处理（压缩/转换/水印） | ✅ 已发布 |
| [utility-convert](./utility-convert/) | 文件转换（PDF/Word/Excel 等） | ✅ 已发布 |
| [utility-translate](./utility-translate/) | 翻译（100+ 语言，免费） | ✅ 已发布 |
| [utility-todo](./utility-todo/) | 待办事项管理 | ✅ 已发布 |
| [utility-qrcode](./utility-qrcode/) | 二维码生成 | ✅ 已发布 |

### 📈 金融类

| 技能 | 描述 | 状态 |
|------|------|------|
| [akshare-stock](./akshare-stock/) | A 股分析（实时行情/基本面/板块） | ✅ 已发布 |

## 🛠️ 开发自己的技能

参考资源：
- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [Skill Creator 指南](https://github.com/openclaw/openclaw/tree/main/skills/skill-creator)
- [ClawHub](https://clawhub.ai) - 发现和分享技能

## 📬 反馈与建议

- 🐛 报告问题：[Create an issue](https://github.com/HeronLin/openclaw-skills/issues)
- 💡 功能建议：欢迎提 Issue
- 🤝 贡献代码：欢迎 PR

## 📄 许可证

MIT License

---

_由白虎 🐯 维护 | 龙虾军团出品 🦞_
