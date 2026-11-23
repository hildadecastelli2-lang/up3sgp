import numpy as np, wave, sys
SR=44100;D=20.0;N=int(SR*D);rng=np.random.default_rng(3)
L=np.zeros(N);Rr=np.zeros(N)
def add(sig,t,g=1.0,pan=0.0):
    i=int(t*SR);n=min(len(sig),N-i)
    if n<=0:return
    L[i:i+n]+=sig[:n]*g*np.sqrt(.5*(1-pan));Rr[i:i+n]+=sig[:n]*g*np.sqrt(.5*(1+pan))
def tt(d):return np.arange(int(d*SR))/SR
def lp(x,c):  # one-pole lowpass, c in Hz (scalar or array)
    c=np.broadcast_to(np.asarray(c,float),x.shape);a=1-np.exp(-2*np.pi*c/SR);y=np.zeros_like(x);s=0.0
    for i in range(len(x)):s+=a[i]*(x[i]-s);y[i]=s
    return y
def hp(x,c):return x-lp(x,c)
noise=lambda d:rng.standard_normal(int(d*SR))
def kick(g=1):
    t=tt(.45);f=45+110*np.exp(-t*28);ph=2*np.pi*np.cumsum(f)/SR
    return (np.sin(ph)*np.exp(-t*7)+.3*np.exp(-t*300)*noise(.45))*g
def hat(d=.06):t=tt(d);return hp(noise(d),7000)*np.exp(-t*70)
def clap():
    t=tt(.3);n=hp(noise(.3),1200);env=np.exp(-t*18)
    for o in(.0,.012,.024):env+=np.where((t>=o)&(t<o+.01),np.exp(-(t-o)*200),0)
    return n*env*.6+np.sin(2*np.pi*190*t)*np.exp(-t*30)*.3
def saw(f,t,det=0):return 2*((t*f*(1+det))%1)-1
def note(m):return 440*2**((m-69)/12)
def pad(ms,d,cut=1800):
    t=tt(d);s=sum(saw(note(m),t,dt) for m in ms for dt in(-.004,0,.005))
    env=np.minimum(1,t/.25)*np.minimum(1,(d-t)/.3);return lp(s,cut)*env*.032
def bass(m,d):
    t=tt(d);s=saw(note(m),t)+.6*np.sin(2*np.pi*note(m-12)*t);env=np.exp(-t*3)*np.minimum(1,(d-t)/.02)
    return lp(s,500+1500*np.exp(-t*12))*env*.35
def riser(d):
    t=tt(d);f=200+4000*(t/d)**2;x=lp(noise(d),f)
    tone=np.sin(2*np.pi*np.cumsum(300+900*(t/d)**2)/SR)*.15
    return (x*.7+tone)*(t/d)**2
def whoosh(d=.45,up=True):
    t=tt(d);e=np.sin(np.pi*t/d)**2;f=(500+5000*(t/d)) if up else (5500-5000*(t/d));return lp(noise(d),f)*e*.9
def impact(g=1):
    t=tt(2.5);boom=np.sin(2*np.pi*np.cumsum(30+70*np.exp(-t*6))/SR)*np.exp(-t*1.8)
    nz=lp(noise(2.5),3000*np.exp(-t*3)+200)*np.exp(-t*4)
    return (boom*1.1+nz*.5)*g
def blip(f=1800,d=.12):t=tt(d);return np.sin(2*np.pi*f*t)*np.exp(-t*35)*.5
def bell(m,d=2.0):
    t=tt(d);return sum(a*np.sin(2*np.pi*note(m)*r*t)*np.exp(-t*k) for a,r,k in((1,1,2.2),(.5,2.0,3),(.3,3.01,5),(.2,4.2,7)))*.25
