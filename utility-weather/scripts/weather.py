#!/usr/bin/env python3
"""
天气查询 - 使用 wttr.in 免费 API
无需 API Key，支持全球城市
"""

import sys
import json
import requests


def get_weather(city: str, lang: str = "zh"):
    """获取天气信息"""
    try:
        # wttr.in 支持中文输出
        url = f"https://wttr.in/{city}?format=j1&lang={lang}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        # 提取关键信息
        current = data.get("current_condition", [{}])[0]
        weather = {
            "city": city,
            "temp": current.get("temp_C", "?"),
            "feels_like": current.get("FeelsLikeC", "?"),
            "weather": current.get("weatherDesc", [{}])[0].get("value", "?"),
            "humidity": current.get("humidity", "?"),
            "wind": current.get("windspeedKmph", "?"),
            "direction": current.get("winddir16Point", "?"),
        }
        
        # 预报
        forecast = []
        for day in data.get("weather", [])[:3]:
            forecast.append({
                "date": day.get("date", "?"),
                "max": day.get("maxtempC", "?"),
                "min": day.get("mintempC", "?"),
                "weather": day.get("avgtempC", "?")
            })
        
        return {"ok": True, "data": weather, "forecast": forecast}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def format_weather(result: dict) -> str:
    """格式化天气输出"""
    if not result.get("ok"):
        return f"⚠️ 天气查询失败：{result.get('error')}"
    
    data = result["data"]
    lines = [
        f"🌤️ {data['city']} 天气",
        "",
        f"🌡️ 温度：{data['temp']}°C (体感 {data['feels_like']}°C)",
        f"☁️ 天气：{data['weather']}",
        f"💧 湿度：{data['humidity']}%",
        f"💨 风力：{data['direction']} {data['wind']}km/h",
        "",
        "📅 未来 3 天预报:",
    ]
    
    for day in result.get("forecast", []):
        lines.append(f"  {day['date']}: {day['min']}°C ~ {day['max']}°C")
    
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python weather.py <城市名>")
        sys.exit(1)
    
    city = sys.argv[1]
    result = get_weather(city)
    print(format_weather(result))
