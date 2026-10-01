# Lanterne d'Aube — un jeu de dialogue à coups de d20

Une app Android minimaliste façon Nothing : tu crées un personnage (14 races, 8 classes),
tu parles à des PNJ et tu lances des d20 pour persuader, mentir, intimider… comme dans Baldur's Gate 3.
Avec un widget d'écran d'accueil qui montre le PNJ de ta scène en cours et un d20 à lancer.

---

## 1. Installer l'outil (une seule fois)

1. Télécharge **Android Studio** (gratuit) : https://developer.android.com/studio
2. Installe-le en gardant les options par défaut. Au premier lancement, il télécharge le SDK Android (quelques Go, sois patient).

## 2. Ouvrir le projet

1. Dézippe `LanterneD20.zip`.
2. Dans Android Studio : **File → Open…** et choisis le dossier `LanterneD20`.
3. Attends la fin de la « synchronisation Gradle » (barre en bas). La première fois, ça peut prendre 5-10 minutes.
   - Si Android Studio propose de mettre à jour une version (« AGP Upgrade Assistant »), tu peux accepter.

## 3. Préparer ton Nothing Phone

1. **Paramètres → À propos du téléphone** → touche **7 fois** sur « Numéro de build » (ou « Nothing OS version ») jusqu'à voir « Vous êtes développeur ».
2. **Paramètres → Système → Options pour les développeurs** → active **Débogage USB**.
3. Branche le téléphone à l'ordinateur en USB et accepte la fenêtre « Autoriser le débogage USB ».

## 4. Lancer l'app

Dans Android Studio, ton téléphone apparaît en haut à côté du bouton ▶. Clique sur **▶ Run**.
L'app « Lanterne d20 » s'installe et s'ouvre sur ton téléphone.

> Pas de téléphone sous la main ? **Tools → Device Manager** permet de créer un téléphone virtuel.

## 5. Ajouter le widget

Sur l'écran d'accueil : appui long sur une zone vide → **Widgets** → **Lanterne d20** → glisse « PNJ & d20 ».
- Toucher le portrait ouvre le jeu.
- Toucher le dé à droite lance un d20 directement sur l'écran d'accueil.
- Le widget se met à jour tout seul quand tu avances dans l'histoire.

---

## Comment ça marche (pour aller plus loin)

```
app/src/main/
├── assets/game.json          ← TOUTE l'histoire, les races, classes, PNJ et portraits
├── java/fr/lanterne/d20/
│   ├── MainActivity.kt       ← point d'entrée de l'app
│   ├── game/                 ← règles D&D, jets de dés, sauvegarde, moteur de l'histoire
│   ├── ui/                   ← les écrans (titre, création, dialogue, jet de dé, fin)
│   └── widget/PnjWidget.kt   ← le widget d'écran d'accueil
└── res/                      ← icône, mise en page du widget, textes
outils/                       ← scripts Python pour écrire l'histoire
```

### Les règles
- **Jet** : d20 + modificateur de caractéristique + maîtrise (+2) si ta classe ou ta race maîtrise la compétence. Il faut atteindre le **DD** (degré de difficulté).
- **20 naturel** = réussite automatique (+1 inspiration). **1 naturel** = échec automatique.
- **Avantage** : certaines infos récoltées plus tôt font lancer 2 dés et garder le meilleur.
- **Inspiration** : permet de relancer un jet raté.
- **Options de race/classe** : des répliques spéciales `[TIEFFELIN]`, `[NAIN]`, `[PALADIN]`… n'apparaissent que si ton perso correspond.

### Modifier ou écrire ton histoire
L'histoire est écrite dans `outils/story.py` (plus lisible que le JSON). Après modification :

```
cd outils
python3 story.py      # régénère app/src/main/assets/game.json et vérifie les liens
python3 simulate.py   # joue des milliers de parties au hasard pour détecter les impasses
```

Chaque scène ressemble à ça :

```python
node("zephyr_1", "zephyr",                       # id de la scène, PNJ qui parle
     "« Les secrets ont un prix, étranger. »",    # texte
     [c("« Aide-moi. »", check=["persuasion", 13, "zephyr_info", "zephyr_faveur"]),  # jet : compétence, DD, si réussi, si raté
      c("« Entre cornus… »", "zephyr_frere", races=["tieffelin"]),                   # réplique réservée à une race
      c("Partir", "taverne")])                                                       # choix simple
```

Pour de nouveaux visages : `outils/portraits.py` dessine les portraits en points (21×21), puis `python3 portraits.py` génère une planche `portraits.png` pour les voir.

### Idées pour la suite
- Utiliser les **LEDs Glyph** à l'arrière du Nothing Phone (Glyph Developer Kit) pour clignoter sur un 20 naturel.
- Ajouter la police dot-matrix officielle style Nothing (par ex. « Doto » sur Google Fonts) dans `res/font`.
- Écrire un deuxième chapitre, ajouter un inventaire, des compagnons…
