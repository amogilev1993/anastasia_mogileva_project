# -*- coding: utf-8 -*-
"""Графика для презентации/отчёта ЛР9 (сериал «Менталист», арка Red John):
   легенда, хронология, аватары персонажей, мотив-смайлик Red John."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse, RegularPolygon, Circle, Arc
from matplotlib.colors import to_rgb
import numpy as np

plt.rcParams["font.family"] = "DejaVu Sans"
RED = "#C0392B"

# ---------------- ЛЕГЕНДА ----------------
fig, ax = plt.subplots(figsize=(8.4, 3.6), dpi=200)
ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis("off")
items = [
    ("ellipse", "#FFE08A", "Главный детектив (Патрик Джейн)"),
    ("ellipse", "#BBD7F2", "Команда расследования (CBI)"),
    ("ellipse", "#F2D9B0", "Подозреваемый («список семи»)"),
    ("ellipse", "#D98B8B", "Антагонист (Red John)"),
    ("ellipse", "#D9D9D9", "Жертва"),
    ("octagon", "#D6C3E8", "Организация / тайная сеть"),
    ("diamond", "#F8B5B0", "Событие"),
    ("box",     "#BFE3B6", "Доказательство / улика"),
]
y = 6.3
for shape, color, text in items:
    if shape == "ellipse":
        ax.add_patch(Ellipse((0.8, y), 1.1, 0.5, facecolor=color, edgecolor="#444", lw=1.2))
    elif shape == "diamond":
        ax.add_patch(RegularPolygon((0.8, y), 4, radius=0.34, orientation=0.785, facecolor=color, edgecolor="#444", lw=1.2))
    elif shape == "octagon":
        ax.add_patch(RegularPolygon((0.8, y), 8, radius=0.36, orientation=0.39, facecolor=color, edgecolor="#444", lw=1.2))
    else:
        ax.add_patch(FancyBboxPatch((0.4, y-0.25), 0.8, 0.5, boxstyle="square,pad=0", facecolor=color, edgecolor="#444", lw=1.2))
    ax.text(1.7, y, text, va="center", ha="left", fontsize=11.5)
    y -= 0.78
# линии-связи
defs = [("#555","-","Прямая связь / прямые улики"),
        ("#555","--","Косвенная связь / косвенные улики"),
        ("#C01C28","-","Связь, ведущая к насилию"),
        ("#B8860B","-","Линия дедукции Джейна")]
yy = 6.3
for color, ls, text in defs:
    ax.plot([6.4, 7.2], [yy, yy], color=color, lw=2, ls=ls)
    ax.text(7.4, yy, text, va="center", fontsize=11)
    yy -= 0.78
ax.set_title("Условные обозначения схемы", fontsize=14, fontweight="bold", loc="left")
plt.tight_layout(); plt.savefig("legend.png", bbox_inches="tight", facecolor="white"); plt.close()

# ---------------- ХРОНОЛОГИЯ ----------------
fig, ax = plt.subplots(figsize=(11.5, 4.3), dpi=200); ax.axis("off")
events = [
    ("Джейн оскорбляет\nRed John в\nтелеэфире", "#F8B5B0"),
    ("Убийство жены и\nдочери Джейна;\nкровавый смайлик", "#F8B5B0"),
    ("Джейн в CBI:\nначало охоты\nна Red John", "#FFE08A"),
    ("Появляется тайная\n«Ассоциация\nБлейка»", "#D6C3E8"),
    ("Разоблачён крот\nRed John\nвнутри CBI", "#F8B5B0"),
    ("Джейн составляет\nсписок из 7\nподозреваемых", "#BFE3B6"),
    ("Стих У. Блейка\n«Tyger» — ключ\nк личности", "#FFE08A"),
    ("Развязка:\nМакаллистер =\nRed John", "#D98B8B"),
]
n = len(events); ax.plot([-0.3, n-0.7], [0, 0], color="#888", lw=2.5, zorder=1)
for i, (txt, color) in enumerate(events):
    ax.scatter(i, 0, s=260, color=color, edgecolor="#333", zorder=3)
    ax.text(i, 0.05, str(i+1), ha="center", va="center", fontsize=10, fontweight="bold", zorder=4)
    up = i % 2 == 0; ytext = 0.6 if up else -0.6; va = "bottom" if up else "top"
    ax.annotate(txt, xy=(i, 0), xytext=(i, ytext), ha="center", va=va, fontsize=9.5,
                bbox=dict(boxstyle="round,pad=0.35", fc=color, ec="#333", lw=1),
                arrowprops=dict(arrowstyle="-", color="#777"))
ax.set_xlim(-0.6, n-0.4); ax.set_ylim(-1.3, 1.3)
ax.set_title("Хронология ключевых событий (арка Red John)", fontsize=15, fontweight="bold")
plt.tight_layout(); plt.savefig("timeline.png", bbox_inches="tight", facecolor="white"); plt.close()

# ---------------- АВАТАРЫ ----------------
def avatar(initials, color, fname):
    fig, ax = plt.subplots(figsize=(2.4, 2.4), dpi=200); fig.patch.set_alpha(0)
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off"); ax.set_aspect("equal")
    yy, xx = np.mgrid[0:256, 0:256]
    r = np.sqrt((xx-128)**2 + (yy-110)**2); mask = r <= 122
    base = np.array(to_rgb(color)); light = np.clip(base*1.45, 0, 1)
    shade = (r/122).clip(0, 1)[..., None]
    img = np.zeros((256, 256, 4)); img[..., :3] = light*(1-shade) + base*0.75*shade
    img[..., 3] = mask.astype(float)
    ax.imshow(img, extent=[0, 10, 0, 10], origin="upper", zorder=1)
    ax.add_patch(Circle((5, 5.2), 4.78, fill=False, edgecolor="white", lw=5, zorder=3))
    ax.add_patch(Circle((5, 5.2), 4.78, fill=False, edgecolor=color, lw=2.2, zorder=4))
    ax.text(5, 5.2, initials, fontsize=50, color="white", ha="center", va="center", fontweight="bold", zorder=5)
    plt.savefig(fname, transparent=True, bbox_inches="tight", pad_inches=0.02); plt.close()

chars = [
    ("ПД", "#C79A1E", "jane"),     # Джейн — золото
    ("ТЛ", "#2C6E9E", "lisbon"),   # Лисбон — синий
    ("КЧ", "#2F8A8A", "cho"),      # Чо — бирюза
    ("УР", "#5A6B73", "rigsby"),   # Ригсби — серо-синий
    ("ГВ", "#4C7A34", "vanpelt"),  # Ван Пелт — зелёный
    ("RJ", "#A02020", "redjohn"),  # Red John — тёмно-красный
    ("ТМ", "#C0392B", "mcallister"),# Макаллистер — красный
    ("БС", "#7A4FA3", "stiles"),   # Стайлз — фиолетовый
]
for initials, color, name in chars:
    avatar(initials, color, f"av_{name}.png")

# ---------------- МОТИВ: КРОВАВЫЙ СМАЙЛИК Red John ----------------
def smiley(fname, color=RED):
    fig, ax = plt.subplots(figsize=(2.2, 2.2), dpi=200); fig.patch.set_alpha(0)
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off"); ax.set_aspect("equal")
    ax.add_patch(Circle((5, 5), 4.4, fill=False, edgecolor=color, lw=7))
    ax.add_patch(Circle((3.4, 6.3), 0.55, color=color))
    ax.add_patch(Circle((6.6, 6.3), 0.55, color=color))
    ax.add_patch(Arc((5, 4.6), 5.0, 4.2, angle=0, theta1=200, theta2=340, lw=7, color=color))
    plt.savefig(fname, transparent=True, bbox_inches="tight", pad_inches=0.02); plt.close()

smiley("smiley.png")
print("mentalist assets done")
