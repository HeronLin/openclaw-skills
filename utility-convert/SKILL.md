---
name: utility-convert
description: 文件转换技能，支持 PDF/Word/Excel/Markdown/HTML 格式互转。适用于文档转换、数据导出、格式标准化。Use when: 用户需要转换文件格式。
---

# 文件转换技能

## 📄 支持的格式

| 转换类型 | 命令 | 依赖 |
|---------|------|------|
| PDF → Word | `pdf2word` | pdf2docx |
| Word → PDF | `word2pdf` | LibreOffice |
| Excel → CSV | `excel2csv` | pandas, openpyxl |
| CSV → Excel | `csv2excel` | pandas, openpyxl |
| Markdown → HTML | `md2html` | markdown |
| HTML → Markdown | `html2md` | html2text |

## 📖 使用方法

### PDF 转 Word

```
把这个 PDF 转成 Word
```

**脚本调用：**
```bash
python scripts/convert.py pdf2word document.pdf
```

### Word 转 PDF

```
把文档转成 PDF
```

**脚本调用：**
```bash
python scripts/convert.py word2pdf report.docx
```

### Excel 转 CSV

```
导出 Excel 为 CSV
```

**脚本调用：**
```bash
python scripts/convert.py excel2csv data.xlsx
```

### CSV 转 Excel

```
把 CSV 转成 Excel
```

**脚本调用：**
```bash
python scripts/convert.py csv2excel data.csv
```

### Markdown 转 HTML

```
把 Markdown 转成网页
```

**脚本调用：**
```bash
python scripts/convert.py md2html readme.md
```

### HTML 转 Markdown

```
把网页转成 Markdown
```

**脚本调用：**
```bash
python scripts/convert.py html2md page.html
```

## 📦 安装依赖

```bash
# 基础转换
pip install pandas openpyxl markdown html2text

# PDF 转 Word
pip install pdf2docx

# Word 转 PDF（需要系统安装 LibreOffice）
# Ubuntu/Debian:
sudo apt install libreoffice
# macOS:
brew install libreoffice
```

## 💡 使用技巧

- PDF 转 Word 保持原有格式
- Excel 转 CSV 自动处理中文编码
- Markdown 转 HTML 包含基础样式
- 大文件转换可能需要时间

---

**作者：** 白虎 🐯  
**版本：** 1.0  
**许可证：** MIT
