/* 
  SmartGrid Edge – enkel demo-logikk
  - Simulerer live målinger og KPI-er
  - "AI"-feildeteksjon via enkel anomali-sjekk
  - SVG-tooltips
  - Optimerings-heuristikker
*/

// ---------- Utils ----------
const $ = (sel, root=document) => root.querySelector(sel);
const $$ = (sel, root=document) => Array.from(root.querySelectorAll(sel));
const rnd = (min, max) => Math.random()*(max-min)+min;
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const fmt = (n, digits=1) => Number(n).toFixed(digits);

// ---------- SVG tooltips ----------
(() => {
  const tip = $('#svg-tip');
  let showTips = true;
  $('#toggle-tooltips').addEventListener('click', () => {
    showTips = !showTips;
    tip.style.display = 'none';
  });
  $$('.node').forEach(node => {
    node.addEventListener('mousemove', e => {
      if(!showTips) return;
      const t = node.getAttribute('data-tip');
      tip.textContent = t || '';
      tip.style.display = 'block';
      tip.style.left = (e.offsetX + 20) + 'px';
      tip.style.top = (e.offsetY + 20) + 'px';
    });
    node.addEventListener('mouseleave', () => tip.style.display = 'none');
  });
})();

// ---------- Live dashboard sim ----------
const KPIS = [
  { key:'gridLoad', title:'Nettlast', unit:'MW' },
  { key:'lossPct',  title:'Tap', unit:'%' },
  { key:'uptime',   title:'Oppetid', unit:'%' },
  { key:'renMix',   title:'Fornybar miks', unit:'%' },
];

const state = {
  running: false,
  tick: 0,
  data: {
    gridLoad: 20,      // MW
    lossPct: 3.8,      // %
    uptime: 99.95,     // %
    renMix: 34,        // %
    rackTemp: 27.0,    // °C
    rackAmps: 420,     // A (sum)
  },
  history: []
};

function renderKPIs(){
  const wrap = $('#kpi-cards');
  wrap.innerHTML = '';
  KPIS.forEach(k => {
    const prev = state.history.at(-1)?.[k.key] ?? state.data[k.key];
    const cur  = state.data[k.key];
    const delta = cur - prev;
    const el = document.createElement('div');
    el.className = 'kpi-card';
    el.innerHTML = `
      <div class="title">${k.title}</div>
      <div class="value">${fmt(cur)} ${k.unit}</div>
      <div class="delta ${delta>=0 ? 'up':'down'}">${delta>=0? '▲':'▼'} ${fmt(Math.abs(delta))}${k.unit}</div>
    `;
    wrap.appendChild(el);
  });
}

function logEvent(msg){
  const ul = $('#event-log');
  const li = document.createElement('li');
  const t = new Date().toLocaleTimeString();
  li.textContent = `[${t}] ${msg}`;
  ul.prepend(li); // siste øverst
  // hold kort logg
  while(ul.children.length > 8) ul.removeChild(ul.lastChild);
}

let loopId = null;
function step(){
  state.tick++;

  // Simuler naturlige variasjoner:
  const dayPhase = Math.sin(state.tick/20);
  state.data.gridLoad = clamp(state.data.gridLoad + rnd(-0.4,0.6) + dayPhase*0.25, 12, 40);
  state.data.lossPct  = clamp(state.data.lossPct  + rnd(-0.10,0.10) - (state.data.renMix-30)*0.002, 2.2, 6.5);
  state.data.uptime   = clamp(99.90 + Math.abs(Math.sin(state.tick/200))*0.1, 99.7, 100);
  state.data.renMix   = clamp(state.data.renMix   + rnd(-1.0,1.2), 15, 80);

  // Miljø (for AI):
  state.data.rackTemp = clamp(state.data.rackTemp + rnd(-0.25,0.35) + (state.data.gridLoad-20)*0.01, 20, 40);
  state.data.rackAmps = clamp(state.data.rackAmps + rnd(-8,10) + (state.data.gridLoad-20)*2, 200, 1000);

  // Historikk (for delta-visning)
  state.history.push({...state.data});
  if(state.history.length>120) state.history.shift();

  renderKPIs();

  // Tilfeldige hendelser
  if(Math.random()<0.03){
    logEvent('Automatisk lastbalansering aktivert på feed B.');
  }
  if(Math.random()<0.02){
    logEvent('Isolasjonsplan testet: rack-gren 3→4 failover OK.');
  }
}

