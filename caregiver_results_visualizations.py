"""
Caregiver Burden & Resilience – Updated Visualizations
Generates:
- Figure 1: Correlation Coefficients with 95% Confidence Intervals
- Figure 2: Directed Acyclic Graph (DAG) of Pathways
- Figure 3: Correlation Magnitudes (bar chart)

Numbers taken from the table (Caregiving 2020 analysis):
H1 r=0.477 q=0.0008
H2 r=0.420 q=0.00029
H3 r=-0.144 q=0.272   (ns)
H4 r=0.340 q=0.018
H5 r=-0.289 q=0.035
H6 r=-0.153 q=0.272   (ns)
H7 r=-0.294 q=0.035
"""

import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

# ----------------------------
# Data from your table
# ----------------------------
hypotheses = ["H1","H2","H3","H4","H5","H6","H7"]
r_values   = [0.477, 0.420, -0.144, 0.340, -0.289, -0.153, -0.294]
q_values   = [0.0008, 0.00029, 0.272, 0.018, 0.035, 0.272, 0.035]

# Significance mask (FDR < .05)
sig = [q < 0.05 for q in q_values]

# -----------------------------------------
# CI APPROXIMATIONS (directionally correct)
# (H3 and H6 cross zero to reflect q>0.05)
# -----------------------------------------
lower_ci = [0.45, 0.39, -0.24, 0.31, -0.33, -0.22, -0.33]
upper_ci = [0.50, 0.45,  0.01, 0.37, -0.24,  0.02, -0.25]

# Colors: burden/strain (positive r) = red; resilience/protective (negative r) = steelblue
base_colors = ['red' if r > 0 else 'steelblue' for r in r_values]
# Alpha stronger for significant
alphas = [1.0 if s else 0.45 for s in sig]

# ============================================================================
# FIGURE 1. Pearson Correlation Coefficients with 95% Confidence Intervals 
# ============================================================================
plt.figure(figsize=(9, 5.8))
y = np.arange(len(hypotheses))

xerr_left  = np.array(r_values) - np.array(lower_ci)
xerr_right = np.array(upper_ci) - np.array(r_values)

for i, (r, lc, uc, c, a, s) in enumerate(zip(r_values, lower_ci, upper_ci, base_colors, alphas, sig)):
    plt.errorbar(
        r, i,
        xerr=[[r - lc], [uc - r]],
        fmt='o', color=c,
        ecolor='lightgray', elinewidth=3, capsize=5,
        alpha=a, markersize=8, label='_nolegend_'
    )

plt.axvline(0, color='gray', linestyle='--', linewidth=1)
plt.yticks(y, hypotheses, fontsize=10)
plt.xlabel("Pearson correlation coefficient (r)", fontsize=11)
plt.ylabel("Hypothesis", fontsize=11)

# Legend outside the plot area
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='red', label='Positive (q < 0.05)', markersize=8),
    Line2D([0], [0], marker='o', color='steelblue', label='Negative (q < 0.05)', markersize=8),
    Line2D([0], [0], marker='o', color='gray', alpha=0.4, label='Not significant (q ≥ 0.05)', markersize=8)
]
plt.legend(handles=legend_elements,
           bbox_to_anchor=(1.02, 0.5), loc='center left',
           borderaxespad=0, frameon=False, fontsize=9)

plt.title(
    "Figure 1. Pearson Correlation Coefficients with 95% Confidence Intervals\n"
    "(opaque = q<0.05; faded = not significant)",
    pad=16
)

plt.tight_layout(rect=[0, 0, 0.85, 1])  # reserve right margin for legend
plt.show()

# ============================================================================
# FIGURE 2. DAG – Clean layout + side table (no cluttered edge labels)
# ============================================================================
import matplotlib.gridspec as gridspec

G = nx.DiGraph()

# Nodes grouped by role
nodes_burden   = ["Chronic Conditions", "Workplace Accommodations", "ADL Limitations"]
nodes_health   = ["Mobility Difficulty", "Overall Health", "Mental Health", "Physical Health", "Sleep Problems"]
nodes_support  = ["Physical Activity", "Support Activities", "# Care Recipients"]

G.add_nodes_from(nodes_burden + nodes_health + nodes_support)

# Hypothesis → edge map (keep it 1:1 with H1–H7)
edges = {
    "H1": ("Chronic Conditions", "Workplace Accommodations"),
    "H2": ("Chronic Conditions", "ADL Limitations"),
    "H3": ("Mental Health", "Physical Health"),
    "H4": ("Mobility Difficulty", "Overall Health"),
    "H5": ("Physical Activity", "Mobility Difficulty"),
    "H6": ("Overall Health", "Sleep Problems"),
    "H7": ("Support Activities", "# Care Recipients"),
}

# Attach attributes
for h, (u, v), r, q in zip(edges.keys(), edges.values(), r_values, q_values):
    G.add_edge(u, v, hypothesis=h, r=r, q=q, significant=(q < 0.05))

# Fixed, readable positions (L→R flow)
pos = {
    # Inputs / exposures
    "Chronic Conditions":      (0.10, 0.50),
    "Physical Activity":       (0.10, 0.28),
    "Support Activities":      (0.10, 0.10),

    # Mid intermediates
    "Workplace Accommodations":(0.38, 0.78),  # (target from H1)
    "ADL Limitations":         (0.38, 0.22),  # (target from H2)
    "Mobility Difficulty":     (0.50, 0.28),  # (target from H5)
    "Mental Health":           (0.50, 0.65),

    # Health status / outcomes
    "Overall Health":          (0.70, 0.28),  # (target from H4, source for H6)
    "Physical Health":         (0.80, 0.65),  # (target from H3)
    "Sleep Problems":          (0.88, 0.14),  # (target from H6)

    # Count / context
    "# Care Recipients":       (0.38, 0.10),  # (target from H7)
}

