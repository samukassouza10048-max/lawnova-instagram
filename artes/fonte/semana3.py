"""Semana 23–27/11: 10 stories (1080x1920) + 3 feeds (1080x1350) em HTML -> JPG."""
import pathlib, sys
from playwright.sync_api import sync_playwright
import build as B  # reaproveita ícones, cores, CSS do carrossel 6x1

D = pathlib.Path(__file__).parent
OUT = D / "s3"; OUT.mkdir(exist_ok=True)
I, COR, ico, card, check = B.I, B.COR, B.ico, B.card, B.check
I["scale"] = '<path d="M12 3v18M6 21h12M5 7h14"/><path d="M5 7l-3 6a3 3 0 0 0 6 0zM19 7l-3 6a3 3 0 0 0 6 0z"/>'
I["bell"] = '<path d="M6 16V11a6 6 0 0 1 12 0v5l1.5 2h-15z"/><path d="M10 20.5a2 2 0 0 0 4 0"/>'
I["spark"] = '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>'
I["sheet"] = '<rect x="3.5" y="3.5" width="17" height="17" rx="2"/><path d="M3.5 9h17M3.5 14.5h17M9 3.5v17M14.5 3.5v17"/>'
I["badge"] = '<rect x="3" y="5" width="18" height="14" rx="2.5"/><circle cx="9" cy="11" r="2.4"/><path d="M5.5 16.5a3.5 3.5 0 0 1 7 0M14.5 10h4M14.5 13.5h3"/>'
I["x"] = '<path d="M6 6l12 12M18 6L6 18"/>'
I["msg"] = '<path d="M4 5h16v11H9l-5 4z"/>'
I["user"] = '<circle cx="12" cy="8" r="3.5"/><path d="M5 20a7 7 0 0 1 14 0"/>'
I["pause"] = '<circle cx="12" cy="12" r="9"/><path d="M10 8.5v7M14 8.5v7"/>'
I["play"] = '<circle cx="12" cy="12" r="9"/><path d="M10 8.5l6 3.5-6 3.5z"/>'
I["flag"] = '<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>'

STORY_CSS = B.CSS.replace("height:1350px", "height:1920px") + """
.top{height:300px;align-items:flex-end;padding-bottom:30px}
.top img{height:78px}
.stag{display:flex;justify-content:center;margin:26px 0 30px}
.stag span{background:#0b2a6f;color:#fff;font:700 26px Inter;letter-spacing:.08em;padding:13px 28px;border-radius:999px;text-transform:uppercase}
h1{font-size:84px} h2{font-size:74px}
.lead{font-size:34px}
.cards{gap:22px;margin-top:44px}
.h{font-size:42px}.p{font-size:32px;line-height:1.4}.card{padding:36px 38px}.chk{font-size:34px;padding:30px 32px}.chk .ok{width:60px;height:60px}.note{font-size:29px;padding:24px 30px}
.cta{position:absolute;left:80px;right:80px;bottom:250px;display:flex;flex-direction:column;align-items:center;gap:22px}
.cta .b{background:#0b2a6f;color:#fff;font:700 36px Poppins;padding:26px 44px;border-radius:999px;text-align:center;box-shadow:0 18px 40px rgba(11,42,111,.25)}
.cta .t{font:400 30px Inter;color:#4b5563}.cta .t b{color:#1d4ed8}
.num{flex:none;width:92px;height:92px;border-radius:28px;background:#0b2a6f;color:#fff;font:800 46px Poppins;display:flex;align-items:center;justify-content:center}
"""


def story(tag, titulo, lead, corpo, cta):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{STORY_CSS}</style></head><body><div class="pg">'
            f'<div class="top"><img src="logo.png"></div><div class="stag"><span>{tag}</span></div>'
            f'<div class="tt"><h1>{titulo}</h1></div>' + (f'<div class="lead">{lead}</div>' if lead else '') + corpo +
            f'</div><div class="cta"><div class="b">{cta}</div><div class="t">Feito para a <b>rotina real</b> da advocacia.</div></div></body></html>')


def passo(n, titulo, texto, cor="azul"):
    c = COR[cor][0]
    return (f'<div class="card"><div class="num" style="background:{c}">{n}</div><div class="ct">'
            f'<div class="h" style="color:{c}">{titulo}</div><div class="p">{texto}</div></div></div>')


