import json, random, itertools
g = json.load(open(__import__('os').path.join(__import__('os').path.dirname(__file__), '..', 'app', 'src', 'main', 'assets', 'game.json'), encoding='utf-8'))
N = g['nodes']
def visible(n, flags, race, cls):
    out=[]
    for c in n['choices']:
        if c.get('races') and race not in c['races']: continue
        if c.get('classes') and cls not in c['classes']: continue
        if any(f not in flags for f in c.get('requires',[])): continue
        if any(f in flags for f in c.get('hideIf',[])): continue
        out.append(c)
    return out
problems=set(); endings={}
for race in [r['id'] for r in g['races']]:
    for cls in [c['id'] for c in g['classes']]:
        for _ in range(300):
            flags=set(); cur=g['start']; steps=0
            while True:
                n=N[cur]; flags |= set(n.get('set',[]))
                if n.get('end'): endings[cur]=endings.get(cur,0)+1; break
                v=visible(n,flags,race,cls)
                if not v: problems.add((cur,race,cls)); break
                c=random.choice(v); flags|=set(c.get('set',[]))
                cur = c['next'] if 'next' in c else random.choice([c['success'],c['failure']])
                steps+=1
                if steps>400: problems.add(('loop',cur)); break
print('problèmes:', problems or 'aucun')
print('fins atteintes:', endings)
