"""
Streamlit app: Crawl Sanfoundry index page → Generate PDFs per sublink → Bundle ZIP download

Usage:
    pip install streamlit requests beautifulsoup4 lxml reportlab cloudscraper
    streamlit run streamlit_sanfoundry_zip.py
"""

import re
import io
import zipfile
import requests
from urllib.parse import urlparse, urljoin, unquote
from bs4 import BeautifulSoup, Tag
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
from reportlab.lib.units import mm

# --- helpers ---
def slug_from_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.fragment:
        raw = parsed.fragment
    else:
        path = parsed.path.rstrip("/")
        raw = path.split("/")[-1] or parsed.netloc
    raw = unquote(raw)
    raw = re.sub(r"\.[a-zA-Z0-9]+$", "", raw)
    slug = re.sub(r"[^0-9A-Za-z]+", "-", raw).strip("-").lower()
    return slug[:120] or "sanfoundry"

def fetch_html(url):
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36"),
        "Referer": "https://www.google.com/"
    }
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 403:
            raise requests.exceptions.HTTPError("403")
    except requests.exceptions.HTTPError:
        try:
            import cloudscraper
            scraper = cloudscraper.create_scraper(browser={'custom': headers['User-Agent']})
            r = scraper.get(url, timeout=20)
        except Exception as e:
            raise RuntimeError("Request blocked (403). Install cloudscraper. " + str(e))
    r.raise_for_status()
    return r.text

def extract_links_from_index(html, base_url):
    soup = BeautifulSoup(html, "lxml")
    links = []
    for table in soup.select("table.sf-2col-tbl"):
        for a in table.select("a[href]"):
            href = a["href"].strip()
            if href.lower().startswith("mailto:") or href.lower().startswith("javascript:"):
                continue
            full = urljoin(base_url, href)
            links.append(full)
    seen, deduped = set(), []
    for u in links:
        if u not in seen:
            seen.add(u)
            deduped.append(u)
    return deduped

def format_choices(text):
    s = (text or "").strip().replace("\r\n", "\n").replace("\r", "\n")
    parts = re.split(r"(?m)(^[a-z]\))", s)
    modified = {}
    for idx in range(1, len(parts), 2):
        key = parts[idx].strip()
        value = (parts[idx + 1] if idx + 1 < len(parts) else "").strip() + "\n"
        modified[key] = value
    return modified

def parse_questions(url):
    html = fetch_html(url)
    soup = BeautifulSoup(html, "lxml")
    title_tag = soup.select_one("h1.entry-title") or soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else url
    content = soup.select_one("div.entry-content") or soup.find("article") or soup.body
    children = [c for c in content.children if isinstance(c, Tag)]

    questions = []
    i = 0
    while i < len(children):
        child = children[i]
        if child.name == "p" and re.match(r"^\d+\.", child.get_text(strip=True)):
            qtext = child.get_text("\n", strip=True).replace("View Answer", "")
            lines = qtext.split("\n")
            cs_idx = None
            for idx, line in enumerate(lines):
                if re.match(r"^[a-z]\)", line.strip()):
                    cs_idx = idx
                    break
            if cs_idx is not None:
                questionText = "\n".join(lines[:cs_idx]).strip()
                choices = format_choices("\n".join(lines[cs_idx:]))
            else:
                questionText, choices = qtext, {}
            # find answer
            k = i + 1
            while k < len(children) and children[k].name != "div":
                k += 1
            answer, explanation = "", ""
            if k < len(children) and children[k].name == "div":
                ans_text = children[k].get_text("\n", strip=True)
                ans_text = ans_text.replace("Answer: ", "").replace("Explanation: ", "")
                parts = ans_text.split("\n", 1)
                answer = parts[0].strip()
                explanation = parts[1].strip() if len(parts) > 1 else ""
            questions.append({
                "questionText": questionText,
                "choices": choices,
                "answer": answer,
                "explanation": explanation
            })
            i = k
        i += 1
    return title, questions

def make_pdf_bytes(title, questions):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            rightMargin=15*mm, leftMargin=15*mm,
                            topMargin=15*mm, bottomMargin=15*mm)
    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    heading = ParagraphStyle("Heading", parent=styles["Heading1"], alignment=1)
    story = [Paragraph(title, heading), Spacer(1, 6)]
    for idx, q in enumerate(questions, 1):
        elems = [Paragraph(f"<b>{idx}. {q['questionText']}</b>", normal), Spacer(1, 4)]
        for key, val in q["choices"].items():
            is_correct = q["answer"] and key[0].lower() == q["answer"][0].lower()
            if is_correct:
                elems.append(Paragraph(f"<font color='blue'><b>{key} {val}</b></font>", normal))
            else:
                elems.append(Paragraph(f"{key} {val}", normal))
        if q["explanation"]:
            elems.append(Paragraph("<font color='red'><b>Explanation:</b></font>", normal))
            elems.append(Paragraph(q["explanation"], normal))
        story.append(KeepTogether(elems))
        story.append(Spacer(1, 8))
    doc.build(story)
    buf.seek(0)
    return buf.read()

# --- Streamlit UI ---
st.set_page_config(page_title="Sanfoundry Index → PDFs ZIP", layout="centered")
st.title("📘 Sanfoundry Index → PDFs (ZIP)")
st.write("Paste a Sanfoundry index page and download all sub-pages as PDFs inside one ZIP.")

url = st.text_input("Enter Sanfoundry Index URL", placeholder="https://www.sanfoundry.com/1000-transformers-questions-answers/")

if st.button("Generate ZIP"):
    if not url:
        st.error("Please enter a valid URL.")
    else:
        try:
            with st.spinner("Fetching index and generating PDFs…"):
                index_html = fetch_html(url)
                links = extract_links_from_index(index_html, url)
                if not links:
                    st.warning("No links found inside <table class=\"sf-2col-tbl\">.")
                else:
                    progress_text = st.empty()
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
                        for i, link in enumerate(links, 1):
                            slug = slug_from_url(link)
                            pdf_name = f"{slug}.pdf"
                            progress_text.info(f"Processing {i}/{len(links)}: {pdf_name}")
                            title, questions = parse_questions(link)
                            if not questions:
                                continue
                            pdf_bytes = make_pdf_bytes(title, questions)
                            zipf.writestr(pdf_name, pdf_bytes)
                    zip_buffer.seek(0)
                    progress_text.success("All PDFs processed!")
                    st.success(f"Generated ZIP with {len(links)} PDFs.")
                    st.download_button("⬇️ Download ZIP", data=zip_buffer.read(),
                                       file_name="sanfoundry_pdfs.zip", mime="application/zip")
        except Exception as e:
            st.error(f"Error: {e}")
