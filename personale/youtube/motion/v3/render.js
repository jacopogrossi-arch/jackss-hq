const {chromium}=require('/opt/node22/lib/node_modules/playwright');
const fs=require('fs');
(async()=>{
 const [,,html,dur,fps,out]=process.argv;
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1920,height:1080}});
 await p.goto('file://'+process.cwd()+'/'+html);
 await p.evaluate(()=>document.fonts.ready);await p.waitForLoadState('networkidle');
 fs.mkdirSync(out,{recursive:true});
 const n=Math.round(dur*fps);
 for(let i=0;i<n;i++){await p.evaluate(t=>render(t),i/fps);await p.screenshot({path:`${out}/f${String(i).padStart(4,'0')}.png`});}
 await b.close();
})();
