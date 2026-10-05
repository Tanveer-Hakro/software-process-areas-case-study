from pathlib import Path
import csv
import math
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 160,
    "savefig.dpi": 220,
    "font.size": 10,
    "axes.titlesize": 14,
    "axes.labelsize": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

def rows(name):
    with open(DATA / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

# 1) Requirements priority distribution
req = rows("requirements.csv")
labels = ["High", "Medium", "Low"]
counts = [sum(r["priority"] == x for r in req) for x in labels]
fig, ax = plt.subplots(figsize=(7.6, 4.7))
wedges, _, autotexts = ax.pie(
    counts, labels=labels, autopct=lambda p: f"{p:.0f}%", startangle=90,
    wedgeprops={"width": 0.42, "edgecolor": "white"}
)
ax.text(0, 0.07, "5", ha="center", va="center", fontsize=28, fontweight="bold")
ax.text(0, -0.12, "requirements", ha="center", va="center", fontsize=10)
ax.set_title("Stakeholder requirements by priority", pad=16, fontweight="bold")
fig.text(0.5, 0.02, "High-priority items dominate the planning baseline.", ha="center", fontsize=9)
fig.tight_layout(rect=(0, 0.05, 1, 1))
fig.savefig(OUT / "requirements-priority.png", bbox_inches="tight")
plt.close(fig)

# 2) Budget planned vs actual
budget = rows("budget.csv")
cats = [r["category"] for r in budget]
planned = [float(r["planned"]) for r in budget]
actual = [float(r["actual"]) for r in budget]
y = np.arange(len(cats))
fig, ax = plt.subplots(figsize=(9.0, 5.3))
h = 0.34
ax.barh(y - h/2, planned, height=h, label="Planned")
ax.barh(y + h/2, actual, height=h, label="Actual")
ax.set_yticks(y, cats)
ax.invert_yaxis()
ax.set_xlabel("Cost ($)")
ax.set_title("Budget plan vs actual expenditure", fontweight="bold", pad=14)
ax.legend(frameon=False, ncol=2, loc="lower right")
for i, (p, a) in enumerate(zip(planned, actual)):
    ax.text(max(p, a) + 3, i, f"${a:.0f}", va="center", fontsize=9)
ax.grid(axis="x", alpha=0.18)
fig.text(0.5, 0.01, "Planned: $440   •   Actual: $400   •   Positive variance: $40", ha="center", fontsize=9)
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig(OUT / "budget-plan-vs-actual.png", bbox_inches="tight")
plt.close(fig)

# 3) Quality dashboard
quality = rows("quality_metrics.csv")
phases = [r["phase"] for r in quality]
scores = [float(r["score"]) for r in quality]
fig, ax = plt.subplots(figsize=(8.4, 4.8))
bars = ax.barh(phases, scores)
ax.set_xlim(0, 105)
ax.set_xlabel("Quality score (%)")
ax.set_title("Quality performance by project phase", fontweight="bold", pad=14)
ax.grid(axis="x", alpha=0.18)
for bar, score in zip(bars, scores):
    ax.text(score + 1.2, bar.get_y() + bar.get_height()/2, f"{score:.0f}%", va="center", fontsize=10, fontweight="bold")
ax.text(0.98, 0.08, "Overall quality: 93%", transform=ax.transAxes, ha="right", va="bottom", fontsize=11, fontweight="bold")
fig.tight_layout()
fig.savefig(OUT / "quality-dashboard.png", bbox_inches="tight")
plt.close(fig)

# 4) Performance radar
perf = rows("performance_metrics.csv")
metrics = [r["metric"] for r in perf]
values = [float(r["score"]) for r in perf]
target = [float(r["target"]) for r in perf]
angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False).tolist()
values_c = values + values[:1]
target_c = target + target[:1]
angles_c = angles + angles[:1]
fig = plt.figure(figsize=(8.2, 6.2))
ax = plt.subplot(111, polar=True)
ax.plot(angles_c, target_c, linewidth=1.8, linestyle="--", label="Ideal target")
ax.plot(angles_c, values_c, linewidth=2.2, label="Actual performance")
ax.fill(angles_c, values_c, alpha=0.18)
ax.set_xticks(angles)
ax.set_xticklabels(metrics, fontsize=9)
ax.set_yticks([1,2,3,4,5])
ax.set_ylim(0,5)
ax.set_title("Project performance across six dimensions", y=1.12, fontweight="bold")
ax.legend(loc="upper right", bbox_to_anchor=(1.28, 1.15), frameon=False)
fig.tight_layout()
fig.savefig(OUT / "performance-radar.png", bbox_inches="tight")
plt.close(fig)

