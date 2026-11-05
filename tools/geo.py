import json, math, sys
G=sys.argv[1]
def load(p):
    t=json.load(open(p)); sc,tr=t['transform']['scale'],t['transform']['translate']
    arcs=[]
    for a in t['arcs']:
        x=y=0; pts=[]
        for dx,dy in a:
            x+=dx;y+=dy; pts.append((x*sc[0]+tr[0], y*sc[1]+tr[1]))
        arcs.append(pts)
    return t,arcs
def ring(arcs,idx):
    out=[]
    for i in idx:
        a=arcs[i] if i>=0 else arcs[~i][::-1]
        out.extend(a if not out else a[1:])
    return out
def polys(geom):
    if geom['type']=='Polygon': return [geom['arcs']]
    if geom['type']=='MultiPolygon': return geom['arcs']
    return []
def merc(lat): return math.log(math.tan(math.pi/4+math.radians(lat)/2))
class Proj:
    def __init__(s,lon0,lon1,lat0,lat1,W):
        s.lon0,s.lon1,s.lat0,s.lat1=lon0,lon1,lat0,lat1
        s.k=W/math.radians(lon1-lon0); s.W=W; s.H=s.k*(merc(lat1)-merc(lat0))
    def __call__(s,lon,lat):
        return (math.radians(lon-s.lon0)*s.k, (merc(s.lat1)-merc(lat))*s.k)
def path(rings,P,m=1.0,minseg=1.2,minarea=4):
    d=[]
    for r in rings:
        pts=[]
        for lon,lat in r:
            lon=min(max(lon,P.lon0-m),P.lon1+m); lat=min(max(lat,P.lat0-m),P.lat1+m)
            x,y=P(lon,lat)
            if not pts or math.hypot(x-pts[-1][0],y-pts[-1][1])>=minseg: pts.append((x,y))
        if len(pts)<3: continue
        a=abs(sum(pts[i][0]*pts[i-1][1]-pts[i-1][0]*pts[i][1] for i in range(len(pts))))/2
        if a<minarea: continue
        xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
        if max(xs)<0 or min(xs)>P.W or max(ys)<0 or min(ys)>P.H: continue
        d.append('M'+'L'.join(f'{x:.1f},{y:.1f}' for x,y in pts)+'Z')
    return ''.join(d)
out={}
# main map
P=Proj(-84,-62,16,44.5,560)
t,arcs=load(f'{G}/wa/package/land-50m.json')
rings=[ring(arcs,r) for g in t['objects']['land']['geometries'] for p in polys(g) for r in p]
out['W']=P.W; out['H']=round(P.H,1)
out['land']=path(rings,P)
t2,arcs2=load(f'{G}/wa/package/countries-50m.json')
dr=[g for g in t2['objects']['countries']['geometries'] if g.get('properties',{}).get('name')=='Dominican Rep.']
out['dr']=path([ring(arcs2,r) for g in dr for p in polys(g) for r in p],P,minseg=0.6,minarea=0.5)
t3,arcs3=load(f'{G}/us/package/states-10m.json')
ny=[g for g in t3['objects']['states']['geometries'] if g['properties']['name']=='New York']
nyr=[ring(arcs3,r) for g in ny for p in polys(g) for r in p]
out['ny']=path(nyr,P,minseg=0.8,minarea=0.5)
pts={'dr':(-70.16,18.74),'sd':(-69.93,18.48),'nyc':(-74.0,40.71),'bing':(-75.91,42.10)}
out['pts']={k:[round(v,1) for v in P(*c)] for k,c in pts.items()}
out['grat']={'lon':{l:round(P(l,30)[0],1) for l in range(-80,-61,5)},'lat':{l:round(P(-70,l)[1],1) for l in range(20,45,5)}}
# scale bar: 500 miles at lat 30
mi=500; deg=mi/(69.17*math.cos(math.radians(30))); out['scale500']=round(math.radians(deg)*P.k,1)
# inset NY state
Q=Proj(-80.0,-71.6,40.4,45.1,200)
out['iW']=Q.W; out['iH']=round(Q.H,1)
out['iny']=path(nyr,Q,minseg=0.7,minarea=0.3)
out['iland']=path(rings,Q,minseg=0.7,minarea=1)
out['ipts']={k:[round(v,1) for v in Q(*pts[k])] for k in ('nyc','bing')}
json.dump(out,open(sys.argv[2],'w'))
print({k:(len(v) if isinstance(v,str) else v) for k,v in out.items()})
