"""Cliente mínimo da API oficial do Instagram (Instagram API with Instagram Login)."""
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

HOST = os.environ.get("IG_API_HOST", "https://graph.instagram.com")
VERSAO = os.environ.get("IG_API_VERSION", "v23.0")


class ErroIG(Exception):
    pass


def _req(metodo, caminho, params, token):
    params = dict(params or {})
    params["access_token"] = token
    url = f"{HOST}/{VERSAO}/{caminho.lstrip('/')}"
    dados = None
    if metodo == "GET":
        url += "?" + urllib.parse.urlencode(params)
    else:
        dados = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data=dados, method=metodo)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        corpo = e.read().decode(errors="replace")
        # nunca imprime a URL (ela contém o token)
        raise ErroIG(f"HTTP {e.code} em {metodo} {caminho}: {corpo[:800]}") from None


def conta(token):
    return _req("GET", "me", {"fields": "user_id,username"}, token)


def _esperar(container_id, token, limite_s=300):
    inicio = time.time()
    while True:
        st = _req("GET", container_id, {"fields": "status_code,status"}, token)
        cod = st.get("status_code")
        if cod in ("FINISHED", "PUBLISHED"):
            return
        if cod in ("ERROR", "EXPIRED"):
            raise ErroIG(f"Container {container_id} com status {cod}: {st.get('status')}")
        if time.time() - inicio > limite_s:
            raise ErroIG(f"Container {container_id} não ficou pronto em {limite_s}s (status {cod})")
        time.sleep(10)


def _container(ig_id, token, **params):
    r = _req("POST", f"{ig_id}/media", params, token)
    if "id" not in r:
        raise ErroIG(f"Resposta inesperada ao criar container: {r}")
    return r["id"]


def publicar(ig_id, token, tipo, urls, legenda=""):
    """tipo: FEED (1 imagem), CARROSSEL (2-20 imagens), STORY (1 imagem ou vídeo), REELS (1 vídeo)."""
    tipo = tipo.upper()
    eh_video = lambda u: u.lower().split("?")[0].endswith((".mp4", ".mov"))
    if tipo == "FEED":
        cid = _container(ig_id, token, image_url=urls[0], caption=legenda)
    elif tipo == "STORY":
        chave = "video_url" if eh_video(urls[0]) else "image_url"
        cid = _container(ig_id, token, media_type="STORIES", **{chave: urls[0]})
    elif tipo == "REELS":
        cid = _container(ig_id, token, media_type="REELS", video_url=urls[0], caption=legenda)
    elif tipo == "CARROSSEL":
        filhos = []
        for u in urls:
            if eh_video(u):
                f = _container(ig_id, token, media_type="VIDEO", video_url=u, is_carousel_item="true")
            else:
                f = _container(ig_id, token, image_url=u, is_carousel_item="true")
            _esperar(f, token)
            filhos.append(f)
        cid = _container(ig_id, token, media_type="CAROUSEL", children=",".join(filhos), caption=legenda)
    else:
        raise ErroIG(f"Tipo desconhecido: {tipo}")
    _esperar(cid, token)
    pub = _req("POST", f"{ig_id}/media_publish", {"creation_id": cid}, token)
    mid = pub.get("id")
    if not mid:
        raise ErroIG(f"Publicação sem id: {pub}")
    link = ""
    try:
        link = _req("GET", mid, {"fields": "permalink"}, token).get("permalink", "")
    except ErroIG:
        pass
    return mid, link


def renovar_token(token):
    url = "https://graph.instagram.com/refresh_access_token?" + urllib.parse.urlencode(
        {"grant_type": "ig_refresh_token", "access_token": token})
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise ErroIG(f"HTTP {e.code} ao renovar token: {e.read().decode(errors='replace')[:500]}") from None
