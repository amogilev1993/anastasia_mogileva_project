import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.font_manager as fm

plt.rcParams["font.family"] = "DejaVu Sans"

# Цвета по типам позиций
C_V1 = "#cdeccd"   # выигрыш за 1 ход (зелёный)
C_V1E = "#2e7d32"
C_P  = "#f6c9c9"   # проигрыш ходящего (красный)
C_PE = "#c62828"
C_V2 = "#cdddf6"   # выигрыш за 2 хода (синий)
C_V2E = "#1565c0"
C_FIN = "#ffe9b3"  # финиш >=52
C_FINE = "#b8860b"

fig = plt.figure(figsize=(13.5, 12))
gs = fig.add_gridspec(2, 1, height_ratios=[1, 2.0], hspace=0.18)

# ============================================================
# ВЕРХ: полоса уровней (number strip)
# ============================================================
ax1 = fig.add_subplot(gs[0])
ax1.set_xlim(0, 13)
ax1.set_ylim(0, 3.2)
ax1.axis("off")
ax1.set_title("Полоса уровней: разбор «с конца» (финиш при n ≥ 52)",
              fontsize=15, fontweight="bold", pad=12)

def cell(ax, x, w, n_label, typ, face, edge, sub=""):
    box = FancyBboxPatch((x, 1.0), w, 1.1,
                         boxstyle="round,pad=0.02,rounding_size=0.06",
                         linewidth=2, edgecolor=edge, facecolor=face)
    ax.add_patch(box)
    ax.text(x + w/2, 1.78, n_label, ha="center", va="center",
            fontsize=15, fontweight="bold")
    ax.text(x + w/2, 1.30, typ, ha="center", va="center",
            fontsize=11, color=edge, fontweight="bold")
    if sub:
        ax.text(x + w/2, 0.78, sub, ha="center", va="top",
                fontsize=8.5, color="#444")

# ячейки: 22, 23, 24, 25, и блок 26-51
cell(ax1, 0.3, 1.7, "22", "П  (зад.21)", C_P, C_PE, "проигрыш Пети\nВаня бьёт за ≤2")
cell(ax1, 2.2, 1.7, "23", "В2 (зад.20)", C_V2, C_V2E, "Петя: +2 → 25")
cell(ax1, 4.1, 1.7, "24", "В2 (зад.20)", C_V2, C_V2E, "Петя: +1 → 25")
cell(ax1, 6.0, 1.7, "25", "П  (зад.19)", C_P, C_PE, "проигрыш Пети\nВаня бьёт за 1")
cell(ax1, 8.0, 4.6, "26 … 51", "В1 — выигрыш за 1 ход", C_V1, C_V1E,
     "из любого: ×2 ≥ 52")

# стрелка направления анализа
ax1.annotate("", xy=(0.25, 2.55), xytext=(12.7, 2.55),
             arrowprops=dict(arrowstyle="-|>", lw=2.2, color="#555"))
ax1.text(6.4, 2.78, "анализируем СПРАВА НАЛЕВО, от финиша",
         ha="center", fontsize=11, style="italic", color="#555")

# ============================================================
# НИЗ: дерево игры из S = 22
# ============================================================
ax2 = fig.add_subplot(gs[1])
ax2.set_xlim(0, 14)
ax2.set_ylim(0, 10.4)
ax2.axis("off")
ax2.set_title("Дерево игры из S = 22 (задание 21): Ваня выигрывает за ≤ 2 хода",
              fontsize=15, fontweight="bold", pad=10)

def node(x, y, text, face, edge, w=1.5, h=0.78, fs=12):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                         boxstyle="round,pad=0.02,rounding_size=0.08",
                         linewidth=2, edgecolor=edge, facecolor=face, zorder=3)
    ax2.add_patch(box)
    ax2.text(x, y, text, ha="center", va="center",
             fontsize=fs, fontweight="bold", zorder=4)

