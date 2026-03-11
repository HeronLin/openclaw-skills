---
name: utility-qrcode
description: 二维码生成技能，支持 URL、文本、WiFi、名片等二维码。可自定义颜色、尺寸。适用于分享链接、WiFi 密码、联系方式。Use when: 用户需要生成二维码。
---

# 二维码生成

## 📱 核心功能

- ✅ **URL 二维码** - 分享网页链接
- ✅ **文本二维码** - 存储任意文本
- ✅ **WiFi 二维码** - 一键连接 WiFi
- ✅ **名片二维码** - 分享联系方式

## 📖 使用方法

### 生成 URL 二维码

```
生成这个链接的二维码：https://github.com
```

**脚本调用：**
```bash
python scripts/qrcode.py url "https://github.com"
```

### 生成 WiFi 二维码

```
生成 WiFi 二维码，SSID 是 HomeWiFi，密码 123456
```

**脚本调用：**
```bash
python scripts/qrcode.py wifi "HomeWiFi" "123456"
```

### 生成名片二维码

```
生成名片二维码，张三，电话 13800138000
```

**脚本调用：**
```bash
python scripts/qrcode.py vcard "张三" "13800138000" "zhangsan@email.com"
```

### 生成文本二维码

```
把这段话转成二维码：Hello World
```

**脚本调用：**
```bash
python scripts/qrcode.py text "Hello World"
```

## 📊 输出示例

```json
{
  "ok": true,
  "message": "✅ 二维码生成成功",
  "output": "qrcode_20260311_114500.png",
  "data": "https://github.com",
  "size": "290x290"
}
```

## 💡 使用技巧

- WiFi 二维码扫描后自动连接
- 名片二维码可导入通讯录
- 支持自定义颜色（--color）
- 调整尺寸（--size 1-20）

## 🎨 高级选项

```bash
# 自定义颜色
python scripts/qrcode.py url "https://..." --color blue --bg white

# 调整大小
python scripts/qrcode.py text "Hello" --size 15

# 指定输出路径
python scripts/qrcode.py url "https://..." --output my_qr.png
```

---

**作者：** 白虎 🐯  
**版本：** 1.0  
**许可证：** MIT
