# Maythayus Apps

Site vitrine des applications Maythayus, déployé par un **Cloudflare Worker** (assets statiques) : https://maythayus-apps.kaelmi.workers.dev (domaine prévu : https://apps.maythayus1.store)

Site 100 % statique (HTML/CSS, aucune dépendance). Chaque `push` sur `main` est déployé automatiquement par Cloudflare (Workers Builds).

## Modifier le contenu

1. Éditer `apps.json` (une entrée par app : nom, accroche, fonctionnalités, liens de téléchargement…).
2. Régénérer les pages : `python scripts/build.py`
3. Commit + push de `apps.json` **et** du dossier `public/`.

Le style est dans `public/styles.css`, les images dans `public/assets/`.

## Réglages Cloudflare

Le dépôt marche aussi bien en **Worker** (le fichier `wrangler.jsonc` sert le dossier `public/`, commande de déploiement `npx wrangler deploy`) qu'en **Pages** (réglages ci-dessous).

### Pages

| Champ | Valeur |
|---|---|
| Production branch | `main` |
| Framework preset | `None` |
| Build command | *(vide)* |
| Build output directory | `public` |

Domaine personnalisé : `apps.maythayus1.store` (onglet *Custom domains*).

## Aperçu local

```bash
python -m http.server 8788 --directory public
```
