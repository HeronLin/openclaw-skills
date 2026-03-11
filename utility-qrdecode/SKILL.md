---
name: utility-qrdecode
description: QR 码解析工具，支持读取二维码内容。完全本地处理，无需 API。适用于二维码识别、内容提取。Use when: 用户需要解析二维码图片。
---

# QR 码解析工具

## 📱 核心功能

- ✅ **解析二维码** - 读取图片中的 QR 码
- ✅ **多码识别** - 支持一张图多个二维码
- ✅ **类型识别** - 自动识别 QR/条形码等
- ✅ **位置信息** - 显示二维码在图中的位置

## 📖 使用方法

### 解析二维码

```
解析这张图片的二维码
```

**脚本调用：**
```bash
python scripts/qrdecode.py decode qrcode.png
```

## 📊 输出示例

```
📱 二维码解析

找到 1 个二维码:

1. 类型：QRCODE
   内容：https://github.com/HeronLin/openclaw-skills
   位置：(50, 50)
   大小：200x200
```

## 💡 使用技巧

- 支持 PNG、JPG 等格式
- 可识别多个二维码
- 支持 QR 码和条形码
- 提取 URL、文本等内容

## ⚠️ 依赖安装

```bash
# Ubuntu/Debian
sudo apt install libzbar0
pip install pillow pyzbar

# macOS
brew install zbar
pip install pillow pyzbar
```

---

**作者：** 白虎 🐯  
**版本：** 1.0  
**许可证：** MIT
