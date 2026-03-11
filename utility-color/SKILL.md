---
name: utility-color
description: 颜色工具，支持 HEX/RGB/HSL 转换、调色板生成、对比度检查。完全本地计算，无需 API。适用于设计、前端开发。Use when: 用户需要处理颜色。
---

# 颜色工具

## 🎨 核心功能

- ✅ **HEX 转 RGB** - 十六进制转 RGB
- ✅ **RGB 转 HEX** - RGB 转十六进制
- ✅ **RGB 转 HSL** - RGB 转色相/饱和度/亮度
- ✅ **调色板生成** - 自动生成配色方案
- ✅ **对比度检查** - WCAG 可访问性检查

## 📖 使用方法

### HEX 转 RGB

```
#FF5733 转 RGB
```

**脚本调用：**
```bash
python scripts/color_tool.py hex2rgb #FF5733
```

### RGB 转 HEX

```
255, 87, 51 转 HEX
```

**脚本调用：**
```bash
python scripts/color_tool.py rgb2hex 255 87 51
```

### 生成调色板

```
生成 #FF5733 的类似色
生成互补色
```

**脚本调用：**
```bash
python scripts/color_tool.py palette #FF5733 analogous 5
python scripts/color_tool.py palette #FF5733 complementary 5
```

### 对比度检查

```
检查白色和黑色的对比度
```

**脚本调用：**
```bash
python scripts/color_tool.py contrast #FFFFFF #000000
```

## 📊 输出示例

### 颜色转换
```
🎨 颜色转换

HEX: #FF5733
RGB: rgb(255, 87, 51)
```

### 调色板
```
🎨 调色板（analogous）

基础色：#FF5733
1. #C7FF33
2. #33FF57
3. #33FFC7
4. #3357FF
5. #C733FF
```

### 对比度
```
🎨 对比度检查

颜色 1: #FFFFFF
颜色 2: #000000

对比度：21.00:1
评级：AAA (优秀)
```

## 💡 使用技巧

- 类似色：相邻颜色，和谐统一
- 互补色：对比强烈，吸引注意
- 三色：三种等距颜色，平衡美观
- 单色：同一色相不同亮度

## 🎨 调色板类型

| 类型 | 说明 |
|------|------|
| analogous | 类似色（相邻） |
| complementary | 互补色（相对） |
| triadic | 三色（等边三角形） |
| monochromatic | 单色（不同亮度） |

---

**作者：** 白虎 🐯  
**版本：** 1.0  
**许可证：** MIT