ST = {}
ST["2026-11-23_0900_story_dica-dias-uteis"] = story("Dica · Prazos", "Prazo em dias úteis:<br><em>conte certo.</em>",
    "Para prazos processuais no CPC:", '<div class="cards">' +
    passo(1, "O dia da publicação não conta", "Exclui-se o dia do começo e inclui-se o do vencimento (art. 224).") +
    passo(2, "Começa no 1º dia útil seguinte", "Se a publicação for na sexta, a contagem começa na segunda.") +
    passo(3, "Só dias úteis entram", "Sábados, domingos e feriados ficam de fora (art. 219).", "verde") + '</div>',
    "No LawNova, a data final já vem calculada")

ST["2026-11-23_1800_story_djen-disponibilizacao"] = story("Você sabia?", "No DJEN,<br>disponibilizar <em>não é</em><br>publicar.",
    "", '<div class="cards">' +
    card("calok", "azul", "qui 26/11 · Disponibilizada", "A intimação aparece no DJEN.") +
    card("doc", "roxo", "sex 27/11 · Publicada", "Considera-se publicada no 1º dia útil seguinte.") +
    card("clock", "verde", "seg 30/11 · Prazo começa", "A contagem inicia no 1º dia útil após a publicação.") +
    '</div><div class="note">' + ico("scale", "azul", 60, 36) + 'Base: Lei 11.419/2006, art. 4º, §§ 3º e 4º.</div>',
    "Prazo já calculado no LawNova")

ST["2026-11-24_0900_story_erro-feriado-local"] = story("Erro comum", "Esqueceu o<br><em>feriado local?</em>",
    "Feriado municipal ou estadual e dia sem expediente forense também ficam fora da contagem.", '<div class="cards">' +
    card("cal", "azul", "Confira o calendário do tribunal", "Cada tribunal publica seus feriados e dias sem expediente.") +
    card("alert", "verm", "No recurso, comprove", "O feriado local deve ser comprovado no ato da interposição (CPC, art. 1.003, § 6º).") +
    card("check", "verde", "Registre no seu controle", "Assim o vencimento fica certo para toda a equipe.") + '</div>',
    "Prazos e tarefas num lugar só: LawNova")

ST["2026-11-24_1800_story_checklist-recesso"] = story("Antes do recesso", "Checklist para<br><em>fechar o ano.</em>",
    "Os prazos ficam suspensos de 20/12/2026 a 20/01/2027 (CPC, art. 220).", '<div class="cards" style="gap:16px">' +
    check("<b>Mapeie o que vence até 19/12</b> em todos os processos.") +
    check("<b>Protocole antes do dia 20</b> o que já estiver pronto.") +
    check("<b>Prazos em curso param em 20/12</b> e voltam em 21/01 com o saldo restante.") +
    check("<b>Urgência no recesso?</b> O caminho é o plantão judiciário.") + '</div>',
    "Veja tudo o que vence no LawNova")

ST["2026-11-25_0900_story_planilha-x-sistema"] = story("Comparativo", "Planilha<br>× <em>sistema.</em>", "",
    '<div style="display:flex;gap:22px;margin-top:44px">'
    '<div class="card" style="flex:1;flex-direction:column;align-items:flex-start;gap:14px;padding:34px 30px">' + ico("sheet", "verm", 92, 54) +
    '<div class="h" style="color:#c2410c">Planilha</div>' + "".join(
        f'<div class="p" style="display:flex;gap:12px;align-items:flex-start"><span style="color:#c2410c;font-weight:800">✕</span>{t}</div>' for t in
        ["Você digita cada intimação", "Conta o prazo na mão", "Ninguém é avisado", "Uma versão por pessoa"]) + '</div>'
    '<div class="card" style="flex:1;flex-direction:column;align-items:flex-start;gap:14px;padding:34px 30px;border:3px solid #1d4ed8">' + ico("spark", "azul", 92, 54) +
    '<div class="h" style="color:#1d4ed8">LawNova</div>' + "".join(
        f'<div class="p" style="display:flex;gap:12px;align-items:flex-start"><span style="color:#15803d;font-weight:800">✓</span>{t}</div>' for t in
        ["Movimentações chegam sozinhas", "Data final calculada", "Tarefa com responsável", "Equipe na mesma tela"]) + '</div></div>',
    "Teste o LawNova por 7 dias")

