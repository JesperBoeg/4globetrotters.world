from __future__ import annotations

import re
from html import unescape
from pathlib import Path
import xml.etree.ElementTree as ET

SITE_ROOT = Path(r"c:\Users\agile\VSCode projects\4globetrotters\option-b-static\site")
EXPORT_XML = Path(r"C:\Users\agile\Downloads\4globetrotters.WordPress.2026-03-28.xml")

GALLERIES: dict[str, list[str]] = {
    '[envira-gallery id="3101"]': [
        '/wp-content/uploads/2022/05/P1190681.jpg',
        '/wp-content/uploads/2022/05/P1190682-1.jpg',
        '/wp-content/uploads/2022/05/P1190690.jpg',
        '/wp-content/uploads/2022/05/P1190695.jpg',
    ],
    '[envira-gallery id="3114"]': [
        '/wp-content/uploads/2022/05/P1190699.jpg',
        '/wp-content/uploads/2022/05/P1190713.jpg',
        '/wp-content/uploads/2022/05/P1190720.jpg',
        '/wp-content/uploads/2022/05/P1190727.jpg',
    ],
    '[envira-gallery id="3119"]': [
        '/wp-content/uploads/2022/05/P1190745.jpg',
        '/wp-content/uploads/2022/05/P1190749-1.jpg',
        '/wp-content/uploads/2022/05/P1190757.jpg',
        '/wp-content/uploads/2022/05/P1190767.jpg',
    ],
    '[envira-gallery id="3128"]': [
        '/wp-content/uploads/2022/05/P1190773.jpg',
        '/wp-content/uploads/2022/05/P1190777.jpg',
        '/wp-content/uploads/2022/05/P1190786.jpg',
        '/wp-content/uploads/2022/05/P1190790.jpg',
    ],
    '[envira-gallery id="3139"]': [
        '/wp-content/uploads/2022/05/P1190852.jpg',
        '/wp-content/uploads/2022/05/P1190863.jpg',
        '/wp-content/uploads/2022/05/P1190868.jpg',
        '/wp-content/uploads/2022/05/P1190886.jpg',
    ],
    '[envira-gallery id="3144"]': [
        '/wp-content/uploads/2022/05/P1190889.jpg',
        '/wp-content/uploads/2022/05/P1190893.jpg',
        '/wp-content/uploads/2022/05/P1190898.jpg',
        '/wp-content/uploads/2022/05/P1190903.jpg',
    ],
    '[envira-gallery id="3149"]': [
        '/wp-content/uploads/2022/05/P1190907.jpg',
        '/wp-content/uploads/2022/05/P1190916.jpg',
        '/wp-content/uploads/2022/05/P1190924.jpg',
        '/wp-content/uploads/2022/05/P1190927.jpg',
    ],
    '[envira-gallery id="3160"]': [
        '/wp-content/uploads/2022/05/P1190955.jpg',
        '/wp-content/uploads/2022/05/P1190958.jpg',
        '/wp-content/uploads/2022/05/P1190959.jpg',
        '/wp-content/uploads/2022/05/P1190970.jpg',
    ],
    '[envira-gallery id="3396"]': [
        '/wp-content/uploads/2022/06/P1210887.jpg',
        '/wp-content/uploads/2022/06/P1210842.jpg',
        '/wp-content/uploads/2022/06/P1210861.jpg',
        '/wp-content/uploads/2022/06/P1210838.jpg',
    ],
    '[envira-gallery id="3397"]': [
        '/wp-content/uploads/2022/06/P1210831.jpg',
        '/wp-content/uploads/2022/06/P1210832.jpg',
        '/wp-content/uploads/2022/06/P1210811.jpg',
        '/wp-content/uploads/2022/06/P1210825.jpg',
    ],
    '[envira-gallery id="3400"]': [
        '/wp-content/uploads/2022/06/GOPR1359.jpg',
    ],
    '[envira-gallery id="3450"]': [
        '/wp-content/uploads/2022/07/P1220004.jpg',
        '/wp-content/uploads/2022/07/P1220008.jpg',
        '/wp-content/uploads/2022/07/P1220014-1.jpg',
        '/wp-content/uploads/2022/07/P1220021.jpg',
    ],
    '[envira-gallery id="3451"]': [
        '/wp-content/uploads/2022/07/P1220029.jpg',
        '/wp-content/uploads/2022/07/P1220040.jpg',
        '/wp-content/uploads/2022/07/P1220048.jpg',
    ],
    '[envira-gallery id="3474"]': [
        '/wp-content/uploads/2022/07/P1220053.jpg',
        '/wp-content/uploads/2022/07/P1220056.jpg',
        '/wp-content/uploads/2022/07/P1220069-1.jpg',
        '/wp-content/uploads/2022/07/P1220072.jpg',
    ],
    '[envira-gallery id="3475"]': [
        '/wp-content/uploads/2022/07/P1220120.jpg',
        '/wp-content/uploads/2022/07/P1220122-1.jpg',
        '/wp-content/uploads/2022/07/P1220130.jpg',
        '/wp-content/uploads/2022/07/P1220132.jpg',
    ],
    '[envira-gallery id="3476"]': [
        '/wp-content/uploads/2022/07/P1220149.jpg',
        '/wp-content/uploads/2022/07/P1220162.jpg',
        '/wp-content/uploads/2022/07/P1220176.jpg',
        '/wp-content/uploads/2022/07/P1220208.jpg',
    ],
    '[envira-gallery id="3519"]': [
        '/wp-content/uploads/2022/07/P1220239.jpg',
        '/wp-content/uploads/2022/07/P1220216.jpg',
    ],
    '[envira-gallery id="3520"]': [
        '/wp-content/uploads/2022/07/P1220288.jpg',
        '/wp-content/uploads/2022/07/P1220264.jpg',
        '/wp-content/uploads/2022/07/P1220280.jpg',
    ],
    '[envira-gallery id="3521"]': [
        '/wp-content/uploads/2022/07/P1220349.jpg',
        '/wp-content/uploads/2022/07/P1220346.jpg',
        '/wp-content/uploads/2022/07/P1220339.jpg',
        '/wp-content/uploads/2022/07/P1220329.jpg',
    ],
    '[envira-gallery id="3522"]': [
        '/wp-content/uploads/2022/07/P1220362.jpg',
        '/wp-content/uploads/2022/07/P1220420.jpg',
        '/wp-content/uploads/2022/07/P1220442.jpg',
        '/wp-content/uploads/2022/07/P1220460.jpg',
    ],
    '[envira-gallery id="3523"]': [
        '/wp-content/uploads/2022/07/P1220533.jpg',
    ],
    '[envira-gallery id="3524"]': [
        '/wp-content/uploads/2022/07/P1220587.jpg',
        '/wp-content/uploads/2022/07/P1220608.jpg',
    ],
    '[envira-gallery id="3525"]': [
        '/wp-content/uploads/2022/07/P1220769.jpg',
        '/wp-content/uploads/2022/07/P1220781.jpg',
    ],
    '[envira-gallery id="3526"]': [
        '/wp-content/uploads/2022/07/P1220851.jpg',
        '/wp-content/uploads/2022/07/P1220898.jpg',
        '/wp-content/uploads/2022/07/P1220901.jpg',
    ],
    '[envira-gallery id="3527"]': [
        '/wp-content/uploads/2022/07/P1220942.jpg',
        '/wp-content/uploads/2022/07/P1220944.jpg',
    ],
    '[envira-gallery id="3701"]': [
        '/wp-content/uploads/2022/08/P1230795.jpg',
        '/wp-content/uploads/2022/08/P1230827.jpg',
        '/wp-content/uploads/2022/08/P1230839.jpg',
        '/wp-content/uploads/2022/08/P1230865.jpg',
    ],
    '[envira-gallery id="3714"]': [
        '/wp-content/uploads/2022/08/IMG_3977.jpeg',
        '/wp-content/uploads/2022/08/IMG_3971.jpeg',
        '/wp-content/uploads/2022/08/IMG_3989.jpeg',
    ],
    '[envira-gallery id="3733"]': [
        '/wp-content/uploads/2022/08/20220813_135525.jpg',
    ],
    '[envira-gallery id="3716"]': [
        '/wp-content/uploads/2022/08/IMG_4154.jpeg',
        '/wp-content/uploads/2022/08/IMG_4208.jpeg',
        '/wp-content/uploads/2022/08/IMG_4220.jpeg',
        '/wp-content/uploads/2022/08/IMG_4221.jpeg',
    ],
    '[envira-gallery id="3717"]': [
        '/wp-content/uploads/2022/08/IMG_4081-1.jpg',
        '/wp-content/uploads/2022/08/IMG_4084-1.jpeg',
    ],
    '[envira-gallery id="3718"]': [
        '/wp-content/uploads/2022/08/IMG_4106-1.jpeg',
        '/wp-content/uploads/2022/08/IMG_4442.jpeg',
    ],
    '[envira-gallery id="3719"]': [
        '/wp-content/uploads/2022/08/IMG_4511.jpeg',
        '/wp-content/uploads/2022/08/IMG_4531.jpeg',
        '/wp-content/uploads/2022/08/IMG_4566.jpeg',
        '/wp-content/uploads/2022/08/IMG_4534.jpeg',
    ],
    '[envira-gallery id="3720"]': [
        '/wp-content/uploads/2022/08/IMG_4828.jpeg',
        '/wp-content/uploads/2022/08/IMG_4922.jpeg',
        '/wp-content/uploads/2022/08/GOPR1533.jpg',
        '/wp-content/uploads/2022/08/GOPR1527.jpg',
    ],
    '[envira-gallery id="3721"]': [
        '/wp-content/uploads/2022/08/IMG_4812.jpeg',
        '/wp-content/uploads/2022/08/20220815_094442-1.jpg',
    ],
    '[envira-gallery id="3724"]': [
        '/wp-content/uploads/2022/08/IMG_4630.jpeg',
        '/wp-content/uploads/2022/08/IMG_4658.jpeg',
        '/wp-content/uploads/2022/08/IMG_4664.jpeg',
        '/wp-content/uploads/2022/08/IMG_4606.jpeg',
    ],
    '[envira-gallery id="3725"]': [
        '/wp-content/uploads/2022/08/P1230844.jpg',
        '/wp-content/uploads/2022/08/IMG_4705.jpeg',
        '/wp-content/uploads/2022/08/IMG_4772.jpeg',
    ],
    '[envira-gallery id="3738"]': [
        '/wp-content/uploads/2022/09/IMG_4992.jpeg',
        '/wp-content/uploads/2022/09/IMG_5003.jpeg',
    ],
    '[envira-gallery id="3743"]': [
        '/wp-content/uploads/2022/09/IMG_5019.jpeg',
        '/wp-content/uploads/2022/09/IMG_5042.jpeg',
    ],
    '[envira-gallery id="3744"]': [
        '/wp-content/uploads/2022/09/20220818_124557.jpg',
    ],
    '[envira-gallery id="3750"]': [
        '/wp-content/uploads/2022/09/IMG_5094.jpeg',
        '/wp-content/uploads/2022/09/IMG_5099.jpeg',
        '/wp-content/uploads/2022/09/IMG_5108.jpeg',
        '/wp-content/uploads/2022/09/IMG_5113.jpeg',
    ],
    '[envira-gallery id="3764"]': [
        '/wp-content/uploads/2022/09/GOPR1569.jpg',
        '/wp-content/uploads/2022/09/GOPR1568.jpg',
        '/wp-content/uploads/2022/09/IMG_5207.jpeg',
        '/wp-content/uploads/2022/09/IMG_5229.jpeg',
    ],
    '[envira-gallery id="3780"]': [
        '/wp-content/uploads/2022/09/IMG_5259.jpeg',
        '/wp-content/uploads/2022/09/IMG_5260.jpeg',
    ],
    '[envira-gallery id="3767"]': [
        '/wp-content/uploads/2022/09/20220823_205619.jpg',
        '/wp-content/uploads/2022/09/20220823_210040.jpg',
        '/wp-content/uploads/2022/09/IMG_5403.jpeg',
        '/wp-content/uploads/2022/09/IMG_5409.jpeg',
    ],
    '[envira-gallery id="3770"]': [
        '/wp-content/uploads/2022/09/20220824_152013.jpg',
        '/wp-content/uploads/2022/09/20220828_211213.jpg',
        '/wp-content/uploads/2022/09/20220828_211230.jpg',
    ],
    '[envira-gallery id="3783"]': [
        '/wp-content/uploads/2022/09/IMG_5394.jpeg',
        '/wp-content/uploads/2022/09/IMG_5393.jpeg',
    ],
    '[envira-gallery id="3789"]': [
        '/wp-content/uploads/2022/09/IMG_5429.jpeg',
        '/wp-content/uploads/2022/09/IMG_5433.jpeg',
        '/wp-content/uploads/2022/09/IMG_5438.jpeg',
        '/wp-content/uploads/2022/09/IMG_5442.jpeg',
    ],
    '[envira-gallery id="3796"]': [
        '/wp-content/uploads/2022/09/IMG_5457.jpeg',
        '/wp-content/uploads/2022/09/IMG_5468.jpeg',
        '/wp-content/uploads/2022/09/20220826_121356.jpg',
        '/wp-content/uploads/2022/09/20220826_122137.jpg',
    ],
    '[envira-gallery id="3799"]': [
        '/wp-content/uploads/2022/09/IMG_5505.jpeg',
        '/wp-content/uploads/2022/09/IMG_5523.jpeg',
    ],
    '[envira-gallery id="3806"]': [
        '/wp-content/uploads/2022/09/IMG_5538.jpeg',
        '/wp-content/uploads/2022/09/IMG_5546.jpeg',
        '/wp-content/uploads/2022/09/IMG_5549.jpeg',
        '/wp-content/uploads/2022/09/IMG_5559.jpeg',
    ],
    '[gallery ids="753,755,754"]': [
        '/wp-content/uploads/2015/12/P1060355.jpg',
        '/wp-content/uploads/2015/12/P1060363.jpg',
        '/wp-content/uploads/2015/12/P1060360.jpg',
    ],
    '[gallery columns="2" size="medium" ids="903,904"]': [
        '/wp-content/uploads/2015/12/P1060426-2.jpg',
        '/wp-content/uploads/2015/12/P1060441.jpg',
    ],
    '[gallery ids="906,782,905"]': [
        '/wp-content/uploads/2015/12/P1060465.jpg',
        '/wp-content/uploads/2015/12/P1060473.jpg',
        '/wp-content/uploads/2015/12/P1060475-2.jpg',
    ],
    '[gallery ids="788,787,790"]': [
        '/wp-content/uploads/2015/12/P1060537.jpg',
        '/wp-content/uploads/2015/12/P1060531.jpg',
        '/wp-content/uploads/2015/12/P1060549.jpg',
    ],
    '[gallery ids="781,780,792"]': [
        '/wp-content/uploads/2015/12/P1060461.jpg',
        '/wp-content/uploads/2015/12/P1060455.jpg',
        '/wp-content/uploads/2015/12/P1060559.jpg',
    ],
    '[gallery columns="2" size="medium" ids="804,805"]': [
        '/wp-content/uploads/2015/12/P1060156.jpg',
        '/wp-content/uploads/2015/12/P1060127.jpg',
    ],
    '[gallery columns="2" size="medium" ids="801,800"]': [
        '/wp-content/uploads/2015/12/P1060152.jpg',
        '/wp-content/uploads/2015/12/P1060139.jpg',
        '/wp-content/uploads/2015/12/P1060162.jpg',
        '/wp-content/uploads/2015/12/P1060167.jpg',
        '/wp-content/uploads/2015/12/P1060134.jpg',
        '/wp-content/uploads/2015/12/P1060164.jpg',
        '/wp-content/uploads/2015/12/P1060143.jpg',
        '/wp-content/uploads/2015/12/P1060144.jpg',
    ],
    '[gallery link="file" columns="2" size="large" ids="921,920"]': [
        '/wp-content/uploads/2015/12/P1050874.jpg',
        '/wp-content/uploads/2015/12/P1050872.jpg',
    ],
}

