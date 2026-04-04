import sys
sys.path.insert(0, 'tools')
import restore_static_posts as r

g = r.load_galleries_from_export(r.EXPORT_XML)
print('Loaded from XML:', len(g))

test_ids = ['3598', '3642', '3258', '3171', '3364', '3426']
for gid in test_ids:
    key = f'[envira-gallery id="{gid}"]'
    imgs = g.get(key)
    if imgs:
        print(f'  {key} -> {len(imgs)} images, first: {imgs[0]}')
    else:
        print(f'  {key} -> MISSING')

print()
print('ALL_GALLERIES has', len(r.ALL_GALLERIES), 'total entries')
for gid in test_ids:
    key = f'[envira-gallery id="{gid}"]'
    imgs = r.ALL_GALLERIES.get(key)
    print(f'  ALL_GALLERIES {key} -> {"OK" if imgs else "MISSING"}')
