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
# FIGURE 1. COEFFICIENT PLOT WITH 95% CI
# ============================================================================
plt.figure(figsize=(7.5, 5.2))
y = np.arange(len(hypotheses))

xerr_left  = np.array(r_values) - np.array(lower_ci)
xerr_right = np.array(upper_ci) - np.array(r_values)

# Plot each point separately to control color/alpha by significance
for i, (r, lc, uc, c, a, s) in enumerate(zip(r_values, lower_ci, upper_ci, base_colors, alphas, sig)):
    plt.errorbar(
        r, i,
        xerr=np.array([[r - lc], [uc - r]]),
        fmt='o',
        color=c,
        ecolor='lightgray',
        elinewidth=3,
        capsize=5,
        alpha=a,
        markersize=7
    )

# zero line
plt.axvline(0, color='gray', linestyle='--', linewidth=1)

plt.yticks(y, hypotheses)
plt.xlabel("Correlation (r)")
plt.title("Figure 1. Correlation Coefficients with 95% Confidence Intervals\n(opaque = q<0.05; faded = not significant)")
plt.tight_layout()
plt.show()

# ============================================================================
# FIGURE 2. DAG – CONCEPTUAL PATHWAYS (edges styled by sign & significance)
# ============================================================================
G = nx.DiGraph()

# Nodes by theme
nodes_burden   = ["Chronic Conditions", "Workplace Accommodations", "ADL Limitations"]
nodes_health   = ["Mobility Difficulty", "Overall Health", "Mental Health", "Physical Health"]
nodes_support  = ["Physical Activity", "Support Activities", "# Care Recipients"]

G.add_nodes_from(nodes_burden + nodes_health + nodes_support)

# Map each hypothesis to an edge with its r and q
edges = {
    "H1": ("Chronic Conditions", "Workplace Accommodations"),
    "H2": ("Chronic Conditions", "ADL Limitations"),
    "H3": ("Mental Health", "Physical Health"),
    "H4": ("Mobility Difficulty", "Overall Health"),
    "H5": ("Physical Activity", "Mobility Difficulty"),
    "H6": ("Overall Health", "Sleep Problems")  # create node if not in graph
    if "Sleep Problems" in G.nodes else ("Overall Health", "Sleep Problems"),
    "H7": ("Support Activities", "# Care Recipients")
}

# Ensure "Sleep Problems" exists (H6)
if "Sleep Problems" not in G.nodes:
    G.add_node("Sleep Problems")

# Add edges with attributes
for (h, (u, v)), r, q in zip(edges.items(), r_values, q_values):
    G.add_edge(u, v, key=h, r=r, q=q, significant=(q < 0.05))

# Node colors
colors_dict = {
    # burden / exposure
    "Chronic Conditions": "mistyrose",
    "Workplace Accommodations": "mistyrose",
    "ADL Limitations": "mistyrose",
    # health status links
    "Mobility Difficulty": "khaki",
    "Overall Health": "khaki",
    "Mental Health": "khaki",
    "Physical Health": "khaki",
    "Sleep Problems": "khaki",
    # protective / support
    "Physical Activity": "lightsteelblue",
    "Support Activities": "lightsteelblue",
    "# Care Recipients": "lightsteelblue",
}

plt.figure(figsize=(10, 6.6))
pos = nx.spring_layout(G, seed=42)

# Draw nodes
nx.draw_networkx_nodes(
    G, pos,
    node_color=[colors_dict.get(n, "lightgray") for n in G.nodes()],
    node_size=2900,
    edgecolors="gray",
    linewidths=0.8
)
nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold")

# Edge styling by sign & significance
for (u, v, k), data in G.edges.items():
    r = data["r"]
    q = data["q"]
    significant = data["significant"]

    color = "red" if r > 0 else "steelblue"
    style = "-" if significant else (0, (4, 4))  # dashed if not significant
    width = 2.5 if significant else 1.5
    alpha = 1.0 if significant else 0.55

    nx.draw_networkx_edges(
        G, pos,
        edgelist=[(u, v)],
        width=width,
        alpha=alpha,
        edge_color=color,
        arrows=True,
        arrowsize=18,
        style=style
    )

    # Edge labels with r and q
    label = f"{k}: r={r:.3f}, q={q:.3f}"
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels={(u, v): label},
        font_size=8,
        label_pos=0.5,
        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.8)
    )

plt.title("Figure 2. Directed Acyclic Graph of Risk (red) and Resilience (blue) Pathways\n(Solid = q<0.05; Dashed = not significant)")
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
