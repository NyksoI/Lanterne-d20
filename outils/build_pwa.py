import re, json
src = open('preview_src.html', encoding='utf-8').read()

def rep(old, new, count=1):
    global src
    assert old in src, old[:80]
    src = src.replace(old, new, count)

# ── tête HTML complète pour une vraie web-app ──
rep("<title>Lanterne d'Aube</title>", """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#000000">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-192.png">
<link rel="apple-touch-icon" href="icon-192.png">
<title>Lanterne d20</title>""")
rep("</style>\n", "</style>\n</head>\n<body>\n")

# ── plein écran sur téléphone ──
rep("body { font-family: var(--f-mono); font-size: 15px; line-height: 1.55; padding-inline: 16px; padding-block: 20px 40px; }",
    "html, body { margin: 0; min-height: 100%; }\n* { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }\n"
    "body { font-family: var(--f-mono); font-size: 15px; line-height: 1.55; padding-inline: 16px; padding-block: 20px 40px; }\n"
    "@media (max-width: 560px) { body { padding: 0; } .phone { border: 0 !important; border-radius: 0 !important; min-height: 100dvh !important;"
    " padding: calc(env(safe-area-inset-top, 0px) + 16px) 18px calc(env(safe-area-inset-bottom, 0px) + 22px) !important; } .wrap { gap: 0; } }")

# ── retirer l'aperçu du widget (pas de widget possible pour une web-app) ──
src = re.sub(r'\n  <section class="stack">.*?</section>\n', '\n', src, flags=re.S)
src = re.sub(r'/\* ── widget ── \*/.*?\n(?=let lastW)', '', src, flags=re.S)
rep("  updateWidget();\n}", "  save();\n}")
src = src.replace("updateWidget();", "")

# ── sauvegarde de la partie ──
rep("const d20 = () => 1 + Math.floor(Math.random() * 20);", """const d20 = () => 1 + Math.floor(Math.random() * 20);
const KEY = 'lanterne-d20-save';
function save() {
  if (!S.player) return;
  try { localStorage.setItem(KEY, JSON.stringify({ player: S.player, scene: S.scene, flags: [...S.flags], insp: S.insp })); } catch (e) {}
}
function loadSave() {
  try { const d = JSON.parse(localStorage.getItem(KEY)); if (d && d.player && GAME.nodes[d.scene]) return d; } catch (e) {}
  return null;
}
function clearSave() { try { localStorage.removeItem(KEY); } catch (e) {} }
function continueGame() {
  const d = loadSave(); if (!d) return;
  S.player = d.player; S.scene = d.scene; S.flags = new Set(d.flags); S.insp = d.insp; S.pending = null; S.screen = 'play'; render();
}""")

# Bouton « Continuer » sur l'écran titre
rep("""    h('button', { class: 'btn', onclick: () => { S.screen = 'create'; render(); } }, 'Nouvelle partie'),""",
    """    ...(loadSave() ? [h('button', { class: 'btn', onclick: continueGame }, 'Continuer')] : []),
    h('button', { class: loadSave() ? 'btn ghost' : 'btn', onclick: () => { S.screen = 'create'; render(); } }, 'Nouvelle partie'),""")

# Fin de partie : on efface la sauvegarde en recommençant
rep("""h('button', { class: 'btn', onclick: () => { S.screen = 'create'; render(); } }, 'Nouvelle aventure')""",
    """h('button', { class: 'btn', onclick: () => { clearSave(); S.player = null; S.screen = 'create'; render(); } }, 'Nouvelle aventure')""")

# Le menu ne doit pas perdre la partie : S.player reste, la sauvegarde aussi.
# ── service worker (hors-ligne) ──
i = src.rindex("</script>")
src = src[:i] + "if ('serviceWorker' in navigator) navigator.serviceWorker.register('sw.js').catch(() => {});\n" + src[i:]
src = src.replace("document.fonts && document.fonts.ready.then(() => {});\n", "")
src = src.rstrip() + "\n</body>\n</html>\n"
rep('/* Layout : une colonne façon téléphone Nothing, centrée ; un aperçu du widget sous le jeu. Look unique sombre assumé. */',
    '/* Layout : web-app plein écran façon Nothing (une colonne centrée sur grand écran). Look unique sombre assumé. */')

game = open('/home/claude/LanterneD20/app/src/main/assets/game.json', encoding='utf-8').read()
src = src.replace('__GAME_JSON__', game)
open('/home/claude/lanterne-d20/docs/index.html', 'w', encoding='utf-8').write(src)

json.dump({
    "name": "Lanterne d20", "short_name": "Lanterne d20",
    "description": "Jeu de dialogue à coups de d20, façon Nothing.",
    "lang": "fr", "start_url": "./", "scope": "./", "display": "standalone",
    "orientation": "portrait", "background_color": "#000000", "theme_color": "#000000",
    "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
}, open('/home/claude/lanterne-d20/docs/manifest.webmanifest', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

open('/home/claude/lanterne-d20/docs/sw.js', 'w').write("""// Met le jeu en cache pour qu'il marche sans connexion.
const CACHE = 'lanterne-d20-v1';
const FILES = ['./', './index.html', './manifest.webmanifest', './icon-192.png', './icon-512.png', './icon-maskable-512.png'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES))); self.skipWaiting(); });
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))));
  self.clients.claim();
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  // réseau d'abord (pour recevoir les mises à jour), cache si hors-ligne
  e.respondWith(fetch(e.request).then(r => {
    if (r.ok && new URL(e.request.url).origin === location.origin) { const copy = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); }
    return r;
  }).catch(() => caches.match(e.request).then(m => m || caches.match('./index.html'))));
});
""")
open('/home/claude/lanterne-d20/docs/.nojekyll', 'w').write('')
print("ok", len(src))
