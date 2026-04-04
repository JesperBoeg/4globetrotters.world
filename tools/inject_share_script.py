from pathlib import Path

site = Path(r"C:\Users\agile\VSCode projects\4globetrotters\option-b-static\site")
skip = {
    "assets", "wp-content", "blog", "category", "countries-we-are-visiting",
    "about-us", "about-us-2", "itinerary", "todo-list", "privacy-policy"
}

for d in site.iterdir():
    if not d.is_dir() or d.name in skip:
        continue
    f = d / "index.html"
    if not f.exists():
        continue
    text = f.read_text(encoding="utf-8", errors="ignore")
    tag = '<script src="/assets/share-buttons.js"></script>'
    if tag in text:
        continue
    if "</body>" in text:
        text = text.replace("</body>", f"{tag}\n</body>")
        f.write_text(text, encoding="utf-8")
        print("updated", d.name)
