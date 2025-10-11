/* Swarm AI Cooling – demo logic
   - KPIs (energy, loss, uptime, renewables)
   - SVG tooltips
   - Interaktivt diagram (lag-toggle, zoom/pan)
   - Swarm agents: anomalies + neighbor balancing
   - Optimizer heuristics
*/

const $  = (s, r=document)=>r.querySelector(s);
const $$ = (s, r=document)=>Array.from(r.querySelectorAll(s));
const rnd=(a,b)=>Math.random()*(b-a)+a;
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const fmt=(n,d=1)=>Number(n).toFixed(d);

/* ---------- SVG tooltips ---------- */
(() => {
  const tip = $('#svg-tip');
  let showTips = true;
  const btn = $('#toggle-tooltips');
  if(btn){ btn.addEventListener('click',()=>{ showTips=!showTips; tip.style.display='none'; }); }
  $$('.node').forEach(n=>{
    n.addEventListener('mousemove',e=>{
      if(!showTips) return;
      tip.textContent = n.getAttribute('data-tip')||'';
      tip.style.display='block';
      // hold tooltip innenfor diagrammet
      const wrap = n.closest('.diagram-wrap');
      const rect = wrap.getBoundingClientRect();
      const x = Math.min(e.clientX-rect.left+16, rect.width-260);
      const y = Math.min(e.clientY-rect.top +16, rect.height-40);
      tip.style.left = x+'px'; tip.style.top = y+'px';
    });
    n.addEventListener('mouseleave',()=> tip.style.display='none');
  });
})();

/* ---------- Diagram UI: lag + zoom/pan ---------- */
(() => {
  const gPower = document.getElementById('layer-power');
  const gCool  = document.getElementById('layer-cooling');
  const vp     = document.getElementById('viewport');
  const svg    = document.querySelector('.diagram-wrap svg');

  // Toggle lag
  const chkP = document.getElementById('toggle-power');
  const chkC = document.getElementById('toggle-cooling');
  if(chkP){ chkP.addEventListener('change', ()=> gPower.classList.toggle('hidden', !chkP.checked)); }
  if(chkC){ chkC.addEventListener('change', ()=> gCool.classList.toggle('hidden', !chkC.checked)); }

  // Zoom/pan (enkelt)
  let scale=1, minS=0.7, maxS=2.2;
  let panX=0, panY=0;
  let dragging=false, last={x:0,y:0};

  function apply(){ vp.setAttribute('transform', `translate(${panX},${panY}) scale(${scale})`); }

  const zi=$('#zoom-in'), zo=$('#zoom-out'), zr=$('#zoom-reset');
  if(zi) zi.addEventListener('click', ()=>{ scale=Math.min(maxS, scale*1.15); apply(); });
  if(zo) zo.addEventListener('click', ()=>{ scale=Math.max(minS, scale/1.15); apply(); });
  if(zr) zr.addEventListener('click', ()=>{ scale=1; panX=0; panY=0; apply(); });

  svg.addEventListener('mousedown', e=>{
    if(e.target.closest('.node')) return;
    dragging=true; last={x:e.clientX, y:e.clientY};
  });
  window.addEventListener('mousemove', e=>{
    if(!dragging) return;
    const dx=e.clientX-last.x, dy=e.clientY-last.y;
    last={x:e.clientX, y:e.clientY};
    panX+=dx; panY+=dy; apply();
  });
  window.addEventListener('mouseup', ()=> dragging=false);

  // Ctrl + scroll for zoom
  svg.addEventListener('wheel', e=>{
    if(!e.ctrlKey) return;
    e.preventDefault();
    const dir = e.deltaY>0 ? -1 : 1;
    const old = scale;
    scale = clamp(scale*(1+dir*0.12), minS, maxS);

    const pt = svg.createSVGPoint();
    pt.x=e.clientX; pt.y=e.clientY;
    const ctm = svg.getScreenCTM().inverse();
    const p = pt.matrixTransform(ctm);
    panX = p.x - (p.x - panX)*(scale/old);
    panY = p.y - (p.y - panY)*(scale/old);
    apply();
  }, {passive:false});
})();

/* ---------- KPIs ---------- */
const KPIS = [
  { key:'energyMW', title:'Nettlast', unit:'MW' },
  { key:'lossPct',  title:'Tap', unit:'%' },
  { key:'uptime',   title:'Oppetid', unit:'%' },
  { key:'renMix',   title:'Fornybar miks', unit:'%' },
];

const state = {
  running:false, tick:0, history:[],
  data: { energyMW:22, lossPct:3.6, uptime:99.96, renMix:32 }
};