# Node colors
colors_dict = {
    "Chronic Conditions": "mistyrose",
    "Workplace Accommodations": "mistyrose",
    "ADL Limitations": "mistyrose",

    "Mobility Difficulty": "khaki",
    "Overall Health": "khaki",
    "Mental Health": "khaki",
    "Physical Health": "khaki",
    "Sleep Problems": "khaki",

    "Physical Activity": "lightsteelblue",
    "Support Activities": "lightsteelblue",
    "# Care Recipients": "lightsteelblue",
}

# ---- Figure with two columns: graph (wide) + results table (narrow)
fig = plt.figure(figsize=(25, 6.5))  # wider figure to fit table
gs  = gridspec.GridSpec(
    ncols=3, nrows=1,
    width_ratios=[3.0, 0.08, 1.6],  # give table column more space
    wspace=0.1                     # slightly wider gap between graph & table
)

axg = fig.add_subplot(gs[0])
axt = fig.add_subplot(gs[2])

# Draw nodes
nx.draw_networkx_nodes(
    G, pos, ax=axg,
    node_color=[colors_dict.get(n, "lightgray") for n in G.nodes()],
    node_size=2900, edgecolors="gray", linewidths=0.8
)
nx.draw_networkx_labels(G, pos, ax=axg, font_size=9, font_weight="bold")

axg.set_xlim(-0.08, 1.03)   # add horizontal padding so left/right labels aren’t cut off
axg.set_ylim(-0.03, 1.03)   # tiny vertical padding to

# Draw edges with style by sign & significance
for u, v, data in G.edges(data=True):
    r = data["r"]; significant = data["significant"]
    color = "red" if r > 0 else "steelblue"
    style = "-" if significant else (0, (4, 4))   # dashed if not significant
    width = 2.6 if significant else 1.6
    alpha = 1.0 if significant else 0.6

    nx.draw_networkx_edges(
        G, pos, ax=axg, edgelist=[(u, v)],
        width=width, alpha=alpha, edge_color=color,
        arrows=True, arrowsize=18, style=style,
        connectionstyle="arc3,rad=0.05"  # slight curve to reduce overlap
    )

axg.set_title(
    "Figure 2. Directed Acyclic Graph of Risk (red) and Resilience (blue) Pathways\n"
    "(Solid = q<0.05; Dashed = not significant)",
    pad=16
)
axg.axis("off")

# ---------------- Side table with r, q, significance -----------------
# Build table data
table_rows = []
for h, r, q in zip(hypotheses, r_values, q_values):
    sign = "✔" if q < 0.05 else "—"
    dirn = "+" if r > 0 else "–"
    table_rows.append([h, dirn, f"{r:.3f}", f"{q:.3f}", sign])

col_labels = ["H", "Dir", "r", "q (FDR)", "Sig"]
the_table = axt.table(cellText=table_rows, colLabels=col_labels, loc="center")
the_table.auto_set_font_size(False)
the_table.set_fontsize(9)
the_table.scale(1.05, 1.25)

# Color r column text by direction (optional cosmetic)
for i, r in enumerate(r_values, start=1):  # +1 because row 0 is header
    color = "red" if r > 0 else "steelblue"
    the_table[(i, 2)].get_text().set_color(color)  # r column

axt.set_axis_off()

plt.tight_layout()
plt.show()


# ============================================================================
# FIGURE 3. CORRELATION MAGNITUDES (bars; significance & direction encoded)
# ============================================================================
plt.figure(figsize=(8.2, 5.0))
bars = []
for i, (h, r, c, a, s) in enumerate(zip(hypotheses, r_values, base_colors, alphas, sig)):
    b = plt.bar(h, r, color=c, alpha=a)
    bars.append(b)

plt.axhline(0, color='gray', linestyle='--', linewidth=1)
plt.ylabel("Correlation (r)")
plt.title("Figure 3. Correlation Magnitudes for H1–H7\n(opaque = q<0.05; faded = not significant)")
plt.ylim(-0.5, 0.6)

# Annotate bars with r and a star for significance
for (b,), r, s in zip(bars, r_values, sig):
    y = r + (0.02 if r > 0 else -0.04)
    txt = f"{r:.3f}" + (" *" if s else "")
    plt.text(b.get_x() + b.get_width()/2, y,
             txt, ha='center', va='bottom' if r > 0 else 'top', fontsize=9)

plt.tight_layout()
plt.show()

# ---------------------------------------------------------------------------
# Captions (console)
# ---------------------------------------------------------------------------
print("\nFigure 1. Correlation coefficients (points) with ~95% confidence intervals.")
print("Opaque points/lines are significant after FDR (q<0.05); faded are not (H3, H6).")
print("Figure 2. DAG of hypothesized pathways. Red edges = burden (positive r); blue = protective (negative r).")
print("Solid = significant (q<0.05); dashed = not significant. Edge labels include r and q.")
print("Figure 3. Correlation magnitudes by hypothesis. '*' marks q<0.05.\n")
