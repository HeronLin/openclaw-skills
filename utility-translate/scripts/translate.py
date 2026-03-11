#!/usr/bin/env python3
"""
翻译技能 - 使用免费翻译 API
支持全球 100+ 语言
"""

import sys
import json
import requests
from urllib.parse import quote


def translate_text(text: str, target_lang: str = "zh", source_lang: str = "auto"):
    """使用 MyMemory 免费翻译 API"""
    try:
        # MyMemory 免费 API（无需 Key，每日 5000 字）
        url = f"https://api.mymemory.translated.net/get?q={quote(text)}&langpair={source_lang}|{target_lang}"
        
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        if data.get("responseStatus", 0) == 200:
            return {
                "ok": True,
                "translated": data.get("responseData", {}).get("translatedText", ""),
                "source_lang": source_lang,
                "target_lang": target_lang,
                "original": text
            }
        else:
            return {
                "ok": False,
                "error": data.get("responseDetails", "翻译失败")
            }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def detect_language(text: str) -> str:
    """检测语言（简化版）"""
    # 简单判断
    if any('\u4e00' <= c <= '\u9fff' for c in text):
        return "zh"
    elif any(ord(c) > 127 for c in text):
        return "auto"
    else:
        return "en"


def format_translation(result: dict) -> str:
    """格式化翻译结果"""
    if not result.get("ok"):
        return f"⚠️ 翻译失败：{result.get('error')}"
    
    lines = [
        "🌐 翻译结果",
        "",
        f"原文：{result['original'][:100]}{'...' if len(result['original']) > 100 else ''}",
        "",
        f"译文：{result['translated']}",
        "",
        f"语言：{result['source_lang']} → {result['target_lang']}"
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python translate.py <文本> [目标语言]",
            "examples": [
                "python translate.py 'Hello' zh",
                "python translate.py '你好' en",
                "python translate.py 'こんにちは' zh"
            ],
            "languages": {
                "zh": "中文",
                "en": "英语",
                "ja": "日语",
                "ko": "韩语",
                "fr": "法语",
                "de": "德语",
                "es": "西班牙语",
                "ru": "俄语"
            }
        }, ensure_ascii=False))
        sys.exit(1)
    
    text = sys.argv[1]
    target = sys.argv[2] if len(sys.argv) > 2 else "zh"
    source = detect_language(text) if len(sys.argv) < 3 else "auto"
    
    result = translate_text(text, target, source)
    print(format_translation(result))
