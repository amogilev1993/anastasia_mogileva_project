# -*- coding: utf-8 -*-
"""Генерация красивой графики для презентации ЛР9 (Breaking Bad):
   - логотип из «химических плиток» (Br/Ba) — стилистический оммаж;
   - круглые аватары персонажей с инициалами и цветом фракции."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
import numpy as np

plt.rcParams["font.family"] = "DejaVu Sans"

GREEN = "#5AA634"
DARKG = "#14211A"

# ---------- ПЛИТКА-ЭЛЕМЕНТ (как в логотипе сериала) ----------
def element_tile(symbol, number, name, fname):
    fig, ax = plt.subplots(figsize=(2.2, 2.2), dpi=200)
    fig.patch.set_alpha(0)
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.4, 0.4), 9.2, 9.2,
                 boxstyle="round,pad=0.1,rounding_size=0.8",
                 facecolor=GREEN, edgecolor="white", lw=3))
    ax.text(1.4, 8.3, str(number), fontsize=20, color="white", ha="left", va="center")
    ax.text(5, 4.7, symbol, fontsize=64, color="white", ha="center", va="center", fontweight="bold")
    ax.text(5, 1.5, name, fontsize=15, color="white", ha="center", va="center")
    plt.savefig(fname, transparent=True, bbox_inches="tight", pad_inches=0.02)
    plt.close()

element_tile("Br", 35, "Bromine", "tile_br.png")
element_tile("Ba", 56, "Barium", "tile_ba.png")

# ---------- АВАТАРЫ ПЕРСОНАЖЕЙ ----------
def avatar(initials, color, fname):
    fig, ax = plt.subplots(figsize=(2.4, 2.4), dpi=200)
    fig.patch.set_alpha(0)
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off"); ax.set_aspect("equal")
    # мягкий радиальный градиент внутри круга
    grad = np.linspace(0, 1, 256).reshape(1, -1)
    grad = np.vstack([grad] * 256)
    yy, xx = np.mgrid[0:256, 0:256]
    r = np.sqrt((xx - 128) ** 2 + (yy - 110) ** 2)
    mask = r <= 122
    img = np.zeros((256, 256, 4))
    from matplotlib.colors import to_rgb
    base = np.array(to_rgb(color))
    light = np.clip(base * 1.45, 0, 1)
    shade = (r / 122).clip(0, 1)[..., None]
    rgb = light * (1 - shade) + base * 0.75 * shade
    img[..., :3] = rgb
    img[..., 3] = mask.astype(float)
    ax.imshow(img, extent=[0, 10, 0, 10], origin="upper", zorder=1)
    ax.add_patch(Circle((5, 5.2), 4.78, fill=False, edgecolor="white", lw=5, zorder=3))
    ax.add_patch(Circle((5, 5.2), 4.78, fill=False, edgecolor=color, lw=2.2, zorder=4))
    ax.text(5, 5.2, initials, fontsize=52, color="white", ha="center", va="center",
            fontweight="bold", zorder=5)
    plt.savefig(fname, transparent=True, bbox_inches="tight", pad_inches=0.02)
    plt.close()

chars = [
    ("УУ", "#4C7A34", "walt"),    # Уолт — зелёный (организатор)
    ("ДП", "#2C6E9E", "jesse"),   # Джесси — синий
    ("ГФ", "#7A4FA3", "gus"),     # Гус — фиолетовый
    ("ХШ", "#C79A1E", "hank"),    # Хэнк (DEA) — золото
    ("СУ", "#B0457A", "skyler"),  # Скайлер — розово-фиолетовый
    ("СГ", "#D2691E", "saul"),    # Сол — оранжевый
    ("МЭ", "#5A6B73", "mike"),    # Майк — серо-синий
    ("ГБ", "#7E8B57", "gale"),    # Гейл — оливковый (жертва)
]
for initials, color, name in chars:
    avatar(initials, color, f"av_{name}.png")

print("assets2 done")