function renderKPIs(){
  const wrap = $('#kpi-cards'); wrap.innerHTML='';
  KPIS.forEach(k=>{
    const prev = state.history.at(-1)?.[k.key] ?? state.data[k.key];
    const cur  = state.data[k.key];
    const delta = cur - prev;
    const el = document.createElement('div');
    el.className='kpi-card';
    el.innerHTML=`
      <div class="title">${k.title}</div>
      <div class="value">${fmt(cur)} ${k.unit}</div>
      <div class="delta ${delta>=0?'up':'down'}">${delta>=0?'▲':'▼'} ${fmt(Math.abs(delta))}${k.unit}</div>`;
    wrap.appendChild(el);
  });
}

/* ---------- Swarm agents ---------- */
const agentNames = ['Z1-A','Z1-B','Z2-A','Z2-B','Z3-A','Z3-B'];
const agents = agentNames.map(id=>({
  id, temp:rnd(25,28), load:rnd(0.35,0.65), power:rnd(2.5,4.5), neighbors:[], status:'OK'
}));
for(let i=0;i<agents.length;i++){
  if(i>0) agents[i].neighbors.push(agents[i-1].id);
  if(i<agents.length-1) agents[i].neighbors.push(agents[i+1].id);
}
const agentById = id => agents.find(a=>a.id===id);

function renderAgents(){
  const box = $('#agents'); box.innerHTML='';
  agents.forEach(a=>{
    const tempClass = a.temp>33?'hot':(a.temp<23?'cold':'ok');
    const wrap = document.createElement('div');
    wrap.className='agent';
    wrap.innerHTML = `
      <div class="agent-header">
        <h4>${a.id}</h4>
        <span class="badge-mini">${a.status}</span>
      </div>
      <div class="agent-metrics">
        <div class="metric"><div class="label">Temp</div><div class="value stat ${tempClass}">${fmt(a.temp)}°C</div></div>
        <div class="metric"><div class="label">Load</div><div class="value">${fmt(a.load*100,0)}%</div></div>
        <div class="metric"><div class="label">Power</div><div class="value">${fmt(a.power,2)} kW</div></div>
      </div>
      <div class="agent-neighbors">Naboer: ${a.neighbors.join(', ')}</div>
    `;
    box.appendChild(wrap);
  });
}

function swarmStep(){
  const ambient = 24 + Math.sin(state.tick/25)*1.0;
  const renBoost = (state.data.renMix-30)*0.002; // litt hjelp fra fornybar

  // lokale oppdateringer
  agents.forEach(a=>{
    const heat = a.load*8;
    const cooling = a.power*(1.8 + renBoost);
    a.temp = clamp(a.temp + 0.05*heat - 0.06*cooling + rnd(-0.15,0.2), ambient-1, 42);
    a.load = clamp(a.load + rnd(-0.02,0.02), 0.15, 0.95);
  });

  // anomali + nabobalansering
  const hot = agents.filter(a=>a.temp>33);
  hot.forEach(a=>{
    a.status='HOT';
    a.neighbors.forEach(nid=>{
      const n=agentById(nid);
      n.power = clamp(n.power+0.15, 1.5, 6.0);
      a.power = clamp(a.power-0.12, 1.0, 6.0);
    });
  });

  // sjelden failure
  if(Math.random()<0.02){
    const failing = agents[Math.floor(Math.random()*agents.length)];
    failing.status='FAIL';
    failing.power = clamp(failing.power*0.2, 0.2, 1.0);
    logEvent(`Agent ${failing.id} feilet – naboer øker innsats.`);
    failing.neighbors.forEach(nid=>{ const n=agentById(nid); n.power = clamp(n.power+0.5, 1.5, 6.0); });
  }

  // settling
  agents.forEach(a=>{
    if(a.temp<=33 && a.status!=='FAIL'){
      a.status='OK';
      a.power = clamp(a.power + rnd(-0.08,0.08), 1.5, 6.0);
    }
  });

  renderAgents();
}

/* ---------- Events ---------- */
function logEvent(msg){
  const ul = $('#event-log');
  const li = document.createElement('li');
  li.textContent = `[${new Date().toLocaleTimeString()}] ${msg}`;
  ul.prepend(li);
  while(ul.children.length>8) ul.removeChild(ul.lastChild);
}