ST["2026-11-25_1800_story_pergunta-horas"] = story("Pergunta rápida", "Quantas horas<br>por semana você<br>gasta <em>caçando<br>intimação?</em>", "",
    '<div class="cards" style="gap:18px;margin-top:60px">' + "".join(
        f'<div class="card" style="justify-content:center;padding:34px"><div class="h" style="color:#0b2a6f;margin:0;font-size:46px">{t}</div></div>' for t in
        ["Menos de 1 hora", "De 1 a 3 horas", "Mais de 3 horas"]) +
    '</div><div class="note" style="margin-top:34px;justify-content:center">' + ico("msg", "azul", 60, 36) + 'Responda aqui no direct.</div>',
    "Com o LawNova, essa resposta é zero")

_PRAZO_INTERNO = story("Dica · Gestão", "Prazo interno<br>× <em>prazo fatal.</em>", "",
    '<div class="cards">' +
    card("flag", "verm", "Prazo fatal", "O último dia previsto em lei para praticar o ato.") +
    card("user", "azul", "Prazo interno", "A data em que a peça fica pronta dentro do escritório, para revisar com calma.") +
    card("check", "verde", "Na prática", "Defina o interno 2 a 3 dias úteis antes do fatal e dê um responsável para cada um.") + '</div>',
    "Tarefas com dono e prazo no LawNova")

ST["2026-11-26_0900_story_bastidor-ia"] = story("Bastidor", "Como a IA separa<br><em>decisão</em> de andamento.", "", '<div class="cards" style="gap:18px">' +
    passo(1, "Lê a movimentação", "O texto chega do tribunal ou do diário oficial.") +
    passo(2, "Entende o tipo de ato", "Sentença, decisão, despacho, juntada…", "roxo") +
    passo(3, "Se precisar, lê o processo inteiro", "Para entender o contexto antes de sugerir algo.", "verde") +
    passo(4, "Separa e sugere", "Decisão ganha destaque e próximo passo; andamento fica no histórico.", "verm") + '</div>',
    "Central Processual com IA · LawNova")

_CHECK_SEXTA = story("Checklist de sexta", "Antes do<br><em>fim de semana:</em>", "", '<div class="cards" style="gap:16px">' +
    check("<b>Confira o que vence segunda e terça.</b>") +
    check("<b>Leia as movimentações</b> que ainda não foram vistas.") +
    check("<b>Distribua as tarefas</b> da próxima semana, cada uma com responsável.") +
    check("<b>Desligue</b> sabendo que nada ficou para trás.") + '</div>',
    "Tudo isso numa tela: LawNova")

_DEZEMBRO = story("Dezembro chegando", "Comece dezembro<br><em>organizado.</em>",
    "Recesso, festas e prazos vencendo antes do dia 20. Dezembro é o mês em que mais coisa escapa.", '<div class="cards">' +
    card("badge", "azul", "Movimentações pela OAB", "Chegam sozinhas, de tribunais e diários oficiais.") +
    card("cal", "verde", "Prazos calculados", "Com a data final em dias úteis.") +
    card("users", "roxo", "Tarefas com responsável", "A equipe sabe o que fazer primeiro.") + '</div>',
    "Teste o LawNova por 7 dias · link na bio")


# ---------------- feeds (1080x1350) ----------------
FEED_XCSS = ".h{font-size:41px}.p{font-size:30px;line-height:1.4}.card{padding:34px 36px}.cards{gap:24px;margin-top:44px}.note{font-size:27px}"
def fslide(n, total, corpo, seta=True, src=""):
    B.TOTAL = total
    return B.slide(n, corpo, seta, src).replace("</style>", FEED_XCSS + "</style>", 1)

REC = {}
T = 7
REC[1] = fslide(1, T, """
<div style="margin-top:30px"><span class="tag">Guia rápido · fim de ano</span></div>
<div class="tt"><h1>Recesso forense:<br>o que <em>suspende</em><br>e o que não.</h1></div>
<div class="lead">Datas de <b>2026/2027</b>, o que para, o que continua correndo e como fica a contagem dos prazos.</div>
<div style="display:flex;gap:20px;margin-top:80px">""" + "".join(
    f'<div class="card" style="flex:1;flex-direction:column;align-items:flex-start;gap:10px;padding:40px 30px"><div class="h" style="color:{c};font-size:62px">{d}</div><div class="p">{t}</div></div>'
    for d, t, c in [("20/12", "começa a suspensão", "#1d4ed8"), ("06/01", "fim do recesso", "#6d28d9"), ("21/01", "prazos voltam", "#15803d")]) + "</div>",
    src="Fontes: CPC art. 220 · CLT art. 775-A · CPP art. 798-A · Lei 5.010/1966 · Res. CNJ 244/2016")
