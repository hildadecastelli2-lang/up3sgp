const {chromium}=require('playwright');const W=process.argv[2];
(async()=>{
const b=await chromium.launch();
const ctx=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:3,isMobile:true,hasTouch:true});
const p=await ctx.newPage();
await p.goto('file://'+W+'/app_demo.html');
await p.evaluate(()=>{localStorage.setItem('up3_dark','1')});await p.reload();await p.waitForTimeout(400);
const sh=async(n,full)=>{await p.waitForTimeout(250);await p.screenshot({path:W+'/shots/'+n+'.png',fullPage:!!full})};
// make main scroll part of page for full captures: capture main scroll height separately
await sh('home_dark');
const mainShot=async(n)=>{const h=await p.evaluate(()=>document.getElementById('mn').scrollHeight);await p.setViewportSize({width:390,height:Math.min(h+140,4000)});await sh(n);await p.setViewportSize({width:390,height:844});};
await mainShot('home_dark_tall');
await p.evaluate(()=>go('pen'));await sh('pen_dark');await mainShot('pen_dark_tall');
await p.fill('#qbox','MOLINA');await p.waitForTimeout(400);await sh('pen_search');
await p.evaluate(()=>{go('home');var i=P.findIndex(function(r){var d=dd(r[8]);return d!==null&&d<=0});sDet2('P',i)});await sh('ficha_cumplido');
await p.evaluate(()=>{S.det=null;var i=P.findIndex(function(r){var d=dd(r[8]);return d!==null&&d<=0});pLib(i,'P')});await sh('modal_lib');
await p.evaluate(()=>{doLib(S.lp.idx,'P')});await p.waitForTimeout(100);await sh('toast_lib');
await p.waitForTimeout(2600);
await p.evaluate(()=>{var i=P.findIndex(function(r){var d=dd(r[8]);return d!==null&&d>0&&d<=30});sDet2('P',i)});await sh('ficha_prx');
await p.evaluate(()=>{S.det=null;go('proc')});await sh('proc_dark');
await p.evaluate(()=>{pTrasl(2,'R')});await p.fill('#tr_dest','UP Nº1 PARANÁ').catch(()=>{});await sh('modal_trasl');
await p.evaluate(()=>{doTrasl(2,'R')});await sh('toast_trasl');await p.waitForTimeout(2600);
await p.evaluate(()=>{pElev(5)});await sh('modal_elev');await p.evaluate(()=>{doElevar(5)});await p.waitForTimeout(2600);
await p.evaluate(()=>{go('hist')});await sh('hist_dark');
await p.evaluate(()=>{S.md='menu';ren()});await sh('menu_dark');
await p.evaluate(()=>{S.md=null;go('home');togDark()});await sh('home_light');
await b.close();})();