BLOCK_TAGS = (
    '<p', '<div', '<ul', '<ol', '<li', '<h1', '<h2', '<h3', '<h4', '<figure',
    '<blockquote', '<img', '<script', '<pre', '<table', '<iframe'
)


def _normalize_upload_url(url: str) -> str:
    url = url.strip()
    marker = '/wp-content/uploads/'
    idx = url.find(marker)
    if idx == -1:
        return url
    return url[idx:]


def _extract_envira_srcs(serialized: str) -> list[str]:
    srcs = re.findall(r's:3:"src";s:\d+:"(https?://[^"]+)"', serialized)
    normalized = [_normalize_upload_url(src) for src in srcs]
    out = []
    seen = set()
    for path in normalized:
        if path not in seen:
            seen.add(path)
            out.append(path)
    return out


def load_galleries_from_export(export_xml: Path) -> dict[str, list[str]]:
    if not export_xml.exists():
        return {}

    ns = {
        'wp': 'http://wordpress.org/export/1.2/',
        'content': 'http://purl.org/rss/1.0/modules/content/',
    }

    root = ET.parse(export_xml).getroot()
    channel = root.find('channel')
    if channel is None:
        return {}

    items = channel.findall('item')
    attachment_by_id: dict[str, str] = {}
    envira_by_id: dict[str, list[str]] = {}

    for item in items:
        post_id = (item.findtext('wp:post_id', default='', namespaces=ns) or '').strip()
        post_type = (item.findtext('wp:post_type', default='', namespaces=ns) or '').strip()
        if not post_id:
            continue

        if post_type == 'attachment':
            attachment_url = (item.findtext('wp:attachment_url', default='', namespaces=ns) or '').strip()
            if attachment_url:
                attachment_by_id[post_id] = _normalize_upload_url(attachment_url)
            continue

        if post_type == 'envira':
            for postmeta in item.findall('wp:postmeta', ns):
                key = (postmeta.findtext('wp:meta_key', default='', namespaces=ns) or '').strip()
                if key != '_eg_gallery_data':
                    continue
                value = postmeta.findtext('wp:meta_value', default='', namespaces=ns) or ''
                images = _extract_envira_srcs(value)
                if images:
                    envira_by_id[post_id] = images
                break

    mapped: dict[str, list[str]] = {}

    for gallery_id, images in envira_by_id.items():
        mapped[f'[envira-gallery id="{gallery_id}"]'] = images

    for item in items:
        content = item.findtext('content:encoded', default='', namespaces=ns) or ''
        if '[gallery ' not in content:
            continue

        for match in re.finditer(r'(\[gallery[^\]]*ids="([0-9,\s]+)"[^\]]*\])', content):
            shortcode = match.group(1)
            ids = [part.strip() for part in match.group(2).split(',') if part.strip()]
            images = [attachment_by_id[i] for i in ids if i in attachment_by_id]
            if images:
                mapped.setdefault(shortcode, images)

    return mapped


