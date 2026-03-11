#!/usr/bin/env python3
"""
DuckDuckGo 搜索增强版 - 支持多种搜索类型
功能：网页搜索、图片搜索、新闻搜索、视频搜索
"""

import sys
import json
from datetime import datetime

try:
    from ddgs import DDGS
except ImportError:
    print(json.dumps({
        "error": "ddgs 未安装",
        "install": "pip install ddgs"
    }, ensure_ascii=False))
    sys.exit(1)


def search_text(query, max_results=5):
    """文字搜索"""
    try:
        results = []
        with DDGS() as ddgs:
            for result in ddgs.text(query, max_results=max_results):
                results.append({
                    "type": "text",
                    "title": result.get("title", ""),
                    "url": result.get("href", ""),
                    "snippet": result.get("body", "")
                })
        return results
    except Exception as e:
        return {"error": str(e)}


def search_images(query, max_results=5):
    """图片搜索"""
    try:
        results = []
        with DDGS() as ddgs:
            for result in ddgs.images(query, max_results=max_results):
                results.append({
                    "type": "image",
                    "title": result.get("title", ""),
                    "image": result.get("image", ""),
                    "source": result.get("source", ""),
                    "url": result.get("url", "")
                })
        return results
    except Exception as e:
        return {"error": str(e)}


def search_news(query, max_results=5):
    """新闻搜索"""
    try:
        results = []
        with DDGS() as ddgs:
            for result in ddgs.news(query, max_results=max_results):
                results.append({
                    "type": "news",
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "source": result.get("source", ""),
                    "date": result.get("date", ""),
                    "snippet": result.get("body", "")
                })
        return results
    except Exception as e:
        return {"error": str(e)}


def search_videos(query, max_results=5):
    """视频搜索"""
    try:
        results = []
        with DDGS() as ddgs:
            for result in ddgs.videos(query, max_results=max_results):
                results.append({
                    "type": "video",
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "source": result.get("source", ""),
                    "duration": result.get("duration", ""),
                    "thumbnail": result.get("thumbnail", "")
                })
        return results
    except Exception as e:
        return {"error": str(e)}


def main():
    if len(sys.argv) < 3:
        print(json.dumps({
            "error": "参数不足",
            "usage": "python duck_search_enhanced.py <搜索类型> <关键词> [结果数量]",
            "types": ["text", "image", "news", "video"]
        }, ensure_ascii=False))
        sys.exit(1)
    
    search_type = sys.argv[1].lower()
    query = sys.argv[2]
    max_results = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    
    print(json.dumps({"query": query, "type": search_type, "timestamp": datetime.now().isoformat()}, ensure_ascii=False))
    
    if search_type == "text":
        results = search_text(query, max_results)
    elif search_type == "image":
        results = search_images(query, max_results)
    elif search_type == "news":
        results = search_news(query, max_results)
    elif search_type == "video":
        results = search_videos(query, max_results)
    else:
        results = {"error": f"不支持的搜索类型：{search_type}"}
    
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
