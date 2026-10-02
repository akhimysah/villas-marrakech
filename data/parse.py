import re, json, unicodedata
def slugify(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+','-',s).strip('-')
def items(s): return [x.strip() for x in s.split('•') if x.strip()]
def parse(path='villas_fr.txt'):
    villas=[]; cur=None
    for ln in open(path,encoding='utf-8'):
        ln=ln.rstrip('\n')
        if not ln.strip() or ln.startswith('#'): continue
        if ln.startswith('== '):
            name,b,c,ba,su=[x.strip() for x in ln[3:].split('|')]
            num=lambda x: None if x=='-' else int(x)
            cur={'name':name,'slug':slugify(name),'bedrooms':num(b),'capacity':num(c),'bathrooms':num(ba),'surface':num(su),
                 'location':[],'features':[],'blocks':[],'included':[],'onRequest':[],'info':[]}
            villas.append(cur); continue
        tag,_,rest=ln.partition(' ')
        if tag=='L': cur['location']+=items(rest)
        elif tag=='D': cur['features']+=items(rest)
        elif tag=='S+': cur['included']+=items(rest)
        elif tag=='S?': cur['onRequest']+=items(rest)
        elif tag=='I': cur['info']+=items(rest)
        elif tag=='X':
            t,_,its=rest.partition('|'); cur['blocks'].append({'title':t.strip(),'items':items(its)})
        else: raise ValueError(ln)
    # unique slugs
    seen={}
    for v in villas:
        s=v['slug']
        if s in seen: seen[s]+=1; v['slug']=f"{s}-{seen[s]}"
        else: seen[s]=1
    return villas
if __name__=='__main__':
    V=parse()
    U=[]
    for v in V:
        for k in ('location','features','included','onRequest','info'): U+=v[k]
        for b in v['blocks']: U+=[b['title']]+b['items']
    uniq=sorted(set(U))
    open('unique_items.txt','w',encoding='utf-8').write('\n'.join(uniq))
    print(len(V),'villas',len(U),'items',len(uniq),'unique',sum(len(x) for x in uniq),'chars')
    print('slugs dup check', len({v['slug'] for v in V})==len(V))