REC[2] = fslide(2, T, f"""
<div class="tt" style="margin-top:20px"><h2>As datas<br><em>que importam.</em></h2></div>
<div class="cards">
{card("cal","roxo","20/12 a 06/01 · Recesso","Expediente suspenso. Tribunais funcionam em plantão para urgências.")}
{card("pause","azul","20/12 a 20/01 · Prazos suspensos","Vale para prazos processuais (CPC, art. 220, \"inclusive\").")}
{card("play","verde","21/01/2027 · Prazos voltam","A contagem retoma no 1º dia útil seguinte, com o saldo que restava.")}
</div>""")
REC[3] = fslide(3, T, f"""
<div class="tt" style="margin-top:20px"><h2>O que fica<br><em>suspenso.</em></h2></div>
<div class="cards">
{card("doc","azul","Prazos processuais cíveis","CPC, art. 220: de 20 de dezembro a 20 de janeiro, inclusive.")}
{card("users","roxo","Audiências e sessões","Não são realizadas no período (CPC, art. 220, § 2º).")}
{card("build","verde","Justiça do Trabalho","Mesma suspensão de prazos, audiências e sessões (CLT, art. 775-A).")}
{card("scale","verm","Processo penal","Prazos também suspensos (CPP, art. 798-A), com exceções. Veja a próxima.")}
</div>""")
REC[4] = fslide(4, T, f"""
<div class="tt" style="margin-top:20px"><h2>O que <em>não para.</em></h2></div>
<div class="cards" style="gap:16px;margin-top:30px">
{card("alert","verm","Réus presos","E os processos vinculados a essas prisões (CPP, art. 798-A, I).")}
{card("users","roxo","Lei Maria da Penha","Procedimentos da Lei 11.340/2006 (CPP, art. 798-A, II).")}
{card("bell","azul","Medidas urgentes","Com despacho fundamentado do juiz, e o plantão judiciário para urgências.")}
{card("clock","verde","Prescrição e decadência","São prazos de direito material: não entram na suspensão processual.")}
</div>""")
REC[5] = fslide(5, T, f"""
<div class="tt" style="margin-top:20px"><h2>Como fica<br><em>a contagem.</em></h2></div>
<div class="cards">
{card("pause","azul","Prazo já em curso","Para em 20/12 e volta em 21/01, contando apenas o saldo que faltava.")}
{card("calok","verde","Intimação durante a suspensão","O prazo só começa a correr depois de 20/01.")}
</div>
<div class="note" style="margin-top:26px;flex-direction:column;align-items:flex-start;gap:6px">
<div style="font:700 28px Poppins;color:#0b2a6f">Exemplo</div>
<div style="font:500 26px/1.45 Inter;color:#1f2937">Prazo de 15 dias úteis com 10 já corridos até 19/12: os <b>5 dias restantes</b> contam a partir de 21/01/2027.</div></div>""")
REC[6] = fslide(6, T, f"""
<div class="tt" style="margin-top:20px"><h2>Atenção aos<br><em>tribunais superiores.</em></h2></div>
<div class="lead">STF, STJ e TST têm férias coletivas em janeiro e costumam ampliar o período de suspensão.</div>
<div class="cards">
{card("landmark","azul","Confira o ato de cada tribunal","Datas e exceções podem variar. O ato oficial do tribunal é o que vale.")}
{card("doc","roxo","Tribunais estaduais e federais","Também publicam portarias próprias sobre recesso, plantão e expediente.")}
{card("check","verde","Registre tudo antes do dia 20","Assim nenhum prazo some no meio das festas.")}
</div>""")
REC[7] = fslide(7, T, """
<div class="tt" style="margin-top:40px"><h1 style="font-size:80px">Feche o ano<br>sabendo <em>o que vence.</em></h1></div>
<div class="lead">Tudo o que vence, num lugar só:</div><div class="cards" style="gap:14px;margin-top:40px">""" + "".join(check(t) for t in ["<b>Movimentações</b> chegam pela sua OAB", "<b>IA</b> analisa e separa o que é decisão", "<b>Prazos</b> calculados em dias úteis", "<b>Tarefas</b> com responsável"]) + """</div>
<div style="margin-top:36px;background:linear-gradient(90deg,#1d4ed8,#0b2a6f);border-radius:32px;padding:38px 44px;color:#fff">
 <div style="font:700 40px/1.25 Poppins">Teste o LawNova por 7 dias.</div><div style="font:500 28px Inter;margin-top:10px;opacity:.9">Link na bio · salve este guia</div></div>""", seta=False)

