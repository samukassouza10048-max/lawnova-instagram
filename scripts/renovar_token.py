"""Renova o token do Instagram (vale 60 dias) e grava o novo no segredo IG_TOKEN."""
import base64
import json
import os
import urllib.request

import ig


def gravar_segredo(nome, valor, pat, repo):
    from nacl import encoding, public  # PyNaCl

    def api(metodo, caminho, corpo=None):
        req = urllib.request.Request(f"https://api.github.com/repos/{repo}/{caminho}", method=metodo,
                                     data=json.dumps(corpo).encode() if corpo else None,
                                     headers={"Authorization": f"Bearer {pat}", "Accept": "application/vnd.github+json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            t = r.read().decode()
            return json.loads(t) if t else {}

    chave = api("GET", "actions/secrets/public-key")
    caixa = public.SealedBox(public.PublicKey(chave["key"].encode(), encoding.Base64Encoder()))
    cifrado = base64.b64encode(caixa.encrypt(valor.encode())).decode()
    api("PUT", f"actions/secrets/{nome}", {"encrypted_value": cifrado, "key_id": chave["key_id"]})


def main():
    if "graph.facebook.com" in ig.HOST:
        print("Token de Página do Facebook não expira: nada a renovar.")
        return
    token = os.environ["IG_TOKEN"].strip()
    r = ig.renovar_token(token)
    novo = r.get("access_token", "")
    dias = int(r.get("expires_in", 0)) // 86400
    print(f"Token renovado: válido por mais {dias} dias.")
    if novo and novo != token:
        pat = os.environ.get("GH_PAT", "").strip()
        if not pat:
            raise SystemExit("O Instagram devolveu um token novo, mas falta o segredo GH_PAT para gravá-lo.")
        gravar_segredo("IG_TOKEN", novo, pat, os.environ["GITHUB_REPOSITORY"])
        print("Segredo IG_TOKEN atualizado.")


if __name__ == "__main__":
    main()
