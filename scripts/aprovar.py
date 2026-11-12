"""Trata eventos das issues de revisão: aprovar, cancelar ou registrar pedido de mudança."""
import json
import os
import re
import shutil

import comum

APROVA = re.compile(r"^\s*(aprovad[oa]s?|aprovar|aprovo|pode (postar|publicar))\b", re.I)
CANCELA = re.compile(r"^\s*(cancelar|cancela|reprovad[oa]|n[aã]o publicar)\b", re.I)


def achar_post(issue):
    m = re.search(r"<!-- post:(\S+) -->", issue.get("body") or "")
    if not m:
        return None, None
    pasta = comum.RAIZ / m.group(1)
    if not (pasta / "post.json").exists():
        return None, None
    return pasta, json.loads((pasta / "post.json").read_text(encoding="utf-8"))


def main():
    ev = json.load(open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8"))
    nome = os.environ["GITHUB_EVENT_NAME"]
    issue = ev["issue"]
    pasta, dados = achar_post(issue)
    if not pasta:
        print("Issue não corresponde a post da fila."); return
    acao = None
    if nome == "issues" and ev["action"] == "labeled" and ev["label"]["name"] == "aprovado":
        acao = "aprovar"
    elif nome == "issues" and ev["action"] == "closed" and not dados.get("aprovado"):
        acao = "cancelar"
    elif nome == "issue_comment" and ev["action"] == "created":
        # repositório é público: só o dono (ou colaboradores) pode aprovar/cancelar
        if ev["comment"]["author_association"] not in ("OWNER", "COLLABORATOR", "MEMBER"):
            print("Comentário de terceiro ignorado."); return
        txt = ev["comment"]["body"]
        if APROVA.search(txt):
            acao = "aprovar"
        elif CANCELA.search(txt):
            acao = "cancelar"
    if acao == "aprovar" and not dados.get("aprovado"):
        dados["aprovado"] = True
        comum.salvar(pasta, dados)
        comum.commitar(f"Aprova {pasta.name}")
        quando = comum.quando(dados)
        msg = ("Publicando agora." if quando <= comum.agora()
               else f"Será publicado {comum.quando_legivel(dados)}.")
        comum.comentar(dados["issue"], f"✅ Aprovado! {msg}")
    elif acao == "cancelar":
        comum.CANCELADOS.mkdir(exist_ok=True)
        shutil.move(str(pasta), str(comum.CANCELADOS / pasta.name))
        comum.commitar(f"Cancela {pasta.name}")
        comum.comentar(dados["issue"], "🗑️ Cancelado. Não será publicado.")
        if issue["state"] != "closed":
            comum.fechar(dados["issue"], "not_planned")
    else:
        print("Nada a fazer.")


if __name__ == "__main__":
    main()
