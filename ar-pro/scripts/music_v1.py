import numpy as np, wave
SR=44100; DUR=36; N=SR*DUR; t=np.arange(N)/SR
out=np.zeros((N,2))
BPM=120; beat=60/BPM
def env(x,a,d): return np.where(x<0,0,np.minimum(x/a,1)*np.exp(-np.maximum(x-a,0)/d))
rng=np.random.default_rng(1)
def add(sig,start,gain=1.0,pan=0.0):
    i=int(start*SR); n=min(len(sig),N-i)
    if n<=0: return
    out[i:i+n,0]+=sig[:n]*gain*(1-pan)/1; out[i:i+n,1]+=sig[:n]*gain*(1+pan)/1
# kick
kl=int(.4*SR); kt=np.arange(kl)/SR
kick=np.sin(2*np.pi*(45*kt+ (120/18)*(1-np.exp(-kt*18))))*np.exp(-kt*7)
# hat
hl=int(.06*SR); hat=rng.standard_normal(hl)*np.exp(-np.arange(hl)/SR*80); hat=np.diff(np.concatenate([[0],hat]))
# chords Am F C G (each 2 bars = 4s), roots in Hz
prog=[(220.0,[0,3,7]),(174.61,[0,4,7]),(261.63,[0,4,7]),(196.0,[0,4,7])]
pad=np.zeros(N); bass=np.zeros(N)
for k in range(10):
    s=k*4.0; root,iv=prog[k%4]
    i0=int(s*SR); i1=min(N,int((s+4)*SR)); tt=t[i0:i1]-s
    e=np.minimum(tt/0.6,1)*np.minimum((4-tt)/0.6,1)
    for st in iv:
        f=root*2**(st/12)
        for det in (-0.004,0.004):
            ph=2*np.pi*f*(1+det)*tt
            pad[i0:i1]+=e*(np.sin(ph)+0.3*np.sin(2*ph))*0.06
    # bass pulse 8th notes
    for j in range(16):
        bs=j*beat/2; m=(tt>=bs)&(tt<bs+0.22)
        x=tt[m]-bs; bass[i0:i1][m]+=np.sign(np.sin(2*np.pi*root/2*tt[m]))*0.5*np.exp(-x*12)*0.25
# lowpass bass crudely
bass=np.convolve(bass,np.ones(30)/30,mode='same')
out[:,0]+=pad+bass; out[:,1]+=pad+bass
# drums: start at 1.0s, stop at 34
b=1.0
while b<34.5:
    add(kick,b,0.9)
    add(hat,b+beat/2,0.25,0.3)
    b+=beat
# whoosh at boundaries
for bd in [4,8.5,13,17.5,22,26.5,31]:
    L=int(0.7*SR); x=np.arange(L)/SR
    nz=rng.standard_normal(L); 
    # rising sweep: progressively less smoothing
    sig=np.zeros(L); w=np.linspace(40,3,L).astype(int)
    cs=np.cumsum(np.concatenate([[0],nz]))
    idx=np.arange(L); lo=np.maximum(idx-w,0); sig=(cs[idx+1]-cs[lo])/(idx+1-lo)
    sig*=np.sin(np.pi*x/0.7)**2
    add(sig,bd-0.45,0.9)
    # impact
    il=int(1.2*SR); it=np.arange(il)/SR
    imp=np.sin(2*np.pi*55*it)*np.exp(-it*4)+rng.standard_normal(il)*np.exp(-it*25)*0.3
    add(imp,bd,0.5)
# intro riser & title hit
add(np.sin(2*np.pi*(80*t[:SR]+200*t[:SR]**2))*np.linspace(0,1,SR)*0.2,0.0)
for s,g in [(0.6,0.7),(31.8,0.9)]:
    il=int(2*SR); it=np.arange(il)/SR
    add((np.sin(2*np.pi*40*it)+0.5*np.sin(2*np.pi*80*it))*np.exp(-it*2.5),s,g)
# master fade
fade=np.ones(N); fade[int(34.5*SR):]=np.linspace(1,0,N-int(34.5*SR)); fade[:int(.3*SR)]=np.linspace(0,1,int(.3*SR))
out*=fade[:,None]
out/=np.max(np.abs(out))*1.12
with wave.open('music.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype('<i2').tobytes())
print('ok')
