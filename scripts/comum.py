"""Funções comuns: fila de posts, GitHub API e commits."""
import datetime as dt
import json
import os
import pathlib
import subprocess
import urllib.parse
import urllib.request

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FILA = RAIZ / "fila"
PUBLICADOS = RAIZ / "publicados"
CANCELADOS = RAIZ / "cancelados"
REPO = os.environ.get("GITHUB_REPOSITORY", "")
FUSO = dt.timezone(dt.timedelta(hours=-3))  # America/Sao_Paulo (sem horário de verão)


def posts():
    """Lista (pasta, dados) de todos os posts da fila, em ordem de horário."""
    itens = []
    for p in sorted(FILA.glob("*/post.json")):
        itens.append((p.parent, json.loads(p.read_text(encoding="utf-8"))))
    return sorted(itens, key=lambda x: x[1]["quando"])


def salvar(pasta, dados):
    (pasta / "post.json").write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def quando(dados):
    return dt.datetime.fromisoformat(dados["quando"])


def agora():
    return dt.datetime.now(dt.timezone.utc)


def quando_legivel(dados):
    d = quando(dados).astimezone(FUSO)
    dias = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]
    return f"{dias[d.weekday()]} {d:%d/%m} às {d:%H:%M}"


def url_raw(caminho_relativo, sha=None):
    sha = sha or git("rev-parse", "HEAD").strip()
    partes = "/".join(urllib.parse.quote(x) for x in pathlib.PurePosixPath(caminho_relativo).parts)
    return f"https://raw.githubusercontent.com/{REPO}/{sha}/{partes}"


def gh(metodo, caminho, corpo=None):
    url = f"https://api.github.com/repos/{REPO}/{caminho.lstrip('/')}"
    dados = json.dumps(corpo).encode() if corpo is not None else None
    req = urllib.request.Request(url, data=dados, method=metodo, headers={
        "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        txt = r.read().decode()
        return json.loads(txt) if txt else {}


def comentar(issue, texto):
    if issue:
        gh("POST", f"issues/{issue}/comments", {"body": texto})


def fechar(issue, motivo="completed"):
    if issue:
        gh("PATCH", f"issues/{issue}", {"state": "closed", "state_reason": motivo})


# identidade do robô para commits e rebases (o pull --rebase também precisa dela)
for _k, _v in (("GIT_AUTHOR_NAME", "lawnova-bot"), ("GIT_COMMITTER_NAME", "lawnova-bot"),
               ("GIT_AUTHOR_EMAIL", "bot@lawnova.local"), ("GIT_COMMITTER_EMAIL", "bot@lawnova.local")):
    os.environ.setdefault(_k, _v)


def git(*args):
    return subprocess.run(["git", *args], cwd=RAIZ, check=True, capture_output=True, text=True).stdout


def commitar(mensagem):
    git("add", "-A")
    if not git("status", "--porcelain").strip():
        return False
    git("-c", "user.name=lawnova-bot", "-c", "user.email=bot@lawnova.local", "commit", "-m", mensagem)
    for _ in range(3):
        try:
            git("pull", "--rebase", "origin", "main")
            git("push", "origin", "HEAD:main")
            return True
        except subprocess.CalledProcessError as e:
            print("push falhou, tentando de novo:", e.stderr[-300:])
            subprocess.run(["git", "rebase", "--abort"], cwd=RAIZ, capture_output=True)
    raise SystemExit("Não consegui enviar o commit.")
