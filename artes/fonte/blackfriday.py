"""Black Friday LawNova: 50% nos 3 primeiros meses para novas contratações. Fundo preto, destaque azul."""
import base64, pathlib

D = pathlib.Path(__file__).parent
# logo em branco para fundo escuro (o arquivo original é escuro): usamos o PNG num selo branco
LOGO = "logo.png"

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:%dpx;overflow:hidden;font-family:Inter,sans-serif;color:#fff;
 background:radial-gradient(90%% 55%% at 50%% 8%%,#16348f 0%%,rgba(22,52,143,0) 60%%),radial-gradient(70%% 40%% at 100%% 100%%,#1d4ed855 0%%,rgba(0,0,0,0) 70%%),#05070f}
.grid{position:absolute;inset:0;opacity:.18;background-image:linear-gradient(#3b82f6 1.5px,transparent 1.5px),linear-gradient(90deg,#3b82f6 1.5px,transparent 1.5px);
 background-size:90px 90px;-webkit-mask-image:radial-gradient(ellipse at 50%% 40%%,black 10%%,transparent 70%%)}
.pg{position:absolute;inset:0;padding:0 80px;display:flex;flex-direction:column;align-items:center;text-align:center}
.selo{background:#fff;border-radius:26px;padding:18px 30px;display:inline-flex}
.selo img{height:58px;display:block}
.bf{font:900 30px Inter;letter-spacing:.32em;color:#93c5fd;text-transform:uppercase}
.big{font:900 300px/0.86 Poppins;letter-spacing:-.06em;background:linear-gradient(180deg,#ffffff 30%%,#93c5fd 100%%);-webkit-background-clip:text;color:transparent;
 filter:drop-shadow(0 0 60px rgba(59,130,246,.55))}
.off{font:900 120px/1 Poppins;letter-spacing:-.03em;color:#3b82f6}
.sub{font:700 52px/1.15 Poppins;color:#fff;letter-spacing:-.01em}
.sub2{font:500 32px/1.4 Inter;color:#cbd5e1}
.pill{display:inline-block;background:#3b82f6;color:#fff;font:800 40px Poppins;padding:26px 50px;border-radius:999px;box-shadow:0 0 60px rgba(59,130,246,.6),0 0 140px rgba(59,130,246,.3)}
.lista{display:grid;grid-template-columns:1fr 1fr;gap:16px;width:100%%;text-align:left}
.it{display:flex;align-items:center;gap:16px;background:rgba(255,255,255,.06);border:1.5px solid rgba(147,197,253,.25);border-radius:22px;padding:20px 22px;font:600 27px/1.25 Inter;color:#e2e8f0}
.ck{flex:none;width:40px;height:40px;border-radius:50%%;background:#3b82f6;display:flex;align-items:center;justify-content:center}
.tag{display:inline-block;border:2px solid #93c5fd;color:#93c5fd;font:800 26px Inter;letter-spacing:.12em;padding:12px 26px;border-radius:999px}
.fine{font:400 22px Inter;color:#94a3b8}
.faixa{position:absolute;left:-40px;right:-40px;height:84px;background:#3b82f6;display:flex;align-items:center;overflow:hidden;transform:rotate(-4deg)}
.faixa span{white-space:nowrap;font:900 40px Poppins;color:#05070f;letter-spacing:.06em}
"""
CK = '<div class="ck"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></div>'
ITENS = ["Movimentações pela sua OAB", "IA que analisa e sugere", "Prazos calculados", "Tarefas com responsável", "Agenda e audiências", "Financeiro com Asaas"]
FAIXA = " · ".join(["BLACK FRIDAY"] * 12)


def page(h, corpo):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS % h}</style></head><body><div class="grid"></div>'
            f'<div class="pg">{corpo}</div></body></html>')


BF_STORIES = {
    # quinta 18h — aviso
    "2026-11-26_1800_story_bf-amanha": page(1920, f"""
<div style="margin-top:280px" class="selo"><img src="{LOGO}"></div>
<div class="bf" style="margin-top:110px">Amanhã · sexta 27/11</div>
<div class="sub" style="font-size:92px;line-height:1;margin-top:30px">Black Friday<br><span style="color:#3b82f6">LawNova</span></div>
<div style="margin-top:80px;display:flex;align-items:baseline;gap:20px"><div class="big" style="font-size:240px">50%</div><div class="off" style="font-size:96px">OFF</div></div>
<div class="sub2" style="margin-top:30px">nos 3 primeiros meses<br>para novas contratações</div>
<div style="margin-top:90px" class="tag">ATIVE O LEMBRETE · FIQUE DE OLHO</div>
<div class="fine" style="position:absolute;bottom:250px;left:80px;right:80px">Feito para a rotina real da advocacia.</div>"""),
    # sexta 9h — abertura
    "2026-11-27_0900_story_bf-abertura": page(1920, f"""
<div class="faixa" style="top:180px"><span>{FAIXA}</span></div>
<div style="margin-top:330px" class="selo"><img src="{LOGO}"></div>
<div class="bf" style="margin-top:70px">Começou a Black Friday LawNova</div>
<div style="margin-top:40px;display:flex;align-items:baseline;gap:20px"><div class="big">50%</div><div class="off">OFF</div></div>
<div class="sub" style="margin-top:20px">nos 3 primeiros meses</div>
<div class="sub2" style="margin-top:12px">para novas contratações</div>
<div class="lista" style="margin-top:56px">{''.join(f'<div class="it">{CK}{t}</div>' for t in ITENS)}</div>
<div style="margin-top:60px" class="pill">Garanta pelo link na bio</div>"""),
    # sexta 18h — última chamada
    "2026-11-27_1800_story_bf-ultima-chamada": page(1920, f"""
<div style="margin-top:280px" class="selo"><img src="{LOGO}"></div>
<div class="tag" style="margin-top:90px;border-color:#fb923c;color:#fb923c">AINDA DÁ TEMPO</div>
<div class="sub" style="font-size:86px;line-height:1.02;margin-top:40px">Seu escritório<br>organizado por<br><span style="color:#3b82f6">metade do preço.</span></div>
<div style="margin-top:60px;display:flex;align-items:baseline;gap:18px"><div class="big" style="font-size:210px">50%</div><div class="off" style="font-size:86px">OFF</div></div>
<div class="sub2" style="margin-top:20px">nos 3 primeiros meses · novas contratações</div>
<div style="margin-top:80px" class="pill">Garanta pelo link na bio</div>
<div class="fine" style="position:absolute;bottom:250px;left:80px;right:80px">Black Friday LawNova · feito para a rotina real da advocacia.</div>"""),
}

BF_FEED = {"2026-11-27_1000_feed_black-friday": {1: page(1350, f"""
<div class="faixa" style="top:60px"><span>{FAIXA}</span></div>
<div style="margin-top:200px" class="selo"><img src="{LOGO}"></div>
<div style="margin-top:34px;display:flex;align-items:baseline;gap:18px"><div class="big" style="font-size:250px">50%</div><div class="off" style="font-size:104px">OFF</div></div>
<div class="sub" style="margin-top:14px;font-size:50px">nos 3 primeiros meses do LawNova</div>
<div class="sub2" style="margin-top:8px">para novas contratações</div>
<div class="lista" style="margin-top:40px">{''.join(f'<div class="it" style="font-size:25px;padding:16px 20px">{CK}{t}</div>' for t in ITENS)}</div>
<div style="margin-top:40px" class="pill" >Garanta pelo link na bio</div>""")}}
