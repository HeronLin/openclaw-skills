---
name: utility-converter
description: 单位转换技能，支持长度、重量、温度、面积、体积、速度、时间转换。完全本地计算，无需 API。适用于日常单位换算。Use when: 用户需要转换单位。
---

# 单位转换器

## 🔄 支持的转换类型

| 类别 | 支持单位 |
|------|---------|
| **长度** | 米、公里、厘米、毫米、英寸、英尺、码、英里 |
| **重量** | 克、千克、公斤、毫克、磅、盎司、斤、两 |
| **温度** | 摄氏度、华氏度、开尔文 |
| **面积** | 平方米、平方公里、公顷、英亩、平方英尺 |
| **体积** | 升、毫升、立方米、加仑、夸脱、品脱、杯 |
| **速度** | 米/秒、千米/小时、英里/小时、节 |
| **时间** | 秒、分钟、小时、天、周、月、年 |

## 📖 使用方法

### 长度转换

```
100 厘米等于多少米
1 公里是多少英里
```

**脚本调用：**
```bash
python scripts/converter.py 100 cm m length
python scripts/converter.py 1 公里 英里
```

### 重量转换

```
1 公斤等于多少斤
150 磅是多少公斤
```

**脚本调用：**
```bash
python scripts/converter.py 1 kg 斤 weight
python scripts/converter.py 150 lb kg weight
```

### 温度转换

```
32 华氏度等于多少摄氏度
100 摄氏度是多少华氏度
```

**脚本调用：**
```bash
python scripts/converter.py 32 f c temperature
python scripts/converter.py 100 c f temperature
```

### 其他转换

```
1 立方米等于多少升
100 英里每小时是多少千米每小时
```

**脚本调用：**
```bash
python scripts/converter.py 1 m3 l volume
python scripts/converter.py 100 mph km/h speed
```

## 📊 输出示例

```
🔄 转换结果

100 cm = 1 m

类别：length
```

```
🔄 转换结果

1 kg = 2 斤

类别：weight
```

## 💡 使用技巧

- 支持中文和英文单位
- 自动检测转换类别
- 支持小数和科学计数法
- 结果保留 6 位有效数字

---

**作者：** 白虎 🐯  
**版本：** 1.0  
**许可证：** MIT
