import json, math, sys
S=sys.argv[1]; m=json.load(open(f'{S}/geo/map.json')); t=open(f'{S}/tools/template.html').read()
f=lambda v: f'{v:.1f}'
W,H=560,m['H']; sd=m['pts']['sd']; nyc=m['pts']['nyc']
r={}
r['H']=f(H); r['H5']=f(H+10); r['IH']=f(m['iH'])
r['LAND']=m['land']; r['NY']=m['ny']; r['DR']=m['dr']
# route: quadratic from Santo Domingo area to NYC, stopping short for the arrow
C=(500,460)
def q(tt,a,c,b): return tuple((1-tt)**2*a[i]+2*tt*(1-tt)*c[i]+tt**2*b[i] for i in range(2))
end=q(.975,sd,C,nyc)
# re-express truncated quadratic: control for [0,s] is lerp(P0,C,s)
s=.975; c2=(sd[0]+(C[0]-sd[0])*s, sd[1]+(C[1]-sd[1])*s)
r['ROUTE']=f'M{f(sd[0])},{f(sd[1])} Q{f(c2[0])},{f(c2[1])} {f(end[0])},{f(end[1])}'
mid=q(.5,sd,C,nyc); r['NOTEX']=f(mid[0]+14); r['NOTEY']=f(mid[1]+4)
r['SDX'],r['SDY']=f(sd[0]),f(sd[1]); r['NYCX'],r['NYCY']=f(nyc[0]),f(nyc[1])
r['DRLX'],r['DRLY']='292','832'; r['DRKX'],r['DRKY']='292','848'
r['NYCLX'],r['NYCLY']=f(nyc[0]-150),f(nyc[1]+22); r['NYCKX'],r['NYCKY']=f(nyc[0]-150),f(nyc[1]+38)
INX,INY=352,6; r['INX'],r['INY']=str(INX),str(INY)
r['LEAD']=f'M{f(nyc[0]+5)},{f(nyc[1]-4)} L{INX},{INY+110}'
r['ILAND']=m['iland']; r['INSETNY']=m['iny']
inyc,ib=m['ipts']['nyc'],m['ipts']['bing']
r['INYCX'],r['INYCY']=f(inyc[0]),f(inyc[1]); r['IBX'],r['IBY']=f(ib[0]),f(ib[1]); r['IBLY']=f(ib[1]-10)
ic=(inyc[0]-38,inyc[1]-6); s=.88; ie=q(s,inyc,ic,ib); ic2=(inyc[0]+(ic[0]-inyc[0])*s, inyc[1]+(ic[1]-inyc[1])*s)
r['IROUTE']=f'M{f(inyc[0])},{f(inyc[1])} Q{f(ic2[0])},{f(ic2[1])} {f(ie[0])},{f(ie[1])}'
r['INOTEX'],r['INOTEY']=f(ib[0]+8),f(ib[1]+30)
SX,SY=490,700; r['STARX'],r['STARY']=str(SX),str(SY)
rh=[]
for k in range(16):
    a=math.radians(k*22.5); rh.append(f'<line x1="{SX}" y1="{SY}" x2="{f(SX+1400*math.sin(a))}" y2="{f(SY-1400*math.cos(a))}" />')
r['RHUMB']=''.join(rh)
st=[]
for k in range(8):
    a=math.radians(k*45); R=34 if k%2==0 else 20; ri=6
    tip=(R*math.sin(a),-R*math.cos(a))
    for sgn,cls in ((1,'star-a'),(-1,'star-b')):
        b=a+sgn*math.radians(22.5); side=(ri*math.sin(b),-ri*math.cos(b))
        if k==0: cls='star-n' if sgn==1 else 'star-b'
        st.append(f'<path class="{cls}" d="M0,0 L{f(tip[0])},{f(tip[1])} L{f(side[0])},{f(side[1])} Z" />')
