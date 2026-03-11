#!/usr/bin/env python3
"""
文件转换 - PDF/Word/Excel/Markdown 等格式互转
"""

import sys
import os
import json
from pathlib import Path
import subprocess


def pdf_to_word(pdf_path: str):
    """PDF 转 Word（需要 pdf2docx）"""
    try:
        from pdf2docx import Converter
        output_path = str(Path(pdf_path).with_suffix('.docx'))
        
        cv = Converter(pdf_path)
        cv.convert(output_path)
        cv.close()
        
        return {
            "ok": True,
            "message": "✅ PDF 转 Word 成功",
            "output": output_path
        }
    except ImportError:
        return {"ok": False, "error": "需要安装：pip install pdf2docx"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def word_to_pdf(docx_path: str):
    """Word 转 PDF（需要 LibreOffice 或 pandoc）"""
    try:
        output_path = str(Path(docx_path).with_suffix('.pdf'))
        
        # 尝试使用 LibreOffice
        result = subprocess.run([
            "libreoffice", "--headless", "--convert-to", "pdf",
            "--outdir", str(Path(docx_path).parent), docx_path
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            return {"ok": True, "message": "✅ Word 转 PDF 成功", "output": output_path}
        else:
            return {"ok": False, "error": "LibreOffice 转换失败"}
    except FileNotFoundError:
        return {"ok": False, "error": "需要安装 LibreOffice"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def excel_to_csv(xlsx_path: str):
    """Excel 转 CSV"""
    try:
        import pandas as pd
        output_path = str(Path(xlsx_path).with_suffix('.csv'))
        
        df = pd.read_excel(xlsx_path)
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        return {
            "ok": True,
            "message": "✅ Excel 转 CSV 成功",
            "output": output_path,
            "rows": len(df)
        }
    except ImportError:
        return {"ok": False, "error": "需要安装：pip install pandas openpyxl"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def csv_to_excel(csv_path: str):
    """CSV 转 Excel"""
    try:
        import pandas as pd
        output_path = str(Path(csv_path).with_suffix('.xlsx'))
        
        df = pd.read_csv(csv_path, encoding='utf-8-sig')
        df.to_excel(output_path, index=False)
        
        return {
            "ok": True,
            "message": "✅ CSV 转 Excel 成功",
            "output": output_path,
            "rows": len(df)
        }
    except ImportError:
        return {"ok": False, "error": "需要安装：pip install pandas openpyxl"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def md_to_html(md_path: str):
    """Markdown 转 HTML"""
    try:
        import markdown
        output_path = str(Path(md_path).with_suffix('.html'))
        
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
        
        # 添加 HTML 模板
        full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{Path(md_path).stem}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
        pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background: #f4f4f4; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        return {
            "ok": True,
            "message": "✅ Markdown 转 HTML 成功",
            "output": output_path
        }
    except ImportError:
        return {"ok": False, "error": "需要安装：pip install markdown"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def html_to_md(html_path: str):
    """HTML 转 Markdown"""
    try:
        import html2text
        output_path = str(Path(html_path).with_suffix('.md'))
        
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        h = html2text.HTML2Text()
        h.ignore_links = False
        md_content = h.handle(html_content)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        return {
            "ok": True,
            "message": "✅ HTML 转 Markdown 成功",
            "output": output_path
        }
    except ImportError:
        return {"ok": False, "error": "需要安装：pip install html2text"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python convert.py <命令> <文件路径>",
            "commands": [
                "pdf2word <PDF 文件>",
                "word2pdf <Word 文件>",
                "excel2csv <Excel 文件>",
                "csv2excel <CSV 文件>",
                "md2html <Markdown 文件>",
                "html2md <HTML 文件>"
            ]
        }, ensure_ascii=False))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if len(sys.argv) < 3:
        print(json.dumps({"ok": False, "error": "请提供文件路径"}))
        sys.exit(1)
    
    file_path = sys.argv[2]
    
    if not os.path.exists(file_path):
        print(json.dumps({"ok": False, "error": f"文件不存在：{file_path}"}))
        sys.exit(1)
    
    if command == "pdf2word":
        result = pdf_to_word(file_path)
    elif command == "word2pdf":
        result = word_to_pdf(file_path)
    elif command == "excel2csv":
        result = excel_to_csv(file_path)
    elif command == "csv2excel":
        result = csv_to_excel(file_path)
    elif command == "md2html":
        result = md_to_html(file_path)
    elif command == "html2md":
        result = html_to_md(file_path)
    else:
        result = {"ok": False, "error": f"未知命令：{command}"}
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
