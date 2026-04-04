import re, pathlib

html = pathlib.Path(r"C:\Users\agile\VSCode projects\4globetrotters\option-b-static\site\countries-we-are-visiting\index.html").read_text(encoding="utf-8")

# Extract card text (everything between dest-card open/close)
card_blocks = re.findall(r'<div class="dest-card">(.*?)</div>\s*</div>', html, re.DOTALL)

# Extract filter terms from both data-filter attributes and JS marker definitions
btn_filters = re.findall(r'data-filter="([^"]+)"', html)
js_filters = re.findall(r"filter:\s*'([^']+)'", html)
all_filters = list(dict.fromkeys(btn_filters + js_filters))  # unique, ordered

print(f"Cards found: {len(card_blocks)}")
print(f"Filters: {len(all_filters)}")
print()

for f in all_filters:
    matched = []
    for i, card in enumerate(card_blocks):
        text = card.lower()
        if f.lower() in text:
            matched.append(i)
    status = "OK  " if matched else "MISS"
    print(f"{status} | {f:45s} | cards: {matched}")
