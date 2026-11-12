"""Publica no Instagram os posts aprovados cujo horário já chegou."""
import os
import shutil

import comum
import ig

MAX_TENTATIVAS = 3


def main():
    token = os.environ.get("IG_TOKEN", "").strip()
    if not token:
        raise SystemExit("Falta o segredo IG_TOKEN (Settings → Secrets and variables → Actions).")
    vencidos = [(p, d) for p, d in comum.posts()
                if d.get("aprovado") and not d.get("falhou") and comum.quando(d) <= comum.agora()]
    if not vencidos:
        print("Nada para publicar agora."); return
    ig_id = ig.conta(token)["user_id"]
    sha = comum.git("rev-parse", "HEAD").strip()
    for pasta, dados in vencidos:
        rel = pasta.relative_to(comum.RAIZ).as_posix()
        urls = [comum.url_raw(f"{rel}/{m}", sha) for m in dados["midia"]]
        try:
            mid, link = ig.publicar(ig_id, token, dados["tipo"], urls, dados.get("legenda", ""))
        except ig.ErroIG as e:
            dados["tentativas"] = dados.get("tentativas", 0) + 1
            dados["erro"] = str(e)[:1000]
            if dados["tentativas"] >= MAX_TENTATIVAS:
                dados["falhou"] = True
            comum.salvar(pasta, dados)
            comum.commitar(f"Erro ao publicar {pasta.name}")
            final = " Desisti depois de 3 tentativas." if dados.get("falhou") else " Vou tentar de novo em 15 min."
            comum.comentar(dados.get("issue"), f"⚠️ Erro ao publicar:\n```\n{dados['erro']}\n```{final}")
            print("ERRO:", pasta.name, e)
            continue
        dados.update({"publicado_em": comum.agora().isoformat(), "media_id": mid, "link": link})
        dados.pop("erro", None)
        comum.salvar(pasta, dados)
        destino = comum.PUBLICADOS / comum.quando(dados).astimezone(comum.FUSO).strftime("%Y-%m")
        destino.mkdir(parents=True, exist_ok=True)
        shutil.move(str(pasta), str(destino / pasta.name))
        comum.commitar(f"Publicado {pasta.name}")
        comum.comentar(dados.get("issue"), f"🚀 Publicado no Instagram! {link}")
        comum.fechar(dados.get("issue"))
        print("Publicado:", pasta.name, link)


if __name__ == "__main__":
    main()
