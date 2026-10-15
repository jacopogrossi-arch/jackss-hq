const {chromium}=require('/opt/node22/lib/node_modules/playwright');
(async()=>{const [,,html,...ts]=process.argv;
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1920,height:1080}});
 await p.goto('file://'+process.cwd()+'/'+html);await p.evaluate(()=>document.fonts.ready);await p.waitForLoadState('networkidle');
 for(const t of ts){await p.evaluate(t=>render(+t),t);await p.screenshot({path:`still-${t}.png`});}
 await b.close();})();
