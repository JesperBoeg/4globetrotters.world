import os, re

site = os.path.join(os.path.dirname(__file__), '..', 'option-b-static', 'site')

mojibake = [
    ('Ã©', 'é'),
    ('Ã¥', 'å'),
    ('Ã¦', 'æ'),
    ('Ã¸', 'ø'),
    ('Ã˜', 'Ø'),
    ('Ã¡', 'á'),
    ('Ã±', 'ñ'),
    ('Ãª', 'ê'),
    ('Ã¨', 'è'),
]

figcap_pattern = re.compile(r'<figcaption class="wp-element-caption">DCIM[^<]*</figcaption>')

fixed = []
for root, dirs, files in os.walk(site):
    for fn in files:
        if not fn.endswith('.html'):
            continue
        path = os.path.join(root, fn)
        with open(path, encoding='utf-8') as f:
            text = f.read()
        original = text
        for bad, good in mojibake:
            text = text.replace(bad, good)
        text = figcap_pattern.sub('', text)
        if text != original:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(text)
            fixed.append(path)

print(f'Fixed {len(fixed)} files:')
for p in fixed:
    print(' ', p)
