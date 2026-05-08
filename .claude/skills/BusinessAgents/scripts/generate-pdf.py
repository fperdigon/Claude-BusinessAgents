#!/usr/bin/env python3
"""Generate a PDF from a carousel HTML file. All session values passed as CLI args."""
import argparse, os, re


def main():
    parser = argparse.ArgumentParser(description="Generate PDF from carousel HTML")
    parser.add_argument("--width",  type=int, required=True, help="Card width in px")
    parser.add_argument("--height", type=int, required=True, help="Card height in px")
    parser.add_argument("--slides", type=int, required=True, help="Number of slides")
    parser.add_argument("--html",   required=True, help="Path to carousel HTML file")
    parser.add_argument("--pdf",    required=True, help="Path for output PDF file")
    args = parser.parse_args()

    CARD_W     = args.width
    CARD_H     = args.height
    NUM_SLIDES = args.slides
    html_path  = os.path.abspath(args.html)
    pdf_path   = os.path.abspath(args.pdf)
    html_dir   = os.path.dirname(html_path)
    pv_path    = os.path.join(html_dir, "carousel-print-view.html")

    # Step 1 — build a stripped print-view HTML (no nav / instructions / caption-box / JS)
    with open(html_path, encoding="utf-8") as f:
        src = f.read()

    for tag in ("nav", "instructions", "caption-box", "doc-title-row"):
        src = re.sub(
            rf'<div[^>]*class="[^"]*{tag}[^"]*".*?</div>\s*',
            "", src, flags=re.DOTALL | re.IGNORECASE,
        )
    src = re.sub(r"<script[\s\S]*?</script>", "", src, flags=re.IGNORECASE)
    src = src.replace(
        "body {",
        "body { flex-direction: column !important; align-items: center !important; gap: 0 !important; padding: 0 !important; background: #080810;",
        1,
    )
    # Replace display:none in the .card rule with display:flex — no !important so JS inline
    # styles can override it per-slide during screenshotting
    src = re.sub(
        r'(\.card\s*\{[^}]*?)display:\s*none',
        r'\1display: flex',
        src,
    )
    with open(pv_path, "w", encoding="utf-8") as f:
        f.write(src)

    # Step 2 — screenshot each slide individually with Playwright
    from playwright.sync_api import sync_playwright

    slide_paths = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": CARD_W, "height": CARD_H})
        page.goto(f"file://{pv_path}")
        page.wait_for_load_state("networkidle", timeout=8000)

        for i in range(NUM_SLIDES):
            page.evaluate(f"""
                document.querySelectorAll('.card').forEach((c, idx) => {{
                    c.style.display = idx === {i} ? 'flex' : 'none';
                }});
            """)
            slide_file = os.path.join(html_dir, f"_slide_{i+1:02d}.png")
            page.screenshot(
                path=slide_file,
                clip={"x": 0, "y": 0, "width": CARD_W, "height": CARD_H},
            )
            slide_paths.append(slide_file)

        browser.close()

    # Step 3 — assemble PDF with ReportLab
    from reportlab.pdfgen import canvas as rl_canvas

    c = rl_canvas.Canvas(pdf_path, pagesize=(CARD_W, CARD_H))
    for sp in slide_paths:
        c.drawImage(sp, 0, 0, CARD_W, CARD_H)
        c.showPage()
    c.save()

    # Step 4 — clean up temp files
    os.remove(pv_path)
    for sp in slide_paths:
        os.remove(sp)

    print(f"PDF saved: {pdf_path}")


if __name__ == "__main__":
    main()