function start(){
  if(loopId) return;
  state.running = true;
  renderKPIs();
  loopId = setInterval(step, 1000);
  logEvent('Live-oppdatering startet.');
}
function stop(){
  if(loopId){
    clearInterval(loopId);
    loopId=null;
    state.running=false;
    logEvent('Live-oppdatering stoppet.');
  }
}
function reset(){
  stop();
  state.tick=0;
  state.history.length=0;
  state.data = { gridLoad:20, lossPct:3.8, uptime:99.95, renMix:34, rackTemp:27.0, rackAmps:420 };
  renderKPIs();
  $('#ai-findings').innerHTML='';
  logEvent('Verdier nullstilt.');
}

$('#btn-start').addEventListener('click', start);
$('#btn-stop').addEventListener('click', stop);
$('#btn-reset').addEventListener('click', reset);

// ---------- "AI" feildeteksjon ----------
function runAI(){
  const findings = [];
  // Enkle terskler som "anomalier"
  if(state.data.rackTemp > 33) findings.push({level:'bad',  msg:`Høy rack-temp: ${fmt(state.data.rackTemp)}°C → Øk luftflyt, vurder flytting av last`});
  if(state.data.lossPct  > 5.5) findings.push({level:'warn', msg:`Tap høyt: ${fmt(state.data.lossPct)}% → Sjekk kabeldim./konvertering`});
  if(state.data.rackAmps > 850) findings.push({level:'bad',  msg:`Strøm nær grense: ${fmt(state.data.rackAmps,0)}A → Aktiver peak-shaving (batteri)`});
  if(state.data.renMix   < 22) findings.push({level:'good', msg:`Lav fornybar nå: ${fmt(state.data.renMix)}% → Planlegg opplading når sol/vind øker`});

  const ul = $('#ai-findings');
  ul.innerHTML='';
  if(findings.length===0){
    const li = document.createElement('li');
    li.className='good';
    li.textContent = 'Ingen avvik – systemet ser stabilt ut.';
    ul.appendChild(li);
  } else {
    findings.forEach(f=>{
      const li = document.createElement('li');
      li.className = f.level;
      li.textContent = f.msg;
      ul.appendChild(li);
    });
  }
  logEvent('AI-feildeteksjon kjørt.');
}

$('#btn-run-ai').addEventListener('click', runAI);

let autoAI = null;
$('#chk-auto-ai').addEventListener('change', (e)=>{
  if(e.target.checked){
    autoAI = setInterval(runAI, 10000);
    logEvent('Auto AI-deteksjon aktivert (10s).');
  } else {
    clearInterval(autoAI); autoAI=null;
    logEvent('Auto AI-deteksjon deaktivert.');
  }
});

// ---------- Optimizer ----------
const inpRenew = $('#inp-renew');
const inpBatt  = $('#inp-batt');
const inpGrowth= $('#inp-growth');
const outRenew = $('#out-renew');
const outBatt  = $('#out-batt');
const outGrowth= $('#out-growth');

function bindRange(inp, out, suffix=''){
  const update=()=> out.textContent = inp.value + suffix;
  inp.addEventListener('input', update); update();
}
bindRange(inpRenew, outRenew, '%');
bindRange(inpBatt,  outBatt);
bindRange(inpGrowth,outGrowth, '%');

function computeKPIs(){
  const r = Number(inpRenew.value);   // %
  const b = Number(inpBatt.value);    // MWh
  const g = Number(inpGrowth.value);  // %

  // For demo: enkle heuristikker
  const baseLoss = 1_200_000; // kWh/år baseline
  const loss = baseLoss * (1 - r*0.003) * (1 - Math.min(b,15)*0.01) * (1 + g*0.004);

  const uptime = clamp(99.8 + Math.min(b,10)*0.05 - g*0.02 + r*0.01, 99.0, 99.999);
  const co2 = r*12 + b*4; // proxy-gevinst
  const pue = clamp(1.45 - r*0.002 - Math.min(b,10)*0.01 + g*0.003, 1.15, 1.6);

  $('#kpi-loss').textContent   = fmt(loss,0);
  $('#kpi-uptime').textContent = fmt(uptime,3);
  $('#kpi-co2').textContent    = fmt(co2,1);
  $('#kpi-pue').textContent    = fmt(pue,2);
}

$('#btn-optimize').addEventListener('click', computeKPIs);

// Autostart liten demo
start();
setTimeout(runAI, 1500);
