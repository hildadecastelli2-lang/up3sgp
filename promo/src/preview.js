const {chromium}=require('playwright');const W=process.argv[2];const ts=process.argv[3].split(',').map(Number);
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+W+'/comp.html');await p.evaluate(()=>window.ready);
for(const t of ts){await p.evaluate(t=>render(t),t);await p.screenshot({path:W+'/pv/'+t.toFixed(2)+'.jpg',type:'jpeg',quality:80})}
await b.close()})();
