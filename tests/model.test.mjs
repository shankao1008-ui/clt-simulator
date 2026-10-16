import assert from 'node:assert/strict';
import {random,normal,cdf,invnorm,means,analyze,ks,quantile,DISTRIBUTIONS} from '../docs/model.mjs';
assert.equal(cdf(0).toFixed(6),'0.500000');
for(const p of [.0001,.001,.01,.1,.5,.9,.99,.999,.9999])assert.ok(Math.abs(cdf(invnorm(p))-p)<1e-6,`normal inverse ${p}`);
assert.ok(Math.abs(invnorm(.975)-1.9599639845)<1e-7);
assert.equal(ks([0,1],x=>x),.5);assert.equal(quantile([0,1,2,3],.5),1.5);
assert.deepEqual(means('chi',30,1000,42),means('chi',30,1000,42));
assert.notDeepEqual(means('chi',30,1000,42),means('chi',30,1000,43));
for(const key of Object.keys(DISTRIBUTIONS)){
 const n=30,N=10000,ys=means(key,n,N,42),a=analyze(key,n,ys),d=DISTRIBUTIONS[key];
 assert.ok(ys.every(Number.isFinite));assert.ok(a.ks>=0&&a.ks<=1);
 if(key==='cauchy'){assert.ok(Math.abs(a.med)<.1);assert.ok(Math.abs(a.q3-a.q1-2)<.2);assert.ok(a.ks<.03);assert.ok(a.normalKS>.05);}
 else {const se=d.sigma/Math.sqrt(n);assert.ok(Math.abs(a.m-d.mu)<6*se/Math.sqrt(N),`${key} mean`);assert.ok(Math.abs(a.sd/se-1)<(key==='t'?.2:.05),`${key} SE`);}
 console.log(key,'mean',a.m.toFixed(4),'SD',a.sd.toFixed(4),'KS',a.ks.toFixed(4));
}
const small=analyze('chi',5,means('chi',5,10000,42)),large=analyze('chi',1000,means('chi',1000,10000,42));assert.ok(large.ks<small.ks);assert.throws(()=>means('chi',0,1000,42));
console.log('All numerical checks passed.');