OAB = {1: fslide(1, 1, f"""
<div style="margin-top:20px"><span class="tag">Central Processual</span></div>
<div class="tt"><h1>Seu número<br>da OAB <em>já basta.</em></h1></div>
<div class="lead">As movimentações dos seus processos, de tribunais e diários oficiais, chegam sozinhas. <b>Sem configurar nada.</b></div>
<div style="display:flex;align-items:center;gap:22px;margin-top:80px">
 <div class="card" style="flex:none;flex-direction:column;align-items:flex-start;gap:6px;padding:28px 30px;border:3px solid #1d4ed8">{ico("badge","azul",84,50)}
  <div style="font:600 22px Inter;color:#6b7280;letter-spacing:.06em;margin-top:10px">SUA OAB</div><div style="font:800 40px Poppins;color:#0b2a6f">OAB/SC 12.345</div></div>
 <svg width="70" height="40" viewBox="0 0 70 40"><path d="M4 20h58M46 6l16 14-16 14" fill="none" stroke="#1d4ed8" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>
 <div style="flex:1;display:flex;flex-direction:column;gap:12px">""" + "".join(
    f'<div class="card" style="padding:16px 20px;gap:16px;border-radius:20px"><span style="font:800 18px Inter;color:#0b2a6f;background:#e8efff;border-radius:10px;padding:8px 10px">{t}</span><span style="font:700 28px Poppins;color:#1f2937">{m}</span></div>'
    for t, m in [("TJSC", "Sentença"), ("TRT9", "Intimação"), ("DJEN", "Despacho"), ("TJPR", "Juntada")]) + "</div></div>"
    + '<div style="margin-top:56px;background:linear-gradient(90deg,#1d4ed8,#0b2a6f);border-radius:32px;padding:32px 40px;color:#fff;display:flex;align-items:center;gap:20px">'
    + '<div style="flex:1"><div style="font:700 36px/1.25 Poppins">A IA analisa e o prazo sai calculado.</div><div style="font:500 26px Inter;margin-top:8px;opacity:.9">Teste o LawNova por 7 dias · link na bio</div></div></div>', seta=False)}

ERR = {}
T = 7
ERR[1] = fslide(1, T, f"""
<div style="margin-top:30px"><span class="tag">Prazos · cuidado</span></div>
<div class="tt"><h1>5 erros que<br>fazem o advogado<br><em>perder prazo.</em></h1></div>
<div class="lead">E como evitar cada um, com a base legal.</div>
<div style="display:flex;gap:16px;margin-top:60px;flex-wrap:wrap">""" + "".join(
    f'<div style="width:150px;height:150px;border-radius:36px;background:#0b2a6f;color:#fff;font:800 80px Poppins;display:flex;align-items:center;justify-content:center;box-shadow:0 18px 36px rgba(11,42,111,.22)">{i}</div>' for i in range(1, 6)) + "</div>")
def erro(n, titulo, errado, certo, base):
    return fslide(n + 1, T, f"""<style>.h{{font-size:46px}}.p{{font-size:34px}}.card{{padding:40px 40px}}</style>
<div style="position:absolute;right:40px;bottom:120px;font:900 520px/1 Poppins;color:#0b2a6f;opacity:.06">{n}</div>
<div style="margin-top:20px"><span class="tag">Erro {n} de 5</span></div>
<div class="tt"><h2>{titulo}</h2></div>
<div class="cards">
<div class="card">{ico("x","verm")}<div class="ct"><div class="h" style="color:#c2410c">O erro</div><div class="p">{errado}</div></div></div>
<div class="card">{ico("check","verde")}<div class="ct"><div class="h" style="color:#15803d">Como evitar</div><div class="p">{certo}</div></div></div>
</div><div class="note">{ico("scale","azul",60,36)}{base}</div>""")
ERR[2] = erro(1, "Contar o dia<br><em>da publicação.</em>", "Começar a contagem no próprio dia em que a intimação foi publicada.",
    "Exclua o dia do começo: o prazo inicia no 1º dia útil seguinte.", "CPC, art. 224")
