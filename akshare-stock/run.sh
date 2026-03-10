#!/bin/bash
# A 股分析 Skill 自动调用脚本
# 用法：./run.sh "景旺电子 603228"

SKILL_DIR="/home/okl/.openclaw/workspace/main/skills/akshare-stock"
VENV_PYTHON="$SKILL_DIR/.venv/bin/python3"

# 检查虚拟环境
if [ ! -f "$VENV_PYTHON" ]; then
    echo "错误：虚拟环境不存在，请先运行：cd $SKILL_DIR && python3 -m venv .venv && source .venv/bin/activate && pip install akshare pandas numpy"
    exit 1
fi

# 执行分析
QUERY="$1"
if [ -z "$QUERY" ]; then
    echo "用法：$0 \"查询内容\""
    echo "示例：$0 \"景旺电子 60328\""
    echo "示例：$0 \"A 股大盘\""
    echo "示例：$0 \"主力资金流入前十\""
    exit 1
fi

cd "$SKILL_DIR"
"$VENV_PYTHON" main.py --query "$QUERY" 2>&1
