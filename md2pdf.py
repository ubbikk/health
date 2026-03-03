#!/usr/bin/env python3
import sys
import markdown
from weasyprint import HTML

def md_to_pdf(md_path, pdf_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    html_body = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
    body {{ font-family: -apple-system, Arial, sans-serif; font-size: 11pt; line-height: 1.5; max-width: 800px; margin: 0 auto; padding: 20px; }}
    h1 {{ font-size: 18pt; border-bottom: 2px solid #333; padding-bottom: 5px; }}
    h2 {{ font-size: 14pt; border-bottom: 1px solid #999; padding-bottom: 3px; margin-top: 20px; }}
    h3 {{ font-size: 12pt; margin-top: 15px; }}
    table {{ border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 9pt; }}
    th, td {{ border: 1px solid #ccc; padding: 4px 8px; text-align: left; }}
    th {{ background-color: #f0f0f0; font-weight: bold; }}
    hr {{ border: none; border-top: 1px solid #ccc; margin: 15px 0; }}
    ul, ol {{ margin: 5px 0; padding-left: 20px; }}
    li {{ margin: 2px 0; }}
    strong {{ font-weight: 700; }}
    p {{ margin: 5px 0; }}
</style></head><body>{html_body}</body></html>"""

    HTML(string=html).write_pdf(pdf_path)
    print(f"Created: {pdf_path}")

if __name__ == '__main__':
    md_to_pdf(sys.argv[1], sys.argv[2])
