const {chromium}=require('playwright');const {spawn}=require('child_process');const W=process.argv[2];const FPS=30,DUR=20;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+W+'/comp.html');await p.evaluate(()=>window.ready);
const ff=spawn('ffmpeg',['-loglevel','error','-y','-f','image2pipe','-framerate',String(FPS),'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','slow','-crf','16','-pix_fmt','yuv420p','-r',String(FPS),W+'/video_noaudio.mp4'],{stdio:['pipe','inherit','inherit']});
const n=FPS*DUR;const t0=Date.now();
for(let f=0;f<n;f++){await p.evaluate(t=>render(t),f/FPS);const buf=await p.screenshot({type:'jpeg',quality:96});
 if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r)); if(f%60===0)console.log('frame',f,((Date.now()-t0)/1000).toFixed(0)+'s')}
ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();console.log('done')})();
