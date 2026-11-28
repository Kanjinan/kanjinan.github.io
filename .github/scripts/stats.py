"""Récupère les statistiques GoatCounter (pays, pages, sites d'origine) pour le tableau de bord.

Lancé chaque heure par .github/workflows/stats.yml ; écrit le JSON sur la sortie standard.
Variables : GOATCOUNTER_TOKEN (jeton API, permission « Read statistics »), GOATCOUNTER_SITE.
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

SITE = os.environ.get("GOATCOUNTER_SITE", "nicoklem")
TOKEN = os.environ["GOATCOUNTER_TOKEN"]
API = f"https://{SITE}.goatcounter.com/api/v0/"


def get(chemin, **params):
    url = API + chemin + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + TOKEN})
    for essai in range(5):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                time.sleep(0.4)  # l'API limite à 4 requêtes par seconde
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429 and essai < 4:
                time.sleep(2)
                continue
            raise


maintenant = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
periodes = {}
for cle, jours in (("7", 7), ("30", 30), ("365", 365), ("0", None)):
    debut = (maintenant - timedelta(days=jours)) if jours else datetime(2020, 1, 1, tzinfo=timezone.utc)
    s = debut.strftime("%Y-%m-%dT%H:%M:%SZ")
    total = get("stats/total", start=s)
    pays = get("stats/locations", start=s, limit=200)
    pages = get("stats/hits", start=s, limit=20)
    refs = get("stats/toprefs", start=s, limit=15)
    periodes[cle] = {
        "visiteurs": (total.get("total") or 0) - (total.get("total_events") or 0),
        "clics": total.get("total_events") or 0,
        "pays": [{"id": p.get("id") or "", "nom": p.get("name") or "", "n": p.get("count") or 0}
                 for p in pays.get("stats") or [] if p.get("count")],
        "pages": [{"chemin": h.get("path"), "titre": h.get("title") or "", "n": h.get("count") or 0}
                  for h in pages.get("hits") or [] if not h.get("event")][:15],
        "origines": [{"nom": r.get("name") or "", "n": r.get("count") or 0} for r in refs.get("stats") or []],
    }

json.dump({"maj": maintenant.isoformat(), "periodes": periodes}, sys.stdout, ensure_ascii=False)