def arrow(x1, y1, x2, y2, label, color="#333", lab_dx=0.0, lab_dy=0.0):
    a = FancyArrowPatch((x1, y1), (x2, y2),
                        arrowstyle="-|>", mutation_scale=16,
                        lw=1.8, color=color, zorder=2,
                        shrinkA=14, shrinkB=14)
    ax2.add_patch(a)
    mx, my = (x1 + x2) / 2 + lab_dx, (y1 + y2) / 2 + lab_dy
    ax2.text(mx, my, label, ha="center", va="center", fontsize=10.5,
             color=color, fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85),
             zorder=5)

# --- ярусы (кто ходит) ---
ax2.text(0.15, 9.7, "ходит Петя →", fontsize=10.5, color=C_PE, fontweight="bold")
ax2.text(0.15, 7.4, "ходит Ваня →", fontsize=10.5, color=C_V2E, fontweight="bold")
ax2.text(0.15, 5.0, "ходит Петя →", fontsize=10.5, color=C_PE, fontweight="bold")
ax2.text(0.15, 2.6, "ходит Ваня →", fontsize=10.5, color=C_V2E, fontweight="bold")

# уровень 0: корень
node(7.0, 9.6, "22\nП", C_P, C_PE)

# уровень 1: ходы Пети -> 23, 24, 44
node(3.0, 7.3, "23\nВ2", C_V2, C_V2E)
node(7.0, 7.3, "24\nВ2", C_V2, C_V2E)
node(11.5, 7.3, "44\nВ1", C_V1, C_V1E)

arrow(7.0, 9.6, 3.0, 7.3, "+1")
arrow(7.0, 9.6, 7.0, 7.3, "+2")
arrow(7.0, 9.6, 11.5, 7.3, "×2")

# ветка 44 -> Ваня выигрывает сразу
node(11.5, 4.9, "88 ≥ 52\nВаня ✓", C_FIN, C_FINE, w=2.0, fs=11)
arrow(11.5, 7.3, 11.5, 4.9, "×2", color=C_V2E)
ax2.text(13.6, 6.1, "выигрыш\nза 1 ход", ha="center", fontsize=9.5,
         color=C_FINE, style="italic")

# уровень 2: Ваня загоняет Петю в 25
node(3.0, 4.9, "25\nП", C_P, C_PE)
node(7.0, 4.9, "25\nП", C_P, C_PE)
arrow(3.0, 7.3, 3.0, 4.9, "+2", color=C_V2E)
arrow(7.0, 7.3, 7.0, 4.9, "+1", color=C_V2E)

# уровень 3: Петя вынужден -> 26/27/50
node(5.0, 2.5, "26 / 27 / 50\n(все < 52)", C_P, C_PE, w=2.7, fs=10.5)
arrow(3.0, 4.9, 5.0, 2.6, "+1/+2/×2", color=C_PE, lab_dx=-1.0)
arrow(7.0, 4.9, 5.0, 2.6, "", color=C_PE)

# уровень 4: Ваня добивает
node(5.0, 0.6, "≥ 52   Ваня ✓", C_FIN, C_FINE, w=2.6, fs=11)
arrow(5.0, 2.5, 5.0, 0.6, "×2", color=C_V2E)

# Легенда
import matplotlib.patches as mpatches
leg = [
    mpatches.Patch(facecolor=C_V1, edgecolor=C_V1E, label="В1 — выигрыш за 1 ход"),
    mpatches.Patch(facecolor=C_V2, edgecolor=C_V2E, label="В2 — выигрыш за 2 хода"),
    mpatches.Patch(facecolor=C_P,  edgecolor=C_PE,  label="П  — проигрыш ходящего"),
    mpatches.Patch(facecolor=C_FIN, edgecolor=C_FINE, label="финиш (≥ 52)"),
]
ax2.legend(handles=leg, loc="lower right", fontsize=10, framealpha=0.95,
           bbox_to_anchor=(1.0, -0.02))

fig.savefig("/home/user/anastasia_mogileva_project/game_diagram.png",
            dpi=130, bbox_inches="tight", facecolor="white")
print("saved")
