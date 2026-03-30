from pathlib import Path
import re

site = Path(r'C:\Users\agile\VSCode projects\4globetrotters\option-b-static\site')
slugs = [
    'peru','ecuador-july-2024','galapagos-june-2024',
    'western-australia-julyaugust-2022','fiji-2022','french-polynesia',
    'san-francisco-2022','usa-denver-to-las-vegas-rockies-yellowstone-bryce-zion',
    'indonesia-bali-and-nearby-islands','australia-cairns','australia-northern-territory',
    'deep-south','cuba','mexico-yucatan','california-usa','hawaii',
    'australia','philippines','vietnam','thailand','cyprus',
]
for slug in slugs:
    f = site / slug / 'index.html'
    if not f.exists():
        print(f'{slug}: NOT FOUND')
        continue
    text = f.read_text(encoding='utf-8')
    imgs = re.findall(r"src='(/wp-content/uploads/[^']+)'", text)
    if not imgs:
        imgs = re.findall(r'src="(/wp-content/uploads/[^"]+)"', text)
    print(f'{slug}: {imgs[0] if imgs else "NO IMG"}')
