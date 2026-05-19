import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patches as mpatches

plt.rcParams["font.family"] = "DejaVu Sans"

C_V1, C_V1E = "#cdeccd", "#2e7d32"   # выигрыш за 1 ход (зел)
C_P,  C_PE  = "#f6c9c9", "#c62828"   # проигрыш ходящего (кр)
C_V2, C_V2E = "#cdddf6", "#1565c0"   # выигрыш за 2 (син)
C_FIN, C_FINE = "#ffe9b3", "#b8860b" # финиш

fig, (axA, axB) = plt.subplots(1, 2, figsize=(15, 8.2))

def node(ax, x, y, text, face, edge, w=1.8, h=0.95, fs=13):
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.1",
        lw=2.2, edgecolor=edge, facecolor=face, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs,
            fontweight="bold", zorder=4)

def arrow(ax, x1, y1, x2, y2, label, color="#333", dx=0, dy=0):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2), arrowstyle="-|>",
        mutation_scale=17, lw=1.9, color=color, zorder=2,
        shrinkA=18, shrinkB=18))
    ax.text((x1+x2)/2+dx, (y1+y2)/2+dy, label, ha="center", va="center",
            fontsize=11, color=color, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.9),
            zorder=5)

# ============================================================
# A: ЗАДАНИЕ 19 — Петя в ловушке
# ============================================================
axA.set_xlim(0, 10); axA.set_ylim(0, 10); axA.axis("off")
axA.set_title("ЗАДАНИЕ 19\nПетя в ЛОВУШКЕ (S = 25)",
              fontsize=15, fontweight="bold", color=C_PE, pad=10)

node(axA, 5, 8.3, "25\nходит Петя", C_P, C_PE, w=2.6, fs=13)
# три хода -> все в зелёную зону
node(axA, 1.9, 5.3, "26", C_V1, C_V1E, w=1.5)
node(axA, 5.0, 5.3, "27", C_V1, C_V1E, w=1.5)
node(axA, 8.1, 5.3, "50", C_V1, C_V1E, w=1.5)
arrow(axA, 5, 8.3, 1.9, 5.3, "+1", C_PE)
arrow(axA, 5, 8.3, 5.0, 5.3, "+2", C_PE)
arrow(axA, 5, 8.3, 8.1, 5.3, "×2", C_PE)
# Ваня добивает
node(axA, 1.9, 2.4, "≥52\nВаня ✓", C_FIN, C_FINE, w=1.7, fs=11)
node(axA, 5.0, 2.4, "≥52\nВаня ✓", C_FIN, C_FINE, w=1.7, fs=11)
node(axA, 8.1, 2.4, "≥52\nВаня ✓", C_FIN, C_FINE, w=1.7, fs=11)
arrow(axA, 1.9, 5.3, 1.9, 2.4, "×2", C_V2E)
arrow(axA, 5.0, 5.3, 5.0, 2.4, "×2", C_V2E)
arrow(axA, 8.1, 5.3, 8.1, 2.4, "×2", C_V2E)
axA.text(5, 0.8,
         "Что бы Петя ни сделал —\nВаня выигрывает СВОИМ 1-м ходом",
         ha="center", fontsize=11.5, style="italic", color=C_PE)

# ============================================================
# B: ЗАДАНИЕ 20 — Петя загоняет Ваню в ловушку
# ============================================================
axB.set_xlim(0, 10); axB.set_ylim(0, 10); axB.axis("off")
axB.set_title("ЗАДАНИЕ 20\nПетя ЗАГОНЯЕТ Ваню в ловушку (S = 24)",
              fontsize=15, fontweight="bold", color=C_V2E, pad=10)

node(axB, 5, 8.9, "24\nходит Петя", C_V2, C_V2E, w=2.6, fs=13)
arrow(axB, 5, 8.9, 5, 7.2, "+1  (загоняем!)", C_V2E)
node(axB, 5, 6.5, "25\nходит Ваня", C_P, C_PE, w=2.6, fs=13)
# Ваня вынужден
node(axB, 1.9, 3.9, "26", C_V1, C_V1E, w=1.4)
node(axB, 5.0, 3.9, "27", C_V1, C_V1E, w=1.4)
node(axB, 8.1, 3.9, "50", C_V1, C_V1E, w=1.4)
arrow(axB, 5, 6.5, 1.9, 3.9, "+1", C_PE)
arrow(axB, 5, 6.5, 5.0, 3.9, "+2", C_PE)
arrow(axB, 5, 6.5, 8.1, 3.9, "×2", C_PE)
# Петя добивает
node(axB, 5.0, 1.4, "≥52   Петя ✓", C_FIN, C_FINE, w=3.0, fs=12)
arrow(axB, 1.9, 3.9, 5.0, 1.6, "×2", C_V2E, dx=-1.0)
arrow(axB, 5.0, 3.9, 5.0, 1.6, "", C_V2E)
arrow(axB, 8.1, 3.9, 5.0, 1.6, "×2", C_V2E, dx=1.0)

leg = [
    mpatches.Patch(facecolor=C_V1, edgecolor=C_V1E, label="В1 — выигрыш за 1 ход"),
    mpatches.Patch(facecolor=C_V2, edgecolor=C_V2E, label="В2 — выигрыш за 2 хода"),
    mpatches.Patch(facecolor=C_P,  edgecolor=C_PE,  label="П  — ловушка (ходящий проигрывает)"),
    mpatches.Patch(facecolor=C_FIN, edgecolor=C_FINE, label="финиш (≥ 52)"),
]
fig.legend(handles=leg, loc="lower center", ncol=4, fontsize=10.5,
           framealpha=0.95, bbox_to_anchor=(0.5, -0.02))

fig.tight_layout(rect=[0, 0.04, 1, 1])
fig.savefig("/home/user/anastasia_mogileva_project/game_19_20.png",
            dpi=130, bbox_inches="tight", facecolor="white")
print("saved")
