"""Classe chaque photo par pièce avec le framework Vision d'Apple, puis fixe l'ordre :
extérieur & piscine → salon → salle à manger → cuisine → autres espaces → chambres → salles de bain.
L'ordre Notion est conservé à l'intérieur de chaque catégorie (les photos d'une même chambre restent groupées).
Usage : python3 order.py <binaire classify>"""
import sys, os, json, subprocess
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, '..', 'villas-marrakech')
CLASSIFY = sys.argv[1]
raw = json.load(open(os.path.join(ROOT, 'photos_raw.json')))
cache_p = os.path.join(ROOT, 'labels_cache.json')
cache = json.load(open(cache_p)) if os.path.exists(cache_p) else {}

todo = [p for ps in raw.values() for p in ps if p not in cache]
for i in range(0, len(todo), 60):
    batch = todo[i:i+60]
    out = subprocess.run([CLASSIFY] + [os.path.join(SITE, p) for p in batch], capture_output=True, text=True).stdout
    for line in out.strip().split('\n'):
        if '\t' not in line: continue
        path, labels = line.split('\t', 1)
        rel = os.path.relpath(path, SITE)
        cache[rel] = dict((l.rsplit(':', 1)[0], float(l.rsplit(':', 1)[1])) for l in labels.split(',') if ':' in l)
    json.dump(cache, open(cache_p, 'w'))
    print(f'{min(i+60, len(todo))}/{len(todo)} classées', flush=True)

def category(L):
    g = lambda *k: max([L.get(x, 0) for x in k] + [0])
    s = {
        'bathroom': g('bathroom', 'bathroom_room', 'bath', 'shower', 'toilet_seat', 'bathroom_faucet'),
        'bedroom':  max(g('bedroom', 'bed'), 0.9 * g('bedding'), 0.75 * g('pillow')),
        'kitchen':  max(g('kitchen', 'kitchen_room', 'kitchen_countertop', 'kitchen_oven', 'kitchen_sink', 'refrigerator', 'stove', 'oven'), 0.8 * g('cookware')),
        'dining':   max(g('dining_room'), 0.7 * g('tableware')),
        'living':   max(g('living_room', 'sofa', 'fireplace'), 0.8 * g('armchair', 'television')),
        'wellness': g('jacuzzi', 'billiards', 'theater'),
    }
    ext = g('outdoor', 'pool', 'garden', 'patio', 'sunbathing')
    best = max(s, key=s.get)
    # une pièce clairement reconnue l'emporte sur le ciel vu par les baies vitrées
    firm = {'bathroom': s['bathroom'], 'kitchen': s['kitchen'], 'bedroom': g('bedroom', 'bed', 'bedding')}
    strong = max(firm, key=firm.get)
    if firm[strong] >= 0.35 and L.get('pool', 0) < 0.6 and not (strong == 'bedroom' and g('sofa', 'living_room') >= firm['bedroom']): return strong
    if s['bedroom'] > s['living'] and g('sofa', 'living_room') >= 0.3: s['bedroom'] = 0
    if ext >= 0.5 and ext >= s[best]: return 'exterior'
    if s[best] >= 0.15: return best
    return 'exterior' if ext >= 0.3 else 'other'

ORDER = ['exterior', 'living', 'dining', 'kitchen', 'wellness', 'other', 'bedroom', 'bathroom']
CAT_SITE = {'wellness': 'wellness'}
result, stats = {}, {}
for slug, ps in raw.items():
    items = [(ORDER.index(category(cache.get(p, {}))), i, p, category(cache.get(p, {}))) for i, p in enumerate(ps)]
    items.sort()
    result[slug] = [{'src': p, 'cat': c} for _, _, p, c in items]
    for _, _, _, c in items: stats[c] = stats.get(c, 0) + 1
json.dump(result, open(os.path.join(ROOT, 'photos.json'), 'w'), separators=(',', ':'))
print('répartition :', stats)