st.append('<text x="0" y="-40" text-anchor="middle" style="font-family:var(--caps);font-size:13px">N</text>')
r['STAR']=''.join(st)
g=[]
for lon,x in m['grat']['lon'].items(): g.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{f(H)}" />')
for lat,y in m['grat']['lat'].items(): g.append(f'<line x1="0" y1="{y}" x2="560" y2="{y}" />')
r['GRAT']=''.join(g)
tk=[]
for lon,x in m['grat']['lon'].items(): tk.append(f'<text class="tick" x="{x}" y="-11" text-anchor="middle">{abs(int(lon))}° W</text>')
for lat,y in m['grat']['lat'].items(): tk.append(f'<text class="tick" x="-9" y="{f(float(y)+4)}" text-anchor="end">{lat}°</text>')
r['TICKS']=''.join(tk)
sb=m['scale500']; seg=sb/4; r['SBY']=f(H-38)
sc=[]
for i in range(4): sc.append(f'<rect class="{"f" if i%2==0 else "e"}" x="{f(i*seg)}" y="0" width="{f(seg)}" height="5" />')
sc.append('<text class="tick" x="0" y="19">0</text>')
sc.append(f'<text class="tick" x="{f(sb/2)}" y="19" text-anchor="middle">250</text>')
sc.append(f'<text class="tick" x="{f(sb)}" y="19" text-anchor="middle">500 mi</text>')
sc.append('<text class="tick" x="0" y="-6" style="font-style:italic">Scale at 30° N</text>')
r['SCALE']=''.join(sc)
# rose
ro=['<svg viewBox="-15 -15 30 30">']
for k in range(5):
    a=math.radians(36+72*k); p=lambda rr,aa:(rr*math.sin(aa),-rr*math.cos(aa))
    t1=p(14.5,a); l=p(6,a-.35); rr_=p(6,a+.35)
    ro.append(f'<path class="s" d="M{f(l[0])},{f(l[1])} L{f(t1[0])},{f(t1[1])} L{f(rr_[0])},{f(rr_[1])} Z" />')
for k in range(5):
    a=math.radians(72*k); ro.append(f'<circle class="p1" cx="{f(7.2*math.sin(a))}" cy="{f(-7.2*math.cos(a))}" r="5.8" />')
for k in range(5):
    a=math.radians(36+72*k); ro.append(f'<circle class="p2" cx="{f(3.6*math.sin(a))}" cy="{f(-3.6*math.cos(a))}" r="3.4" />')
ro.append('<circle class="c" r="2.4" /></svg>'); r['ROSE']=''.join(ro)
# chart
X=lambda tt: 80+(tt-2015.75)*70
NOW=2026+10/12
ch=[]
ch.append(f'<line class="nowline" x1="{f(X(NOW))}" y1="14" x2="{f(X(NOW))}" y2="214" />')
ch.append(f'<text class="now-t" x="{f(X(NOW))}" y="10" text-anchor="end">NOW · NOV 2026</text>')
g0=X(2015+11/12); ch.append(f'<path class="edu" d="M{f(g0)},24 l6,6 l-6,6 l-6,-6 Z" />')
ch.append(f'<text x="{f(g0+12)}" y="35">Binghamton University, B.S. <tspan class="dur" dx="6">Dec 2015</tspan></text>')
rows=[(2016,2021+9/12,80,'Avero · Product Owner &amp; Data Analyst','5 yr 9 mo',''),
      (2021+9/12,2023+4/12,130,'Jefferies · Data Analyst','1 yr 7 mo',''),
      (2023+4/12,NOW,180,'Jefferies · Product Strategist, Associate → VP','3 yr 6 mo','now')]
for a,b,y,lab,dur,cls in rows:
    ch.append(f'<rect class="bar {cls}" x="{f(X(a))}" y="{y-4}" width="{f(X(b)-X(a))}" height="8" />')
    full=f'{lab} <tspan class="dur" dx="6">{dur}</tspan>'
    if X(a)+330>X(NOW): ch.append(f'<text x="{f(X(b)-8)}" y="{y-12}" text-anchor="end">{full}</text>')
    else: ch.append(f'<text x="{f(X(a))}" y="{y-12}">{full}</text>')
ch.append(f'<line class="axis" x1="{f(X(2016))}" y1="226" x2="{f(X(NOW))}" y2="226" />')
for yr in range(2016,2027):
    ch.append(f'<line class="tk" x1="{f(X(yr))}" y1="226" x2="{f(X(yr))}" y2="231" /><text class="yr" x="{f(X(yr))}" y="246" text-anchor="middle">{yr}</text>')
r['CHART']=''.join(ch)
for k,v in r.items(): t=t.replace(f'__{k}__',v)
assert '__' not in t.replace('__agentproxy','') or print([l for l in t.split('\n') if '__' in l][:3])
open(sys.argv[2],'w').write(t)
print(len(t))
