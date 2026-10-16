// Browser-local numerical core. No network or third-party libraries required.
export const NS=[5,10,30,50,100,300,500,1000];
export const DISTRIBUTIONS={
 uniform:{label:'均勻分配',formula:'U(0, 1)',mu:.5,sigma:Math.sqrt(1/12),skew:0,kurt:-1.2,note:'對稱、有界。觀察平均數如何逐漸形成鐘形分配。'},
 t:{label:'t 分配',formula:'t(3)',mu:0,sigma:Math.sqrt(3),skew:null,kurt:null,note:'變異數有限，因此 CLT 成立；但重尾會讓模擬標準差與尾部較不穩定。'},
 chi:{label:'卡方分配',formula:'χ²(2)',mu:2,sigma:2,skew:2,kurt:6,note:'從右偏到接近對稱。增加 n，觀察平均數與常態曲線逐漸靠攏。'},
 beta:{label:'貝他分配',formula:'Beta(9, 2)',mu:9/11,sigma:Math.sqrt(18/1452),skew:-14*Math.sqrt(12)/(13*Math.sqrt(18)),kurt:6*(49*12-18*13)/(18*13*14),note:'左偏且有界。和卡方分配一起比較不同偏斜方向的影響。'},
 normal:{label:'常態分配',formula:'N(5, 2²)',mu:5,sigma:2,skew:0,kurt:0,note:'母體本身為常態：任何 n 下，平均數都精確服從常態分配。'},
 poisson:{label:'卜瓦松分配',formula:'Poisson(4)',mu:4,sigma:2,skew:.5,kurt:.25,note:'離散母體。小 n 時的階梯與間隙是分配本身的特性。'},
 cauchy:{label:'柯西分配',formula:'Cauchy(0, 1)',mu:null,sigma:null,skew:null,kurt:null,note:'CLT 條件不成立：沒有有限平均數與變異數，平均數仍為標準柯西。'}
};
export function random(seed=42){let a=seed>>>0;return()=>{a=(a+0x6D2B79F5)>>>0;let t=a;t=Math.imul(t^t>>>15,t|1);t^=t+Math.imul(t^t>>>7,t|61);return (((t^t>>>14)>>>0)+.5)/4294967296;};}
export function normal(r){return Math.sqrt(-2*Math.log(r()))*Math.cos(2*Math.PI*r());}
function gamma(k,r){const d=k-1/3,c=1/Math.sqrt(9*d);for(;;){const x=normal(r);let v=1+c*x;if(v<=0)continue;v=v*v*v;const u=r();if(u<1-.0331*x**4||Math.log(u)<.5*x*x+d*(1-v+Math.log(v)))return d*v;}}
export function sampler(key,r){switch(key){case'uniform':return()=>r();case't':return()=>normal(r)/Math.sqrt(2*gamma(1.5,r)/3);case'chi':return()=>-2*Math.log(r());case'beta':return()=>{const a=gamma(9,r);return a/(a+gamma(2,r));};case'normal':return()=>5+2*normal(r);case'poisson':return()=>{let p=1,k=0;do{k++;p*=r();}while(p>Math.exp(-4));return k-1;};case'cauchy':return()=>Math.tan(Math.PI*(r()-.5));default:throw Error('Unknown distribution');}}
export function means(key,n,N,seed){if(!DISTRIBUTIONS[key]||!Number.isInteger(n)||n<1||n>1000||!Number.isInteger(N)||N<100||N>10000)throw Error('Invalid simulation parameters');const draw=sampler(key,random(seed));const out=new Float64Array(N);for(let i=0;i<N;i++){let s=0;for(let j=0;j<n;j++)s+=draw();out[i]=s/n;}return out;}
export const pdf=z=>Math.exp(-z*z/2)/Math.sqrt(2*Math.PI);
export function cdf(z){const x=Math.abs(z),t=1/(1+.2316419*x);const p=1-pdf(x)*t*(.319381530+t*(-.356563782+t*(1.781477937+t*(-1.821255978+t*1.330274429))));return z>=0?p:1-p;}
// Peter J. Acklam's inverse-normal rational approximation.
export function invnorm(p){if(p<=0)return-Infinity;if(p>=1)return Infinity;const a=[-39.6968302866538,220.946098424521,-275.928510446969,138.357751867269,-30.6647980661472,2.50662827745924],b=[-54.4760987982241,161.585836858041,-155.698979859887,66.8013118877197,-13.2806815528857],c=[-.00778489400243029,-.322396458041136,-2.40075827716184,-2.54973253934373,4.37466414146497,2.93816398269878],d=[.00778469570904146,.32246712907004,2.445134137143,3.75440866190742];let q,r;if(p<.02425||p>1-.02425){q=Math.sqrt(-2*Math.log(p<.02425?p:1-p));r=(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5])/((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1);return p<.02425?r:-r;}q=p-.5;r=q*q;return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q/(((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1);}
export function quantile(a,p){const j=(a.length-1)*p,i=Math.floor(j);return a[i]+(a[Math.min(i+1,a.length-1)]-a[i])*(j-i);}
export function ks(a,F){let v=0;for(let i=0;i<a.length;i++){const f=F(a[i]);v=Math.max(v,(i+1)/a.length-f,f-i/a.length);}return v;}
export function analyze(key,n,values){const info=DISTRIBUTIONS[key],a=Array.from(values).sort((a,b)=>a-b),N=a.length;const m=a.reduce((s,x)=>s+x,0)/N;let m2=0,m3=0,m4=0;for(const v of a){const x=v-m;m2+=x*x;m3+=x**3;m4+=x**4;}const q1=quantile(a,.25),med=quantile(a,.5),q3=quantile(a,.75),cauchy=key==='cauchy',loc=cauchy?med:info.mu,scale=cauchy?(q3-q1)/1.3489795:info.sigma/Math.sqrt(n);return {key,n,N,a,m,sd:Math.sqrt(m2/(N-1)),skew:(m3/N)/(m2/N)**1.5,kurt:(m4/N)/(m2/N)**2-3,q1,med,q3,loc,scale,ks:ks(a,cauchy?x=>.5+Math.atan(x)/Math.PI:x=>cdf((x-loc)/scale)),normalKS:ks(a,x=>cdf((x-loc)/scale))};}
