# NicoKlem

Blog Jekyll hébergé sur GitHub Pages : https://kanjinan.github.io

- **Nouveau billet de devlog** : `_posts/AAAA-MM-JJ-titre.html` (ou `.md`), avec en tête :
  ```
  ---
  title: "Titre du billet"
  jeu: warrior-man        # slug du jeu concerné (facultatif)
  ---
  ```
- **Nouveau jeu** : copier un fichier de `_jeux/` et adapter `titre`, `resume`, `cover`, `captures`, `ordre`…
- **Images** : `images/` (captures des jeux dans `images/jeux/<slug>/`)
- **Fichiers à télécharger** : `fichiers/` (100 Mo maximum par fichier, environ 1 Go pour tout le dépôt)
- **Réglages** (titre, description) : `_config.yml`

## Langues

Le site existe en français (racine), anglais (`en/`), allemand (`de/`), espagnol (`es/`) et japonais (`ja/`).

- **Billets** : une copie par langue dans `fr/_posts/`, `en/_posts/`, `de/_posts/`, `es/_posts/`, `ja/_posts/`, avec le même nom de fichier et le même `ref` (c'est ce qui relie les traductions).
- **Jeux** : une copie par langue dans `_jeux/`, `_jeux/en/`, `_jeux/de/`, `_jeux/es/`, `_jeux/ja/`, avec le même nom de fichier.
- **Textes de l'interface** : `_data/i18n.yml`. La liste des langues et leur ordre dans le sélecteur : `langues` dans `_config.yml`.
- Une page sans traduction dans une langue n'apparaît simplement pas dans le sélecteur pour cette langue.