/* ---------- Main loop ---------- */
let loopId=null;
function step(){
  state.tick++;
  const day = Math.sin(state.tick/20);
  state.data.energyMW = clamp(state.data.energyMW + rnd(-0.4,0.6) + day*0.25, 12, 40);
  state.data.renMix   = clamp(state.data.renMix   + rnd(-0.8,1.0), 15, 80);
  state.data.lossPct  = clamp(state.data.lossPct  + rnd(-0.08,0.10) - (state.data.renMix-30)*0.002, 2.0, 6.2);
  state.data.uptime   = clamp(99.90 + Math.abs(Math.sin(state.tick/200))*0.1, 99.7, 100);

  state.history.push({...state.data}); if(state.history.length>120) state.history.shift();

  renderKPIs();
  swarmStep();

  if(Math.random()<0.03) logEvent('Sverm balanse: last flyttet fra Z2-A → Z2-B.');
}
function start(){ if(loopId) return; loopId=setInterval(step,1000); state.running=true; renderKPIs(); renderAgents(); logEvent('Live-oppdatering startet.'); }
function stop(){ if(loopId){clearInterval(loopId); loopId=null; state.running=false; logEvent('Live-oppdatering stoppet.');} }
function reset(){ stop(); state.tick=0; state.history.length=0; state.data={energyMW:22,lossPct:3.6,uptime:99.96,renMix:32}; agents.forEach(a=>{a.temp=rnd(25,28);a.load=rnd(0.35,0.65);a.power=rnd(2.5,4.5);a.status='OK';}); renderKPIs(); renderAgents(); $('#ai-findings').innerHTML=''; logEvent('Nullstilt.'); }
$('#btn-start')?.addEventListener('click',start);
$('#btn-stop')?.addEventListener('click',stop);
$('#btn-reset')?.addEventListener('click',reset);

/* ---------- “AI” anomaly button ---------- */
function runAI(){
  const ul = $('#ai-findings'); ul.innerHTML='';
  let count=0;
  agents.forEach(a=>{
    if(a.temp>33){
      count++;
      const li=document.createElement('li');
      li.className='bad';
      li.textContent=`${a.id}: høy temp ${fmt(a.temp)}°C → naboer øker duty`;
      ul.appendChild(li);
    }
  });
  if(count===0){
    const li=document.createElement('li');
    li.className='good';
    li.textContent='Ingen kritiske avvik – svermen er stabil.';
    ul.appendChild(li);
  }
  logEvent('Anomali-sjekk kjørt.');

  // Blink cooling-laget ved avvik
  try{
    if(count>0){
      const cool = document.getElementById('layer-cooling');
      cool.classList.remove('pulse'); void cool.offsetWidth; cool.classList.add('pulse');
      setTimeout(()=> cool.classList.remove('pulse'), 800);
    }
  }catch{}
}
$('#btn-run-ai')?.addEventListener('click',runAI);

let autoAI=null;
$('#chk-auto-ai')?.addEventListener('change',e=>{
  if(e.target.checked){ autoAI=setInterval(runAI,10000); logEvent('Auto anomali-sjekk aktivert (10s).'); }
  else { clearInterval(autoAI); autoAI=null; logEvent('Auto anomali-sjekk deaktivert.'); }
});

/* ---------- Optimizer ---------- */
const inpRenew=$('#inp-renew'), inpBatt=$('#inp-batt'), inpGrowth=$('#inp-growth');
const outRenew=$('#out-renew'), outBatt=$('#out-batt'), outGrowth=$('#out-growth');
function bindRange(i,o,suf=''){ const u=()=>o.textContent=i.value+suf; i?.addEventListener('input',u); i&&u(); }
bindRange(inpRenew,outRenew,'%'); bindRange(inpBatt,outBatt); bindRange(inpGrowth,outGrowth,'%');

function computeKPIs(){
  const r=Number(inpRenew.value), b=Number(inpBatt.value), g=Number(inpGrowth.value);
  const baseLoss=1_200_000;
  const loss = baseLoss * (1 - r*0.003) * (1 - Math.min(b,15)*0.01) * (1 + g*0.004);
  const uptime = clamp(99.8 + Math.min(b,10)*0.05 - g*0.02 + r*0.01, 99.0, 99.999);
  const co2 = r*12 + b*4;
  const pue = clamp(1.45 - r*0.002 - Math.min(b,10)*0.01 + g*0.003, 1.15, 1.6);
  $('#kpi-loss').textContent=fmt(loss,0);
  $('#kpi-uptime').textContent=fmt(uptime,3);
  $('#kpi-co2').textContent=fmt(co2,1);
  $('#kpi-pue').textContent=fmt(pue,2);
}
$('#btn-optimize')?.addEventListener('click',computeKPIs);

/* Autostart demo */
start();
setTimeout(runAI,1500);