ERR[3] = erro(2, "Confundir disponibilização<br>com <em>publicação.</em>", "Contar o prazo a partir do dia em que a intimação apareceu no DJEN.",
    "A publicação é o 1º dia útil após a disponibilização, e o prazo começa no dia útil seguinte.", "Lei 11.419/2006, art. 4º, §§ 3º e 4º")
ERR[4] = erro(3, "Esquecer o<br><em>feriado local.</em>", "Ignorar feriado municipal ou estadual, ou não comprová-lo no recurso.",
    "Confira o calendário do tribunal e comprove o feriado local no ato da interposição.", "CPC, art. 1.003, § 6º")
ERR[5] = erro(4, "Deixar para a<br><em>última hora.</em>", "Protocolar às 23h do último dia. Se o sistema cair, o risco é seu.",
    "Trabalhe com prazo interno, 2 a 3 dias úteis antes do fatal, para revisar com calma.", "A prorrogação por instabilidade depende de reconhecimento do tribunal")
ERR[6] = erro(5, "Prazo<br><em>sem dono.</em>", "Todo mundo viu a intimação, mas ninguém ficou responsável.",
    "Cada prazo vira uma tarefa com responsável, prioridade e data.", "Gestão de equipe · boa prática")
ERR[7] = fslide(7, T, """
<div class="tt" style="margin-top:40px"><h1 style="font-size:80px">Menos risco,<br>menos <em>planilha.</em></h1></div>
<div class="lead">No LawNova:</div><div class="cards" style="gap:14px;margin-top:40px">""" + "".join(check(t) for t in ["<b>Movimentações</b> chegam pela sua OAB", "<b>IA</b> analisa e separa o que é decisão", "<b>Prazos</b> calculados em dias úteis", "<b>Tarefas</b> com responsável"]) + """</div>
<div style="margin-top:36px;background:linear-gradient(90deg,#1d4ed8,#0b2a6f);border-radius:32px;padding:38px 44px;color:#fff">
 <div style="font:700 40px/1.25 Poppins">Teste o LawNova por 7 dias.</div><div style="font:500 28px Inter;margin-top:10px;opacity:.9">Link na bio · salve e compartilhe com a equipe</div></div>""", seta=False)

FEEDS = {"2026-11-24_1000_carrossel_recesso-forense": REC, "2026-11-25_1000_feed_oab-ja-basta": OAB, "2026-11-26_1000_carrossel_5-erros-prazo": ERR}

from blackfriday import BF_STORIES, BF_FEED
ST.update(BF_STORIES)
FEEDS.update(BF_FEED)

if __name__ == "__main__":
    so = sys.argv[1:]
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        for nome, html in ST.items():
            if so and not any(s in nome for s in so): continue
            f = D / f"_{nome}.html"; f.write_text(html, encoding="utf-8"); pg.goto(f.as_uri()); pg.wait_for_timeout(200)
            pg.screenshot(path=str(OUT / f"{nome}.png"))
            bot = pg.evaluate("Math.max(...[...document.querySelectorAll('.pg > *')].map(e=>e.getBoundingClientRect().bottom))")
            print(nome, "conteúdo até", round(bot), "(cta começa ~", 1920 - 250 - 150, ")")
        pg.set_viewport_size({"width": 1080, "height": 1350})
        for nome, sl in FEEDS.items():
            if so and not any(s in nome for s in so): continue
            for n, html in sl.items():
                f = D / f"_{nome}_{n}.html"; f.write_text(html, encoding="utf-8"); pg.goto(f.as_uri()); pg.wait_for_timeout(200)
                pg.screenshot(path=str(OUT / f"{nome}_{n}.png"))
                bot = pg.evaluate("Math.max(...[...document.querySelectorAll('.cards,.note,.lead')].map(e=>e.getBoundingClientRect().bottom),0)")
                print(nome, n, "até", round(bot))
        b.close()
