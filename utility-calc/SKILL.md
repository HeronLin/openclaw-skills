---
name: utility-calc
description: 实用计算器，支持数学计算、百分比、日期差、BMI 计算。完全本地计算，无需 API。适用于日常计算、健康管理。Use when: 用户需要进行计算。
---

# 实用计算器

## 🧮 核心功能

- ✅ **数学计算** - 支持加减乘除、三角函数
- ✅ **百分比计算** - 计算占比
- ✅ **日期差** - 计算两个日期间隔
- ✅ **日期加减** - 计算 N 天后的日期
- ✅ **BMI 计算** - 身体健康指数

## 📖 使用方法

### 数学计算

```
计算 2+3*4
计算 sin(30)
计算 sqrt(16)
```

**脚本调用：**
```bash
python scripts/calc.py calc "2+3*4"
python scripts/calc.py calc "sin(30)"
python scripts/calc.py calc "sqrt(16)"
```

### 百分比计算

```
50 占 200 的百分比是多少
```

**脚本调用：**
```bash
python scripts/calc.py percent 50 200
```

### 日期差

```
2026 年 1 月 1 日到 2026 年 12 月 31 日有多少天
```

**脚本调用：**
```bash
python scripts/calc.py datediff 2026-01-01 2026-12-31
```

### 日期加减

```
2026 年 3 月 11 日往后 100 天是哪天
```

**脚本调用：**
```bash
python scripts/calc.py dateadd 2026-03-11 100
```

### BMI 计算

```
计算 BMI，体重 70kg，身高 175cm
```

**脚本调用：**
```bash
python scripts/calc.py bmi 70 175
```

## 📊 输出示例

### 数学计算
```
🧮 计算结果

2+3*4 = 14
```

### 百分比
```
📊 百分比计算

50 占 200 的 25.00%
```

### BMI 计算
```
🏃 BMI 计算

体重：70kg
身高：175cm

BMI: 22.9
类别：正常
```

## 💡 使用技巧

- 支持数学函数：sin, cos, tan, sqrt, pow
- 使用 pi 和 e 常量
- ^ 符号表示幂运算
- BMI 正常范围：18.5-24

## 📐 支持的数学函数

| 函数 | 说明 |
|------|------|
| sin | 正弦 |
| cos | 余弦 |
| tan | 正切 |
| sqrt | 平方根 |
| pow | 幂运算 |
| pi | 圆周率 |
| e | 自然常数 |

---

**作者：** 白虎 🐯  
**版本：** 1.0  
**许可证：** MIT