def tick():t=tt(.03);return hp(noise(.03),3000)*np.exp(-t*200)*.5+np.sin(2*np.pi*2400*t)*np.exp(-t*150)*.2
B=.5 # beat
CH=[[57,60,64],[53,57,60],[48,52,55,60],[55,59,62]]; BS=[45,41,48,43]
# --- HOOK 0-3
add(impact(.9),0.0)
add(pad([45,52,57],3.0,700),0.0,1.4)
for i,tc in enumerate(np.linspace(.05,1.15,22)):add(tick(),tc,.7,(-1)**i*.3)
add(whoosh(.35),1.25,.6);add(impact(.35),1.42)
add(riser(1.4),1.55,.55)
for tc in(1.5,2.0,2.5,2.75):add(kick(.8),tc)
add(blip(900,.2),2.15,.5);add(blip(860,.2),2.3,.4)
add(whoosh(.5),2.55,.8)
# --- MAIN 3-13
for b in range(6,26):
    tc=b*B;add(kick(1),tc)
    add(hat(),tc+B/2,.35,.3)
    if tc>=7:
        add(hat(.03),tc+B/4,.18,-.3);add(hat(.03),tc+3*B/4,.18,-.3)
        if b%2==1:add(clap(),tc,.8)
for bar in range(5):
    t0=3+bar*2;k=bar%4
    add(pad(CH[k],2.0,1400 if t0<7 else 2400),t0,1.1)
    for s in range(8):add(bass(BS[k] if s%2==0 else BS[k]+12,.24),t0+s*.25,.9 if s%2==0 else .5)
add(impact(.7),3.0)
for tc,pn in((4.6,-.5),(5.05,.5),(5.5,-.5)):add(blip(1400,.15),tc,.6,pn);add(blip(2100,.1),tc+.05,.3,pn)
for tc in(6.8,8.32,9.82,11.32):add(whoosh(.35),tc,.9,.6 if int(tc)%2 else -.6)
add(impact(.4),7.0)
for tc in(9.05,10.55,12.05):add(blip(1700,.12),tc,.6)
add(bell(84,1.2),12.25,.7);add(bell(91,1.2),12.33,.45)
add(riser(1.3),11.7,.8)
# --- WOW 13-17
add(impact(1.2),13.0)
add(pad([45,52,57,64],3.3,2200),13.0,1.5)
add(pad([53,57,60,65],0.1,2200),16.2,0)
for tc,m in((13.25,69),(14.15,72),(15.05,76)):
    add(kick(.9),tc);add(bell(m,1.2),tc,.6);add(clap(),tc,.5)
for tc in np.arange(13.0,16.2,.25):add(hat(.03),tc,.12)
add(riser(1.2),15.8,.9);add(whoosh(.8),16.2,1.0)
# --- END 17-20
add(impact(1.2),17.0)
add(pad([45,52,57,60,64],3.0,1600),17.0,1.6)
add(bell(81,2.8),17.05,.8);add(bell(88,2.8),17.15,.5);add(bell(76,2.8),17.4,.4)
for tc in(17.4,17.5,17.6):add(blip(2600,.08),tc,.2)
add(blip(1300,.18),18.3,.7);add(bell(93,1.5),18.95,.35,.4)
for tc in(18.7,19.2,19.7):add(kick(.55),tc)
# master: simple reverb-ish (feedback delays), fade, limiter
def verb(x):
    y=x.copy()
    for dly,g in((.031,.35),(.047,.3),(.071,.25),(.113,.2),(.173,.14)):
        n=int(dly*SR);y[n:]+=x[:-n]*g
    return y
L=L+verb(L)*.25;Rr=Rr+verb(Rr)*.25
fade=np.ones(N);fo=int(.4*SR);fade[-fo:]=np.linspace(1,0,fo)**1.5
st=np.stack([L,Rr],1)*fade[:,None];st=np.tanh(st*0.9)/np.tanh(0.9)
st=st/np.max(np.abs(st))*0.93
with wave.open(sys.argv[1],'wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((st*32767).astype('<i2').tobytes())
print('ok',np.sqrt(np.mean(st**2)))
