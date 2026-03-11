---
name: utility-json
description: JSON 处理工具，支持格式化、验证、提取、转换 CSV、压缩。完全本地处理，无需 API。适用于 JSON 编辑、数据转换。Use when: 用户需要处理 JSON 数据。
---

# JSON 处理工具

## 📄 核心功能

- ✅ **JSON 格式化** - 美化 JSON 输出
- ✅ **JSON 验证** - 检查格式是否正确
- ✅ **值提取** - 按路径提取 JSON 值
- ✅ **JSON 转 CSV** - 转换为 CSV 格式
- ✅ **JSON 压缩** - 减小文件大小

## 📖 使用方法

### 格式化 JSON

```
格式化这个 JSON：{"name":"test","value":123}
```

**脚本调用：**
```bash
python scripts/json_tool.py format '{"name":"test","value":123}'
```

### 验证 JSON

```
验证 JSON 格式：{"name":"test"}
```

**脚本调用：**
```bash
python scripts/json_tool.py validate '{"name":"test"}'
```

### 提取值

```
提取 JSON 中的 name 值
```

**脚本调用：**
```bash
python scripts/json_tool.py extract '{"user":{"name":"John"}}' user.name
```

### JSON 转 CSV

```
把 JSON 数组转成 CSV
```

**脚本调用：**
```bash
python scripts/json_tool.py tocsv '[{"name":"John","age":30},{"name":"Jane","age":25}]'
```

### 压缩 JSON

```
压缩这个 JSON
```

**脚本调用：**
```bash
python scripts/json_tool.py minify '{"name":"test","value":123}'
```

## 📊 输出示例

### 格式化
```json
{
  "name": "test",
  "value": 123
}
```

### 提取值
```
📄 提取值

路径：user.name
值："John"
```

### JSON 转 CSV
```csv
age,name
30,John
25,Jane
```

## 💡 使用技巧

- 支持嵌套路径：data.items.0.name
- 数组使用索引：items.0
- 压缩可减小 30-50% 体积
- 验证快速检查 JSON 格式

---

**作者：** 白虎 🐯  
**版本：** 1.0  
**许可证：** MIT
