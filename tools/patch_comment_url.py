from pathlib import Path

SITE = Path(r"C:\Users\agile\VSCode projects\4globetrotters\option-b-static\site")
INSERT_AFTER = '    site_id: "4globetrotters",\n'
INSERT_LINE = '    url: window.location.href.replace(/^https?:\\/\\/www\\./, "https://").split(/[?#]/)[0],\n'

updated = 0
for f in SITE.glob("*/index.html"):
    text = f.read_text(encoding="utf-8", errors="ignore")
    if "var remark_config = {" not in text:
        continue
    if INSERT_LINE in text:
        continue
    if INSERT_AFTER not in text:
        continue
    text = text.replace(INSERT_AFTER, INSERT_AFTER + INSERT_LINE, 1)
    f.write_text(text, encoding="utf-8")
    updated += 1

print(updated)
