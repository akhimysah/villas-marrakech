"""Extrait les photos des villas d'un export Notion (Markdown & CSV), les redimensionne,
les classe par pièce (framework Vision d'Apple) et écrit data/photos.json.
Usage : python3 photos.py <export.zip>"""
import sys, os, re, io, json, zipfile, unicodedata, subprocess, urllib.parse
from PIL import Image, ImageOps, ImageFile
import tempfile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from parse import parse

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, '..', 'villas-marrakech')
OUT = os.path.join(SITE, 'photos', 'v')
CLASSIFY = sys.argv[2] if len(sys.argv) > 2 else None
MAXW, Q = 1280, 70

def norm(s):
    s = re.sub(r'\s+[0-9a-fA-F]{32}$', '', s.strip())
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().upper()
    return re.sub(r'[^A-Z0-9]+', ' ', s).strip()

def open_parts(path):
    """Renvoie la liste des zip à lire (gère les exports découpés en zip imbriqués)."""
    z = zipfile.ZipFile(path)
    inner = [n for n in z.namelist() if n.lower().endswith('.zip')]
    if not inner: return [z]
    parts = []
    for n in inner:
        parts.append(zipfile.ZipFile(io.BytesIO(z.read(n))))
    return parts

def main(zpath):
    parts = open_parts(zpath)
    files, real = {}, {}
    for z in parts:
        for n in z.namelist():
            fixed = n
            try: fixed = n.encode('cp437').decode('utf-8')
            except Exception: pass
            fixed = unicodedata.normalize('NFC', fixed)
            files[fixed] = z; real[fixed] = n
    mds = [n for n in files if n.lower().endswith('.md')]
    villas = parse(os.path.join(ROOT, 'villas_fr.txt'))
    by_key = {}
    for v in villas: by_key.setdefault(norm(v['name']).replace(' ROUTE D AMIZMIZ', ''), []).append(v)
    result = {}
    for md in mds:
        title = os.path.splitext(os.path.basename(md))[0]
        key = norm(title)
        cands = by_key.get(key)
        if not cands: continue
        text = files[md].read(real[md]).decode('utf-8', 'ignore')
        v = cands[0]
        if len(cands) > 1:  # deux « Villa Zaya » : on départage par la localisation
            v = next((c for c in cands if 'Amizmiz' in c['name']) if 'Amizmiz' in text else (c for c in cands if 'Amizmiz' not in c['name']), cands[0])
        base = os.path.dirname(md)
        refs = re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', text)
        imgs = []
        for r in refs:
            r = urllib.parse.unquote(r.split(' ')[0])
            p = unicodedata.normalize('NFC', os.path.normpath(os.path.join(base, r)).replace('\\', '/'))
            if p in files and re.search(r'\.(jpe?g|png|webp|heic|heif|avif)$', p, re.I): imgs.append(p)
        if not imgs: continue
        d = os.path.join(OUT, v['slug']); os.makedirs(d, exist_ok=True)
        out = []
        for i, p in enumerate(dict.fromkeys(imgs)):
            dst = os.path.join(d, f'{i+1:03d}.jpg')
            if not os.path.exists(dst):
                try:
                    data = files[p].read(real[p])
                    try:
                        im = Image.open(io.BytesIO(data)); im.load()
                    except Exception:  # HEIC : conversion par l'outil sips de macOS
                        with tempfile.TemporaryDirectory() as td:
                            src = os.path.join(td, 'in' + os.path.splitext(p)[1]); open(src, 'wb').write(data)
                            subprocess.run(['sips', '-s', 'format', 'jpeg', src, '--out', os.path.join(td, 'o.jpg')], capture_output=True)
                            im = Image.open(os.path.join(td, 'o.jpg')); im.load()
                    im = ImageOps.exif_transpose(im).convert('RGB')
                    if im.width > MAXW: im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
                    im.save(dst, 'JPEG', quality=Q, optimize=True, progressive=True)
                except Exception as e:
                    print('skip', p, e); continue
            out.append(f'photos/v/{v["slug"]}/{i+1:03d}.jpg')
        result[v['slug']] = out
        print(f'{v["name"]}: {len(out)} photos', flush=True)
    json.dump(result, open(os.path.join(ROOT, 'photos_raw.json'), 'w'), indent=0)
    print('villas avec photos:', len(result), '/', len(villas), '| photos:', sum(map(len, result.values())))

if __name__ == '__main__':
    main(sys.argv[1])
