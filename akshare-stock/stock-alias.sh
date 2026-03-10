#!/bin/bash
# 股票分析快捷命令
# 添加到 ~/.bashrc 或 ~/.zshrc 后使用：stock "景旺电子 603228"

stock() {
    /home/okl/.openclaw/workspace/main/skills/akshare-stock/run.sh "$1"
}

# 常用别名
alias stock-dapan="/home/okl/.openclaw/workspace/main/skills/akshare-stock/run.sh 'A 股大盘'"
alias stock-flow="/home/okl/.openclaw/workspace/main/skills/akshare-stock/run.sh '主力资金流入前十'"