def merged_galleries() -> dict[str, list[str]]:
    merged = dict(GALLERIES)
    from_export = load_galleries_from_export(EXPORT_XML)
    for shortcode, images in from_export.items():
        merged[shortcode] = images
    return merged


ALL_GALLERIES = merged_galleries()


def alt_from_path(path: str) -> str:
    name = path.rsplit('/', 1)[-1]
    name = re.sub(r'\.[A-Za-z0-9]+$', '', name)
    return name.replace('-', ' ')


def render_gallery(images: list[str]) -> str:
    items = []
    for path in images:
        alt = alt_from_path(path)
        items.append(
            f"  <figure class='wp-block-image'><a href='{path}'><img src='{path}' alt='{alt}'></a></figure>"
        )
    return "\n<div class='wp-block-gallery restored-gallery'>\n" + "\n".join(items) + "\n</div>\n"


def replace_galleries(text: str) -> str:
    for shortcode, images in ALL_GALLERIES.items():
        text = text.replace(shortcode, render_gallery(images))
    text = re.sub(r'<strong>\s*&nbsp;\s*(<div class=\'wp-block-gallery restored-gallery\'>.*?</div>)\s*</strong>', r'\1', text, flags=re.S)
    return text


def cleanup_excerpt(text: str) -> str:
    return re.sub(
        r'\n\s*<p>[^<]{40,700}\.\.\.</p>\s*(<p class="meta">Category:.*?</p>)',
        r'\n  \1',
        text,
        flags=re.S,
    )


