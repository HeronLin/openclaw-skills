#!/usr/bin/env python3
"""
DuckDuckGo 搜索脚本 - 完全免费，无需 API Key
使用 duckduckgo_search 库
"""

import sys
import json

try:
    from ddgs import DDGS
except ImportError:
    print(json.dumps({
        "error": "ddgs 未安装",
        "install": "pip install ddgs"
    }, ensure_ascii=False))
    sys.exit(1)


def search(query, max_results=5):
    """
    执行 DuckDuckGo 搜索
    
    Args:
        query: 搜索关键词
        max_results: 最大结果数（默认 5）
    
    Returns:
        搜索结果列表
    """
    try:
        results = []
        with DDGS() as ddgs:
            for result in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("href", ""),
                    "snippet": result.get("body", "")
                })
        return results
    except Exception as e:
        return {"error": str(e)}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "缺少搜索关键词",
            "usage": "python duck_search.py <搜索关键词> [结果数量]"
        }, ensure_ascii=False))
        sys.exit(1)
    
    query = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    results = search(query, max_results)
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
