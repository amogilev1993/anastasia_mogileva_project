# -*- coding: utf-8 -*-
"""Генерация вспомогательных изображений для презентации ЛР9: легенда и хронология."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse, RegularPolygon
import matplotlib.font_manager as fm

plt.rcParams["font.family"] = "DejaVu Sans"

# ---------- ЛЕГЕНДА ----------
fig, ax = plt.subplots(figsize=(8, 3.2), dpi=200)
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")

items = [
    ("ellipse", "#BBD7F2", "Персонаж — подозреваемый / участник"),
    ("ellipse", "#FFE08A", "Детектив / агент DEA"),
    ("ellipse", "#D9D9D9", "Жертва"),
    ("diamond", "#F8B5B0", "Событие (убийство, взрыв, отравление)"),
    ("box",     "#BFE3B6", "Доказательство / улика"),
]
y = 5.3
for shape, color, text in items:
    if shape == "ellipse":
        ax.add_patch(Ellipse((0.8, y), 1.1, 0.55, facecolor=color, edgecolor="#444", lw=1.3))
    elif shape == "diamond":
        ax.add_patch(RegularPolygon((0.8, y), 4, radius=0.38, orientation=0.785,
                                     facecolor=color, edgecolor="#444", lw=1.3))
    else:
        ax.add_patch(FancyBboxPatch((0.35, y-0.27), 0.9, 0.54, boxstyle="square,pad=0",
                                    facecolor=color, edgecolor="#444", lw=1.3))
    ax.text(1.7, y, text, va="center", ha="left", fontsize=12)
    y -= 1.0

# линии-связи
ax.plot([6.6, 7.4], [5.3, 5.3], color="#555", lw=2)
ax.text(7.6, 5.3, "Прямая связь / прямые улики", va="center", fontsize=11)
ax.plot([6.6, 7.4], [4.3, 4.3], color="#555", lw=2, ls="--")
ax.text(7.6, 4.3, "Косвенная связь / косвенные улики", va="center", fontsize=11)
ax.plot([6.6, 7.4], [3.3, 3.3], color="#C01C28", lw=2)
ax.text(7.6, 3.3, "Связь, ведущая к гибели/насилию", va="center", fontsize=11)
ax.plot([6.6, 7.4], [2.3, 2.3], color="#B8860B", lw=2)
ax.text(7.6, 2.3, "Линия расследования DEA", va="center", fontsize=11)

ax.set_title("Условные обозначения схемы", fontsize=14, fontweight="bold", loc="left")
plt.tight_layout()
plt.savefig("legend.png", bbox_inches="tight", facecolor="white")
plt.close()

# ---------- ХРОНОЛОГИЯ ----------
fig, ax = plt.subplots(figsize=(11, 4.2), dpi=200)
ax.axis("off")
events = [
    ("Диагноз рака.\nУолт начинает\n«варить» мет\nс Джесси", "#F8B5B0"),
    ("Появляется\nфирменный\n«голубой мет»\n— улика DEA", "#BFE3B6"),
    ("Сделка с Гусом.\nСуперлаборатория\nпод прачечной", "#BBD7F2"),
    ("Убийство Гейла\n(исполнитель —\nДжесси)", "#F8B5B0"),
    ("Отравление Брока\nрицином —\nманипуляция\nДжесси", "#F8B5B0"),
    ("Взрыв: гибель\nГуса (бомба\nГектора)", "#F8B5B0"),
    ("Книга «Leaves of\nGrass» — Хэнк\nразоблачает\nХайзенберга", "#FFE08A"),
    ("Гибель Хэнка\n(банда Джека).\nКрах империи", "#F8B5B0"),
]
n = len(events)
x = list(range(n))
ax.plot([-0.3, n-0.7], [0, 0], color="#888", lw=2.5, zorder=1)
for i, (txt, color) in enumerate(events):
    ax.scatter(i, 0, s=260, color=color, edgecolor="#333", zorder=3)
    ax.text(i, 0.06, str(i+1), ha="center", va="center", fontsize=10, fontweight="bold", zorder=4)
    up = i % 2 == 0
    ytext = 0.55 if up else -0.55
    va = "bottom" if up else "top"
    ax.annotate(txt, xy=(i, 0), xytext=(i, ytext), ha="center", va=va, fontsize=9.5,
                bbox=dict(boxstyle="round,pad=0.35", fc=color, ec="#333", lw=1),
                arrowprops=dict(arrowstyle="-", color="#777"))
ax.set_xlim(-0.6, n-0.4); ax.set_ylim(-1.25, 1.25)
ax.set_title("Хронология ключевых событий", fontsize=15, fontweight="bold")
plt.tight_layout()
plt.savefig("timeline.png", bbox_inches="tight", facecolor="white")
plt.close()
print("assets done")
