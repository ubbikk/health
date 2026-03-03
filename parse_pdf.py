"""
Parse medical PDF documents into structured XML using Claude API.

Usage:
    # Parse a single PDF
    python parse_pdf.py document.pdf

    # Parse multiple PDFs
    python parse_pdf.py doc1.pdf doc2.pdf doc3.pdf

    # Parse all PDFs in a folder
    python parse_pdf.py med_docs/

    # Parse and append to existing XML database (default: parsed_docs/all_280_docs.xml)
    python parse_pdf.py new_doc.pdf --append

    # Parse and append to a custom XML file
    python parse_pdf.py new_doc.pdf --append --db my_records.xml

Requires ANTHROPIC_API_KEY environment variable to be set.
"""

import argparse
import base64
import re
import sys
import traceback
from datetime import datetime
from pathlib import Path

import anthropic

MODEL = "claude-sonnet-4-5-20250929"
MAX_TOKENS = 4096
DEFAULT_DB = "parsed_docs/all_280_docs.xml"

PROMPT = Path(__file__).parent / "prompts" / "transform_one_med_doc_v2.md"


def parse_date_from_xml(xml_text):
    date_match = re.search(r"<date>(.*?)</date>", xml_text)
    if not date_match:
        return datetime.max
    date_str = date_match.group(1).strip()
    for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y"]:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return datetime.max


def process_pdf(pdf_path, prompt, client):
    with open(pdf_path, "rb") as f:
        pdf_data = base64.b64encode(f.read()).decode("utf-8")

    try:
        message = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "document",
                            "source": {
                                "type": "base64",
                                "media_type": "application/pdf",
                                "data": pdf_data,
                            },
                        },
                        {"type": "text", "text": prompt},
                    ],
                },
                {"role": "assistant", "content": "<doc>"},
            ],
        )

        xml = "<doc>" + message.content[0].text
        date = parse_date_from_xml(xml)

        input_cost = (message.usage.input_tokens / 1_000_000) * 3
        output_cost = (message.usage.output_tokens / 1_000_000) * 15
        cost = input_cost + output_cost

        print(f"  OK  {pdf_path} | date={date.strftime('%Y-%m-%d') if date != datetime.max else '???'} | ${cost:.4f}")
        return {"date": date, "path": str(pdf_path), "xml": xml, "cost": cost}

    except Exception as e:
        traceback.print_exc()
        print(f"  FAIL {pdf_path}: {e}")
        return None


def collect_pdfs(paths):
    pdfs = []
    for p in paths:
        p = Path(p)
        if p.is_dir():
            pdfs.extend(sorted(p.glob("*.pdf")))
        elif p.suffix.lower() == ".pdf":
            pdfs.append(p)
        else:
            print(f"Skipping non-PDF: {p}")
    return pdfs


def load_existing_docs(db_path):
    """Load existing <doc>...</doc> blocks from the XML database."""
    if not Path(db_path).exists():
        return []
    text = Path(db_path).read_text()
    docs = re.findall(r"<doc>.*?</doc>", text, re.DOTALL)
    return docs


def write_combined_xml(docs, db_path):
    """Sort docs by date and write the combined XML file."""
    dated = []
    for doc in docs:
        date = parse_date_from_xml(doc)
        dated.append((date, doc))
    dated.sort(key=lambda x: x[0])

    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    with open(db_path, "w") as f:
        f.write("<medical_records>\n")
        for _, doc in dated:
            f.write(doc.strip() + "\n\n")
        f.write("</medical_records>\n")

    print(f"\nWrote {len(dated)} documents to {db_path}")


def main():
    parser = argparse.ArgumentParser(description="Parse medical PDFs into structured XML")
    parser.add_argument("paths", nargs="+", help="PDF files or folders to process")
    parser.add_argument("--append", action="store_true", help="Append results to existing XML database")
    parser.add_argument("--db", default=DEFAULT_DB, help=f"XML database path (default: {DEFAULT_DB})")
    args = parser.parse_args()

    prompt_path = PROMPT
    if not prompt_path.exists():
        print(f"Error: prompt file not found at {prompt_path}")
        sys.exit(1)
    prompt = prompt_path.read_text()

    pdfs = collect_pdfs(args.paths)
    if not pdfs:
        print("No PDF files found.")
        sys.exit(1)

    print(f"Processing {len(pdfs)} PDF(s)...\n")

    client = anthropic.Anthropic()
    results = []
    total_cost = 0

    for pdf in pdfs:
        result = process_pdf(pdf, prompt, client)
        if result:
            results.append(result)
            total_cost += result["cost"]

    print(f"\nProcessed {len(results)}/{len(pdfs)} files | Total cost: ${total_cost:.4f}")

    if not results:
        return

    new_docs = [r["xml"] for r in results]

    if args.append:
        existing = load_existing_docs(args.db)
        all_docs = existing + new_docs
        write_combined_xml(all_docs, args.db)
    else:
        # Print to stdout
        for doc in new_docs:
            print(doc.strip())
            print()


if __name__ == "__main__":
    main()
