"""Confere se o token funciona: mostra a conta do Instagram e o limite de publicações (não publica nada)."""
import os

import ig

token = os.environ.get("IG_TOKEN", "").strip()
if not token:
    raise SystemExit("Falta o segredo IG_TOKEN.")
c = ig.conta(token)
print(f"✅ Conectado ao Instagram @{c.get('username')} (id {c['user_id']})")
lim = ig._req("GET", f"{c['user_id']}/content_publishing_limit", {"fields": "config,quota_usage"}, token)
print("Limite de publicação:", lim)
if "graph.facebook.com" in ig.HOST:
    info = ig._req("GET", "debug_token", {"input_token": token}, token).get("data", {})
    exp = info.get("expires_at", 0)
    print("Tipo do token:", info.get("type"), "| expira:", "nunca" if exp == 0 else exp)
    print("Permissões:", ", ".join(info.get("scopes", [])))
