import xml.etree.ElementTree as ET
from datetime import datetime
tree = ET.parse(r'C:\Users\agile\Downloads\4globetrotters.WordPress.2026-03-28.xml')
root = tree.getroot()
WP = 'http://wordpress.org/export/1.2/'
channel = root.find('channel')
for item in channel.findall('item'):
    for cat_el in item.findall('category'):
        if cat_el.get('nicename') == 'phillipines':
            slug = item.findtext(f'{{{WP}}}post_name')
            pd = item.findtext('pubDate') or ''
            parts = pd.split(', ', 1)
            date_part = parts[1][:20] if len(parts) > 1 else ''
            try:
                dt = datetime.strptime(date_part, '%d %b %Y %H:%M:%S')
                print(slug[:50], '->', f"{dt.strftime('%B')} {dt.day}, {dt.year}")
            except Exception as e:
                print(slug[:50], 'FAIL', repr(pd), str(e))
            break