# 5) Process-area workflow as SVG
svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 520" role="img" aria-labelledby="title desc">
<title id="title">Software process-area workflow</title>
<desc id="desc">Requirements Management feeds Project Planning, which is monitored by Project Monitoring and Control, assured by Process and Product Quality Assurance, and controlled through Configuration Management.</desc>
<defs>
  <linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#f8fafc"/><stop offset="1" stop-color="#eef2ff"/></linearGradient>
  <filter id="s" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="6" stdDeviation="8" flood-opacity="0.12"/></filter>
  <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#64748b"/></marker>
</defs>
<rect width="1200" height="520" rx="28" fill="url(#g)"/>
<text x="600" y="58" text-anchor="middle" font-family="Arial, sans-serif" font-size="30" font-weight="700" fill="#0f172a">Integrated process-area workflow</text>
<text x="600" y="92" text-anchor="middle" font-family="Arial, sans-serif" font-size="16" fill="#475569">From stakeholder needs to controlled, quality-assured delivery</text>

<g font-family="Arial, sans-serif" filter="url(#s)">
  <rect x="60" y="180" width="190" height="120" rx="18" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="155" y="220" text-anchor="middle" font-size="18" font-weight="700" fill="#0f172a">RM</text>
  <text x="155" y="247" text-anchor="middle" font-size="15" fill="#334155">Requirements</text>
  <text x="155" y="268" text-anchor="middle" font-size="15" fill="#334155">Management</text>

  <rect x="300" y="180" width="190" height="120" rx="18" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="395" y="220" text-anchor="middle" font-size="18" font-weight="700" fill="#0f172a">PP</text>
  <text x="395" y="247" text-anchor="middle" font-size="15" fill="#334155">Project</text>
  <text x="395" y="268" text-anchor="middle" font-size="15" fill="#334155">Planning</text>

  <rect x="540" y="180" width="190" height="120" rx="18" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="635" y="220" text-anchor="middle" font-size="18" font-weight="700" fill="#0f172a">PMC</text>
  <text x="635" y="247" text-anchor="middle" font-size="15" fill="#334155">Monitoring</text>
  <text x="635" y="268" text-anchor="middle" font-size="15" fill="#334155">&amp; Control</text>

  <rect x="780" y="180" width="190" height="120" rx="18" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="875" y="220" text-anchor="middle" font-size="18" font-weight="700" fill="#0f172a">PPQA</text>
  <text x="875" y="247" text-anchor="middle" font-size="15" fill="#334155">Quality</text>
  <text x="875" y="268" text-anchor="middle" font-size="15" fill="#334155">Assurance</text>

  <rect x="1020" y="180" width="120" height="120" rx="18" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="1080" y="220" text-anchor="middle" font-size="18" font-weight="700" fill="#0f172a">CM</text>
  <text x="1080" y="247" text-anchor="middle" font-size="15" fill="#334155">Config.</text>
  <text x="1080" y="268" text-anchor="middle" font-size="15" fill="#334155">Control</text>
</g>

<g stroke="#64748b" stroke-width="3" fill="none" marker-end="url(#arrow)">
  <path d="M250 240 H292"/>
  <path d="M490 240 H532"/>
  <path d="M730 240 H772"/>
  <path d="M970 240 H1012"/>
</g>
<path d="M875 315 C875 420 395 420 395 315" fill="none" stroke="#64748b" stroke-width="2.5" stroke-dasharray="8 8" marker-end="url(#arrow)"/>
<text x="635" y="438" text-anchor="middle" font-family="Arial, sans-serif" font-size="15" fill="#475569">Quality findings and monitoring results feed corrective planning</text>

<g font-family="Arial, sans-serif" font-size="14" fill="#475569">
  <text x="155" y="334" text-anchor="middle">Capture &amp; trace needs</text>
  <text x="395" y="334" text-anchor="middle">Schedule &amp; budget</text>
  <text x="635" y="334" text-anchor="middle">Track progress &amp; risk</text>
  <text x="875" y="334" text-anchor="middle">Verify adherence</text>
  <text x="1080" y="334" text-anchor="middle">Protect baselines</text>
</g>
</svg>'''
(OUT / "process-area-workflow.svg").write_text(svg, encoding="utf-8")

print("Generated:")
for p in sorted(OUT.iterdir()):
    print(" -", p.name)
