---
name: utility-image
description: 图片处理技能，支持压缩、格式转换、调整大小、添加水印。使用 Pillow 库。适用于图片优化、格式转换、批量处理。Use when: 用户需要处理图片文件。
---

# 图片处理技能

## 🖼️ 核心功能

- ✅ **图片压缩** - 减小文件大小
- ✅ **格式转换** - JPG/PNG/WEBP 互转
- ✅ **调整大小** - 缩放图片尺寸
- ✅ **添加水印** - 文字水印

## 📖 使用方法

### 图片压缩

```
压缩这张图片
把图片压缩到 80% 质量
```

**脚本调用：**
```bash
python scripts/image.py compress photo.jpg 80
```

### 格式转换

```
把图片转成 PNG
转换成 WEBP 格式
```

**脚本调用：**
```bash
python scripts/image.py convert photo.jpg png
```

### 调整大小

```
把图片宽度改成 800
调整图片大小到 1920x1080
```

**脚本调用：**
```bash
python scripts/image.py resize photo.jpg --width 800
python scripts/image.py resize photo.jpg --width 1920 --height 1080
```

### 添加水印

```
给图片添加水印"版权所有"
```

**脚本调用：**
```bash
python scripts/image.py watermark photo.jpg "版权所有" br
```

**位置参数：**
- `tl` - 左上
- `tr` - 右上
- `bl` - 左下
- `br` - 右下（默认）

## 📊 输出示例

### 压缩结果
```json
{
  "ok": true,
  "message": "✅ 压缩成功",
  "original_size": "2.5MB",
  "new_size": "500KB",
  "compression": "80.0%"
}
```

### 转换格式
```json
{
  "ok": true,
  "message": "✅ 格式转换成功",
  "output": "photo.png",
  "format": "PNG"
}
```

## 💡 使用技巧

- 压缩质量建议：70-90（平衡质量和大小）
- 转换 PNG 时保留透明通道
- 调整大小时保持原始比例
- 水印位置根据图片内容选择

---

**作者：** 白虎 🐯  
**版本：** 1.0  
**许可证：** MIT
