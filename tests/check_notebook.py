"""Regression test for the notebook models (u6sim v1.1).

Runs the model code of notebook/U6GHz_Simulator.ipynb (Sections 1-12, no plotting) and compares
a set of results with tests/reference_values.json. Usage:  python tests/check_notebook.py [--write]
"""
import json, sys, os, io, contextlib, copy
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt; plt.show = lambda *a, **k: None
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
nb = json.load(open(os.path.join(ROOT, "notebook", "U6GHz_Simulator.ipynb")))
code = []
for c in nb["cells"]:
    if c["cell_type"] != "code": continue
    src = "".join(c["source"])
    if "## 13" in src or "bearings = list(range" in src: break
    code.append(src.replace("SAVE = True", "SAVE = False"))
ns = {"__name__": "__main__"}
cwd = os.getcwd(); os.chdir(HERE)
with contextlib.redirect_stdout(io.StringIO()):
    for src in code:
        if "plt.subplots" in src or "plt.figure" in src: continue
        exec(compile(src, "nb", "exec"), ns)
os.chdir(cwd)
g = ns; cases = json.load(open(os.path.join(HERE, "cases.json")))
out = {"fs": {c["name"]: g["mc_fixed_service"](**c["py"])["pct"] for c in cases["fs"]}}
out["fss"] = g["mc_fss_satellite"]()["pct"]
wv = g["wifi_victim_throughput"]
out["wifi_trial"] = {f"{ch}/{w} {st}": wv(st, ch, w, use_ref_carrier=True)
                     for ch, w in ((189,160),(193,160),(221,160),(221,80)) for st in ("No_BTS","No_UE","Idle_UE","Active_UE")}
out["wifi_block_221_160_active"] = wv("Active_UE", 221, 160)
cp = g["coverage_point"]
out["coverage"] = {f"{f} MHz {d} m": cp(d, f, bw, a)[0] for d in (200, 400, 800) for f, bw, a in ((6625.0,200.0,"giga_256"),(3500.0,80.0,"macro_64"))}
out["cell_edge_snr"] = g["cell_edge_snr"]()
ul = g["ul_coexistence"]
out["terminal"] = {f"{d} {'coord' if c else 'co'} {m} m": [ul(d,221,160,m,c)["rx_ap"], ul(d,221,160,m,c)["in_dev"]]
                   for d in ("handheld","cpe_rooftop") for c in (False,True) for m in (5,10,20)}
out["res220_256"] = [r["expected"] for r in g["res220_check"]()]
ref_path = os.path.join(HERE, "reference_values.json")
if "--write" in sys.argv:
    json.dump(out, open(ref_path, "w"), indent=1); print("reference values written"); sys.exit(0)
ref = json.load(open(ref_path))
def flat(x, p=""):
    if isinstance(x, dict):
        for k, v in x.items(): yield from flat(v, p + "/" + k)
    elif isinstance(x, list):
        for i, v in enumerate(x): yield from flat(v, f"{p}[{i}]")
    else: yield p, x
a, b = dict(flat(out)), dict(flat(ref)); bad = [k for k in b if abs(a[k] - b[k]) > 1e-6]
print(f"notebook: {len(b)} values, {len(bad)} differ from the reference" + ("" if not bad else ": " + ", ".join(bad[:10])))
sys.exit(1 if bad else 0)
