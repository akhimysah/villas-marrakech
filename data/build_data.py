import json
from parse import parse
T=json.load(open('tr.json',encoding='utf-8'))
def L(fr): t=T[fr]; return {'fr':fr,'en':t['en'],'nl':t['nl'],'es':t['es']}
V=parse()
import os
PH=json.load(open('photos.json',encoding='utf-8')) if os.path.exists('photos.json') else {}
out=[]
for v in V:
    out.append({
      'slug':v['slug'],'name':v['name'],
      'bedrooms':v['bedrooms'],'capacity':v['capacity'],'bathrooms':v['bathrooms'],'surface':v['surface'],
      'location':[L(x) for x in v['location']],
      'features':[L(x) for x in v['features']],
      'blocks':[{'title':L(b['title']),'items':[L(x) for x in b['items']]} for b in v['blocks']],
      'included':[L(x) for x in v['included']],
      'onRequest':[L(x) for x in v['onRequest']],
      'info':[L(x) for x in v['info']],
      'photos':PH.get(v['slug'],[])
    })
js='''/* =====================================================================
   4. DONNÉES DES VILLAS
   Générées depuis data/villas_fr.txt (transcription de la base Notion « Propriétés »)
   et data/tr.json (traductions EN / NL / ES) par data/build_data.py.
   Structure identique pour chaque villa :
     1. name        Nom de la villa
     2. location    Localisation
     3. features    Description (caractéristiques) + blocks (blocs complémentaires)
     4. included / onRequest   Services & équipements
     5. info        Autres informations importantes (+ chambres, capacité, salles de bain, surface)
   photos : [{src, cat}] — photos Notion déjà triées par data/order.py (cat = pièce).
   ===================================================================== */
const DEMO = false;
const VILLAS = '''+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';\n'
open('../_data.js','w',encoding='utf-8').write(js)
print(len(out),'villas ->',len(js),'bytes')