def normalize_headings(line: str) -> str:
    stripped = line.strip()
    match = re.fullmatch(r'<strong>(.*?)</strong>', stripped)
    if not match:
        return line
    inner = match.group(1).replace('&nbsp;', ' ').strip()
    if '<' in inner or not inner:
        return line
    return f'<h2>{inner}</h2>'


def wrap_loose_text(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    buffer: list[str] = []

    def flush() -> None:
        if not buffer:
            return
        content = ' '.join(part.strip() for part in buffer if part.strip())
        content = re.sub(r'\s+', ' ', content).strip()
        if content:
            out.append(f'<p>{content}</p>')
        buffer.clear()

    for raw_line in lines:
        line = raw_line.strip()
        if not line or line == '&nbsp;':
            flush()
            continue
        line = normalize_headings(line)
        if line.startswith('<img '):
            flush()
            out.append(f"<p class='content-image'>{line}</p>")
            continue
        if line.startswith(BLOCK_TAGS) or line.startswith('</'):
            flush()
            out.append(line)
            continue
        buffer.append(unescape(line))

    flush()
    return '\n'.join(out)


def fix_post(file_path: Path) -> bool:
    text = file_path.read_text(encoding='utf-8')
    original = text
    text = text.replace('[gallery columns=&quot;2&quot; size=&quot;medium&quot; ids=&quot;747,746&quot;]', '')

    main_match = re.search(r'(<main class="page-content">)(.*?)(</main>)', text, flags=re.S)
    if not main_match:
        return False

    before, main, after = main_match.groups()
    if '<p class="meta">Category:' not in main:
        return False

    main = replace_galleries(main)
    main = cleanup_excerpt(main)
    main = wrap_loose_text(main)
    main = re.sub(r'\n{3,}', '\n\n', main)

    text = text[:main_match.start()] + before + '\n' + main + '\n' + after + text[main_match.end():]
    if text != original:
        file_path.write_text(text, encoding='utf-8', newline='\n')
        return True
    return False


def main() -> None:
    changed = []
    unresolved = []
    for file_path in SITE_ROOT.glob('*/index.html'):
        source = file_path.read_text(encoding='utf-8')
        if '[envira-gallery' in source or '[gallery ' in source or '<p class="meta">Category:' in source:
            if fix_post(file_path):
                changed.append(file_path)
            remaining = re.findall(r'\[(?:envira-gallery|gallery)[^\]]+\]', file_path.read_text(encoding='utf-8'))
            if remaining:
                unresolved.append((file_path.name, remaining))

    print(f'Changed {len(changed)} files')
    for path in changed:
        print(path)
    if unresolved:
        print('\nUnresolved shortcodes:')
        for name, shortcodes in unresolved:
            print(name)
            for shortcode in shortcodes:
                print(f'  {shortcode}')


if __name__ == '__main__':
    main()
