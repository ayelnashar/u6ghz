// Regression test for the browser simulator (u6sim v1.1).
// Extracts the model code from docs/index.html, evaluates the shared cases and compares them with
// tests/reference_values.json (written from the notebook). Usage:  node tests/check_browser.js
const fs = require('fs'), path = require('path');
const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'docs', 'index.html'), 'utf8');
const model = html.slice(html.indexOf('<script>') + 8, html.indexOf('/* ---------------- formatting'));
const cases = JSON.parse(fs.readFileSync(path.join(__dirname, 'cases.json'), 'utf8'));
const ref = JSON.parse(fs.readFileSync(path.join(__dirname, 'reference_values.json'), 'utf8'));
const run = new Function('cases', model + `
  const out={fs:{}};
  for(const c of cases.fs) out.fs[c.name]=mcFS(c.js).pct;
  out.fss=mcFSS().pct; out.wifi_trial={};
  for(const [ch,w] of [[189,160],[193,160],[221,160],[221,80]]) for(const st of ['No_BTS','No_UE','Idle_UE','Active_UE'])
    out.wifi_trial[ch+'/'+w+' '+st]=wifiVictim(st,ch,w,true).tp;
  out.wifi_block_221_160_active=wifiVictim('Active_UE',221,160,false).tp;
  out.coverage={};
  for(const d of [200,400,800]) for(const [f,bw,a] of [[6625,200,'giga_256'],[3500,80,'macro_64']]) out.coverage[f.toFixed(1)+' MHz '+d+' m']=coveragePoint(d,f,bw,a);
  out.cell_edge_snr=cellEdgeSnr(); out.terminal={};
  for(const d of ['handheld','cpe_rooftop']) for(const c of [0,1]) for(const m of [5,10,20]){ const r=ulCoexistence(d,221,160,m,c); out.terminal[d+' '+(c?'coord':'co')+' '+m+' m']=[r.rxAp,r.inDev]; }
  out.res220_256=res220Rows().map(r=>r.e);
  return out;`);
const out = run(cases);
const flat = (x, p = '', acc = {}) => { if (Array.isArray(x)) x.forEach((v, i) => flat(v, `${p}[${i}]`, acc));
  else if (x && typeof x === 'object') Object.entries(x).forEach(([k, v]) => flat(v, p + '/' + k, acc)); else acc[p] = x; return acc; };
const a = flat(out), b = flat(ref), bad = Object.keys(b).filter(k => !(k in a) || Math.abs(a[k] - b[k]) > 1e-6);
console.log(`browser: ${Object.keys(b).length} values, ${bad.length} differ from the notebook reference` + (bad.length ? ': ' + bad.slice(0, 10).join(', ') : ''));
process.exit(bad.length ? 1 : 0);
