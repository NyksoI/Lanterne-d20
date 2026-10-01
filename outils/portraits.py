"""Génère les portraits dot-matrix (21x21) de chaque race et des PNJ.
Légende : '.' vide, '+' gris (peau), '#' blanc (contour, cheveux, traits), 'r' rouge (accent).
"""
import json, math

W = H = 21
CX = 10


def blank():
    return [['.'] * W for _ in range(H)]


def put(g, x, y, c):
    if 0 <= x < W and 0 <= y < H:
        g[y][x] = c


def ellipse(g, cx, cy, rx, ry, fill, outline=None):
    for y in range(H):
        for x in range(W):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if d <= 1.0:
                g[y][x] = fill
    if outline:
        for y in range(H):
            for x in range(W):
                d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                if d <= 1.0:
                    # bord = voisin hors ellipse
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if ((nx - cx) / rx) ** 2 + ((ny - cy) / ry) ** 2 > 1.0:
                            g[y][x] = outline
                            break


def rect(g, x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            put(g, x, y, c)


def sym(g, pts, c):
    """Points symétriques par rapport à l'axe central (x donné côté gauche)."""
    for x, y in pts:
        put(g, x, y, c)
        put(g, 2 * CX - x, y, c)


def shoulders(g, width=8, top=18):
    prev = 2
    for y in range(top, H):
        spread = min(width + (y - top), 3 + 3 * (y - top + 1))
        for x in range(CX - spread, CX + spread + 1):
            edge = abs(x - CX) == spread or (y == top) or abs(x - CX) > prev
            put(g, x, y, '#' if edge else '+')
        prev = spread
    # cou
    rect(g, CX - 1, top - 2, CX + 1, top - 1, '+')


def face(g, cy=9, rx=4.6, ry=5.6, eyes='#', eye_y=None, mouth=True):
    ellipse(g, CX, cy, rx, ry, '+', '#')
    ey = eye_y if eye_y is not None else cy
    sym(g, [(CX - 2, ey)], eyes)
    if mouth:
        put(g, CX - 1, cy + 3, '#'); put(g, CX, cy + 3, '#'); put(g, CX + 1, cy + 3, '#')


def hair_top(g, cy=9, ry=5.6, rx=4.6, rows=2):
    top = int(round(cy - ry))
    for y in range(top, top + rows + 1):
        for x in range(W):
            if g[y][x] == '+':
                g[y][x] = '#'


def finalize(g):
    return [''.join(r) for r in g]


# ---------- Races ----------

def humain():
    g = blank(); shoulders(g); face(g); hair_top(g, rows=2)
    sym(g, [(CX - 5, 7), (CX - 5, 8)], '#')  # favoris
    return g


def elfe():
    g = blank(); shoulders(g, 7); face(g, rx=4.2)
    hair_top(g, rows=2)
    # oreilles longues et pointues
    sym(g, [(CX - 5, 9), (CX - 6, 8), (CX - 7, 7), (CX - 8, 6), (CX - 6, 9), (CX - 7, 8)], '#')
    # cheveux longs
    for y in range(6, 18):
        sym(g, [(CX - 5, y)], '#') if y > 10 else None
    return g


def demi_elfe():
    g = blank(); shoulders(g); face(g); hair_top(g, rows=2)
    sym(g, [(CX - 5, 9), (CX - 6, 8), (CX - 7, 7)], '#')
    return g


def nain():
    g = blank(); shoulders(g, 9, 17); face(g, cy=9, rx=5.0, ry=5.2, eye_y=8, mouth=False)
    # casque
    rect(g, CX - 5, 3, CX + 5, 5, '#')
    sym(g, [(CX - 6, 5)], '#')
    put(g, CX, 2, '#')
    # nez
    put(g, CX, 9, '#'); put(g, CX, 10, '#')
    # grosse barbe
    for y in range(11, 20):
        w = 5 - max(0, y - 16)
        for x in range(CX - w, CX + w + 1):
            put(g, x, y, '#')
    put(g, CX, 12, '.'); put(g, CX - 1, 12, '.'); put(g, CX + 1, 12, '.')  # bouche
    return g


def halfelin():
    g = blank(); shoulders(g, 6, 18); face(g, cy=11, rx=4.0, ry=4.6)
    # cheveux bouclés
    for x in range(CX - 4, CX + 5):
        put(g, x, 6 + (x % 2), '#')
        put(g, x, 7, '#')
    sym(g, [(CX - 5, 8), (CX - 5, 9)], '#')
    # oreilles légèrement pointues
    sym(g, [(CX - 5, 11), (CX - 6, 10)], '#')
    return g


def gnome():
    g = blank(); shoulders(g, 6, 18); face(g, cy=12, rx=4.2, ry=4.2, eye_y=11, mouth=False)
    # bonnet pointu
    for i, y in enumerate(range(1, 8)):
        w = i // 1 if y > 2 else 0
        w = min(i, 5)
        rect(g, CX - w, y, CX + w, y, '#')
    put(g, CX + 1, 1, '#'); put(g, CX + 2, 0, '#')
    # gros nez
    rect(g, CX - 1, 12, CX + 1, 13, '#')
    put(g, CX - 1, 15, '#'); put(g, CX, 15, '#'); put(g, CX + 1, 15, '#')
    sym(g, [(CX - 5, 11), (CX - 6, 10)], '#')
    return g


def tieffelin():
    g = blank(); shoulders(g); face(g, eyes='r'); hair_top(g, rows=1)
    # cornes recourbées
    sym(g, [(CX - 3, 3), (CX - 4, 2), (CX - 5, 1), (CX - 6, 1), (CX - 7, 2), (CX - 7, 3), (CX - 6, 4),
            (CX - 4, 3), (CX - 5, 2)], '#')
    return g


def drakeide():
    g = blank(); shoulders(g, 9)
    # tête allongée de profil-ish : museau
    ellipse(g, CX, 9, 4.6, 5.0, '+', '#')
    rect(g, CX - 2, 12, CX + 2, 15, '+')
    sym(g, [(CX - 3, 12), (CX - 3, 13), (CX - 3, 14), (CX - 2, 15)], '#')
    put(g, CX - 1, 15, '#'); put(g, CX, 15, '#'); put(g, CX + 1, 15, '#')
    sym(g, [(CX - 1, 13)], '#')  # narines
    sym(g, [(CX - 2, 8)], 'r')  # yeux
    sym(g, [(CX - 3, 7)], '#')  # arcade
    # crête / épines
    for i, x in enumerate(range(CX - 4, CX + 5, 2)):
        put(g, x, 3, '#'); put(g, x, 2, '#' if i % 2 == 0 else '.')
    sym(g, [(CX - 6, 6), (CX - 7, 5), (CX - 6, 8), (CX - 7, 7)], '#')
    # écailles
    sym(g, [(CX - 2, 10), (CX - 1, 11)], '.')
    return g


def demi_orc():
    g = blank(); shoulders(g, 10, 17); face(g, cy=9, rx=5.4, ry=5.4, eye_y=8, mouth=False)
    hair_top(g, cy=9, ry=5.4, rows=1)
    rect(g, CX - 3, 6, CX - 1, 6, '#'); rect(g, CX + 1, 6, CX + 3, 6, '#')  # sourcils lourds
    put(g, CX, 9, '#')  # nez
    # mâchoire et défenses
    rect(g, CX - 2, 12, CX + 2, 12, '#')
    sym(g, [(CX - 2, 11)], '#')
    sym(g, [(CX - 6, 9), (CX - 6, 8)], '#')  # oreilles
    return g


def githyanki():
    g = blank(); shoulders(g, 7); face(g, cy=10, rx=3.8, ry=5.6, eye_y=9)
    # chignon haut
    rect(g, CX - 1, 0, CX + 1, 4, '#')
    rect(g, CX - 2, 1, CX + 2, 2, '#')
    hair_top(g, cy=10, ry=5.6, rows=1)
    # oreilles pointées vers l'arrière
    sym(g, [(CX - 4, 9), (CX - 5, 8), (CX - 6, 7), (CX - 5, 9)], '#')
    sym(g, [(CX - 2, 12)], '+')
    return g


def aasimar():
    g = blank(); shoulders(g); face(g, cy=10, eye_y=10); hair_top(g, cy=10, rows=2)
    # auréole
    for x in range(CX - 4, CX + 5):
        put(g, x, 1, 'r')
    sym(g, [(CX - 5, 2), (CX - 6, 3)], 'r')
    for x in range(CX - 4, CX + 5):
        put(g, x, 2, '.') if g[2][x] == '.' else None
    sym(g, [(CX - 5, 10), (CX - 5, 11), (CX - 5, 12)], '#')
    return g


def tabaxi():
    g = blank(); shoulders(g); face(g, cy=10, rx=4.8, ry=5.0, eye_y=9, mouth=False)
    # oreilles de chat
    sym(g, [(CX - 5, 2), (CX - 5, 3), (CX - 5, 4), (CX - 4, 3), (CX - 4, 4), (CX - 3, 4), (CX - 6, 5)], '#')
    # yeux félins
    sym(g, [(CX - 2, 9), (CX - 2, 8)], '#')
    # museau + moustaches
    put(g, CX, 11, '#'); put(g, CX - 1, 12, '#'); put(g, CX + 1, 12, '#')
    sym(g, [(CX - 4, 11), (CX - 5, 11), (CX - 6, 10), (CX - 4, 12), (CX - 5, 13)], '#')
    return g


def goliath():
    g = blank(); shoulders(g, 10, 17); face(g, cy=9, rx=4.8, ry=5.4, eye_y=8)
    # chauve + marques tribales
    sym(g, [(CX - 2, 5), (CX - 3, 6), (CX - 1, 4)], '#')
    sym(g, [(CX - 3, 10), (CX - 3, 11)], '#')
    rect(g, CX - 3, 7, CX - 1, 7, '#'); rect(g, CX + 1, 7, CX + 3, 7, '#')
    return g


def firbolg():
    g = blank(); shoulders(g, 9); face(g, cy=9, rx=4.6, ry=5.4, eye_y=8, mouth=False)
    hair_top(g, rows=2)
    # oreilles tombantes
    sym(g, [(CX - 5, 8), (CX - 6, 9), (CX - 7, 10), (CX - 8, 11), (CX - 6, 10), (CX - 7, 11)], '#')
    # nez bovin
    rect(g, CX - 1, 10, CX + 1, 11, '#'); put(g, CX, 11, '+')
    # barbe tressée
    rect(g, CX - 2, 13, CX + 2, 14, '#')
    for y in range(15, 19):
        put(g, CX, y, '#')
    return g


RACES = {
    'humain': humain, 'elfe': elfe, 'demi_elfe': demi_elfe, 'nain': nain, 'halfelin': halfelin,
    'gnome': gnome, 'tieffelin': tieffelin, 'drakeide': drakeide, 'demi_orc': demi_orc,
    'githyanki': githyanki, 'aasimar': aasimar, 'tabaxi': tabaxi, 'goliath': goliath, 'firbolg': firbolg,
}


# ---------- Variantes PNJ (accessoires) ----------

def with_eyepatch(g):
    put(g, CX + 2, g_eye_row(g), 'r')
    for x in range(CX - 4, CX + 5):
        if g[g_eye_row(g) - 2][x] in '+#':
            pass
    return g


def g_eye_row(g):
    for y in range(H):
        if 'r' in g[y]:
            return y
    return 9


def hood(g):
    """Capuche : arc blanc autour de la tête, visage dans l'ombre."""
    for y in range(H):
        for x in range(W):
            if g[y][x] == '+' and y < 16:
                g[y][x] = '.'
    ellipse_outline = []
    for y in range(1, 17):
        for x in range(W):
            d = ((x - CX) / 6.2) ** 2 + ((y - 9) / 7.6) ** 2
            if 0.78 < d <= 1.0:
                g[y][x] = '#'
    return g


def scar(g, row=None):
    for i in range(4):
        put(g, CX + 1 + i % 2, 6 + i, 'r')
    return g


def crown(g):
    for x in range(CX - 4, CX + 5, 2):
        put(g, x, 1, '#')
    rect(g, CX - 4, 2, CX + 4, 2, '#')
    put(g, CX, 1, 'r')
    return g


def mug(g):
    rect(g, 15, 15, 18, 19, '#'); put(g, 19, 16, '#'); put(g, 19, 17, '#'); put(g, 20, 16, '#')
    rect(g, 16, 16, 17, 18, '+')
    return g


def build():
    portraits = {k: finalize(f()) for k, f in RACES.items()}
    # PNJ de l'aventure
    portraits['npc_brunhilde'] = finalize(mug(nain()))
    portraits['npc_zephyr'] = finalize(hood(tieffelin()))
    portraits['npc_voss'] = finalize(scar(drakeide()))
    portraits['npc_ithil'] = finalize(crown(elfe()))
    p = halfelin(); put(p, CX - 1, 14, '#'); put(p, CX + 2, 13, '#')  # sourire en coin
    rect(p, 16, 13, 17, 14, 'r')  # pièce volée
    portraits['npc_pipo'] = finalize(p)
    portraits['npc_ondine'] = finalize(aasimar())
    k = githyanki()
    for i in range(7):
        put(k, 15 + i // 2, 4 + i, '#')  # épée dans le dos
    put(k, 15, 6, 'r'); put(k, 16, 5, 'r'); put(k, 14, 5, 'r')
    sym(k, [(CX - 2, 9)], 'r')
    portraits['npc_kezra'] = finalize(k)
    o = demi_orc(); put(o, CX - 6, 10, 'r'); put(o, CX + 6, 10, 'r')  # boucles d'oreille
    portraits['npc_grommash'] = finalize(o)
    return portraits


if __name__ == '__main__':
    p = build()
    # planche de contrôle
    from PIL import Image, ImageDraw
    keys = list(p.keys())
    cols = 6; cell = 21 * 8 + 20
    rows = math.ceil(len(keys) / cols)
    img = Image.new('RGB', (cols * cell, rows * (cell + 20)), 'black')
    d = ImageDraw.Draw(img)
    col = {'#': (255, 255, 255), '+': (110, 110, 110), 'r': (215, 25, 33), '.': (28, 28, 28)}
    for i, k in enumerate(keys):
        ox = (i % cols) * cell + 10; oy = (i // cols) * (cell + 20) + 10
        for y, row in enumerate(p[k]):
            for x, c in enumerate(row):
                cx, cy = ox + x * 8 + 4, oy + y * 8 + 4
                d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=col[c])
        d.text((ox, oy + 21 * 8 + 2), k, fill=(200, 200, 200))
    img.save('portraits.png')
    print(len(p), 'portraits')
