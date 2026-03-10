# 📈 股票分析 Skill 配置完成

## ✅ 配置状态

| 项目 | 状态 | 说明 |
|------|------|------|
| **Skill 安装** | ✅ 完成 | `~/.openclaw/workspace/main/skills/akshare-stock` |
| **Python 环境** | ✅ 完成 | 虚拟环境 + akshare 1.18.35 |
| **OpenClaw 配置** | ✅ 完成 | 已添加到 `openclaw.json` |
| **快捷脚本** | ✅ 完成 | `run.sh` 可执行 |

---

## 🚀 使用方法

### 方法 1：直接在 QQ 中问我（推荐）

现在你可以直接在 QQ 里问我股票相关的问题，我会自动调用股票分析 skill：

```
景旺电子 603228
贵州茅台最新行情
今天 A 股大盘怎么样
主力资金流入前十
宁德时代 K 线分析
```

### 方法 2：命令行调用

```bash
# 使用快捷脚本
/home/okl/.openclaw/workspace/main/skills/akshare-stock/run.sh "景旺电子 603228"

# 或直接使用 Python
cd /home/okl/.openclaw/workspace/main/skills/akshare-stock
source .venv/bin/activate
python3 main.py --query "景旺电子 603228"
```

### 方法 3：添加 Shell 别名（可选）

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
source /home/okl/.openclaw/workspace/main/skills/akshare-stock/stock-alias.sh

# 然后可以这样用：
stock "景旺电子 603228"
stock-dapan  # 查看大盘
stock-flow   # 查看资金流
```

---

## 📊 支持的功能

### 大盘行情
- "A 股大盘" / "上证指数" / "今天股市怎么样"

### 个股分析
- "景旺电子 603228" / "贵州茅台" / "600519"
- "宁德时代 K 线" / "比亚迪分时"

### 资金流向
- "主力资金流入前十"
- "北向资金今天流向"
- "行业资金流向"

### 板块分析
- "行业板块涨幅榜"
- "AI 概念板块"
- "今天哪个板块最强"

### 其他功能
- "今日涨停统计"
- "茅台财务指标"
- "沪深 300 成分股"
- "IF 主力合约"（期货）
- "腾讯控股"（港股）
- "英伟达"（美股）

---

## ⚙️ 技术细节

- **数据源**: AKShare 1.18.35（免费、实时）
- **Python 版本**: 3.13.7
- **虚拟环境**: `/home/okl/.openclaw/workspace/main/skills/akshare-stock/.venv`
- **依赖**: akshare, pandas, numpy

---

## 🔧 维护命令

```bash
# 更新 akshare
cd /home/okl/.openclaw/workspace/main/skills/akshare-stock
source .venv/bin/activate
pip install --upgrade akshare

# 检查技能状态
ls -la ~/.openclaw/workspace/main/skills/akshare-stock/

# 测试运行
./run.sh "测试"
```

---

**配置完成时间**: 2026-03-09  
**配置者**: 白虎 🐯
