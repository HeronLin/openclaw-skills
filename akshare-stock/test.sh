#!/bin/bash
# 测试脚本
cd /home/okl/.openclaw/workspace/main/skills/akshare-stock
source .venv/bin/activate
python3 main.py --query "$1"
