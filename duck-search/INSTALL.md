# 安装指南

## 快速安装

```bash
# 1. 安装 Python 依赖
pip install duckduckgo_search

# 2. 测试安装
python scripts/duck_search.py "test"

# 3. 完成！
```

## 详细步骤

### 步骤 1：检查 Python 环境

```bash
python --version
# 需要 Python 3.7+
```

### 步骤 2：安装依赖

**方式 A：pip（推荐）**
```bash
pip install duckduckgo_search
```

**方式 B：pip3**
```bash
pip3 install duckduckgo_search
```

**方式 C：国内镜像**
```bash
pip install duckduckgo_search -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 步骤 3：验证安装

```bash
python scripts/duck_search.py "Python tutorial" 3
```

如果看到 JSON 格式的搜索结果，说明安装成功！

## 常见问题

### Q: pip 找不到命令？

**A:** 尝试用 `pip3` 或 `python -m pip`

```bash
python -m pip install duckduckgo_search
```

### Q: 安装失败？

**A:** 检查网络和 Python 版本

```bash
# 检查 Python 版本
python --version

# 升级 pip
python -m pip install --upgrade pip

# 重新安装
pip install duckduckgo_search
```

### Q: 在 OpenClaw 中如何使用？

**A:** 技能会自动调用脚本，确保：
1. 已安装 `duckduckgo_search` 库
2. 脚本有执行权限：`chmod +x scripts/duck_search.py`

## 卸载

```bash
pip uninstall duckduckgo_search
```
