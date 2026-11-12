"""Abre uma issue de revisão (com prévia) para cada post novo da fila."""
import comum


def corpo(pasta, dados):
    rel = pasta.relative_to(comum.RAIZ).as_posix()
    imgs = "\n".join(
        f'<img src="{comum.url_raw(rel + "/" + m)}" width="360">' if not m.lower().endswith((".mp4", ".mov"))
        else f"🎬 Vídeo: [{m}]({comum.url_raw(rel + '/' + m)})"
        for m in dados["midia"])
    legenda = dados.get("legenda") or "_(story não tem legenda)_"
    return f"""**{dados['tipo']}** · {comum.quando_legivel(dados)}

{imgs}

**Legenda:**

{legenda}

---
✅ **Para aprovar:** comente `aprovado` (ou adicione a etiqueta **aprovado**).
✏️ **Para pedir mudança:** comente o que quer mudar.
🗑️ **Para cancelar:** comente `cancelar` ou feche esta issue.

<!-- post:{rel} -->"""


def garantir_etiqueta():
    try:
        comum.gh("GET", "labels/aprovado")
    except Exception:
        comum.gh("POST", "labels", {"name": "aprovado", "color": "0f766e", "description": "Liberado para publicar"})


def baixar_midias():
    """Posts podem vir com "baixar": [urls] (ex.: exportação do Canva). Baixa, converte para JPG e grava na pasta."""
    import io
    import urllib.request
    from PIL import Image
    mudou = False
    for pasta, dados in comum.posts():
        urls = dados.get("baixar")
        if not urls:
            continue
        nomes = []
        for i, u in enumerate(urls, 1):
            with urllib.request.urlopen(u, timeout=120) as r:
                bruto = r.read()
            if u.lower().split("?")[0].endswith((".mp4", ".mov")):
                nome = f"{i}.mp4"; (pasta / nome).write_bytes(bruto)
            else:
                im = Image.open(io.BytesIO(bruto)).convert("RGB")
                nome = f"{i}.jpg"; im.save(pasta / nome, "JPEG", quality=95, optimize=True)
            nomes.append(nome)
        dados["midia"] = nomes
        dados.pop("baixar")
        comum.salvar(pasta, dados)
        mudou = True
        print("Mídia baixada:", pasta.name, nomes)
    if mudou:
        comum.commitar("Baixa mídias dos posts novos")


def main():
    baixar_midias()
    novos = [(p, d) for p, d in comum.posts() if not d.get("issue")]
    if not novos:
        print("Nenhum post novo."); return
    garantir_etiqueta()
    for pasta, dados in novos:
        titulo = f"{'📱' if dados['tipo'] == 'STORY' else '🖼️'} {dados['tipo'].title()} · {comum.quando_legivel(dados)} · {dados.get('titulo', pasta.name)}"
        issue = comum.gh("POST", "issues", {"title": titulo, "body": corpo(pasta, dados)})
        dados["issue"] = issue["number"]
        comum.salvar(pasta, dados)
        print("Revisão aberta:", issue["html_url"])
    comum.commitar("Abre revisão de novos posts")


if __name__ == "__main__":
    main()
