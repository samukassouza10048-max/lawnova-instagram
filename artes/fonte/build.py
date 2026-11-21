"""Carrossel 6x1 (decisão Dino 12/11/2026) — 1080x1350, padrão LawNova."""
import pathlib, sys
from playwright.sync_api import sync_playwright

D = pathlib.Path(__file__).parent
TOTAL = 9

I = {  # ícones (traço), viewBox 24
 "cal": '<rect x="3" y="4.5" width="18" height="16" rx="2.5"/><path d="M3 9.5h18M8 2.5v4M16 2.5v4"/><path d="M7.5 13h2M11 13h2M14.5 13h2M7.5 16.5h2M11 16.5h2"/>',
 "calok": '<rect x="3" y="4.5" width="18" height="16" rx="2.5"/><path d="M3 9.5h18M8 2.5v4M16 2.5v4"/><path d="M8.5 15l2.5 2.5 4.5-5"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
 "users": '<circle cx="12" cy="8" r="3.2"/><circle cx="5.5" cy="9.5" r="2.4"/><circle cx="18.5" cy="9.5" r="2.4"/><path d="M6.5 20v-1.5a5.5 5.5 0 0 1 11 0V20"/><path d="M1.5 19v-1a4 4 0 0 1 4.5-4M22.5 19v-1a4 4 0 0 0-4.5-4"/>',
 "doc": '<path d="M14 2.5H6.5A2 2 0 0 0 4.5 4.5v15a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V8z"/><path d="M14 2.5V8h5.5M8 12.5h8M8 16h8M8 9h3"/>',
 "hand": '<path d="M11 17l2 2a1.4 1.4 0 0 0 2-2l-1-1"/><path d="M14 16l2.5 2.5a1.4 1.4 0 0 0 2-2L15 13"/><path d="M15 13l2 2a1.4 1.4 0 0 0 2-2l-4.5-4.5L12 11a1.6 1.6 0 0 1-2.2-2.2L13 5.5"/><path d="M2.5 11.5L6 8l3 1M21.5 11.5l-3-3"/><path d="M6.5 12.5l4 4a1.4 1.4 0 0 1-2 2l-4-4"/>',
 "coins": '<ellipse cx="12" cy="6" rx="7" ry="2.8"/><path d="M5 6v4c0 1.5 3.1 2.8 7 2.8s7-1.3 7-2.8V6"/><path d="M5 10v4c0 1.5 3.1 2.8 7 2.8s7-1.3 7-2.8v-4"/><path d="M5 14v4c0 1.5 3.1 2.8 7 2.8s7-1.3 7-2.8v-4"/>',
 "chart": '<path d="M3 21h18"/><rect x="5" y="13" width="3" height="6" rx=".6"/><rect x="10.5" y="9" width="3" height="10" rx=".6"/><rect x="16" y="5" width="3" height="14" rx=".6"/>',
 "gavel": '<path d="M13.5 4.5l6 6M11 7l6 6M15.5 2.5l6 6-2.5 2.5-6-6z"/><path d="M12.5 8.5L4 17a1.8 1.8 0 0 0 2.5 2.5l8.5-8.5"/><path d="M3 22h9"/>',
 "build": '<path d="M3 21h18M5 21V8l7-4 7 4v13"/><path d="M9 21v-5h6v5M9 11h.01M12 11h.01M15 11h.01"/>',
 "landmark": '<path d="M3 21h18M4 10h16M12 3l8.5 5h-17z"/><path d="M6 10v8M10 10v8M14 10v8M18 10v8"/>',
 "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 "alert": '<path d="M12 3l9.5 17h-19z"/><path d="M12 10v4.5M12 17.5h.01"/>',
 "repeat": '<path d="M17 2.5l3.5 3.5L17 9.5"/><path d="M3.5 11.5V10a4 4 0 0 1 4-4h13"/><path d="M7 21.5L3.5 18 7 14.5"/><path d="M20.5 12.5V14a4 4 0 0 1-4 4h-13"/>',
 "star": '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
}
COR = {"azul": ("#1d4ed8", "#e8efff"), "verde": ("#15803d", "#e6f6ec"), "verm": ("#c2410c", "#fdeee6"),
       "roxo": ("#6d28d9", "#efe9fd"), "marinho": ("#0b2a6f", "#e6ecf7")}


def ico(nome, cor="azul", tam=96, s=58):
    c, bg = COR[cor]
    return (f'<div class="ico" style="width:{tam}px;height:{tam}px;background:{bg}">'
            f'<svg viewBox="0 0 24 24" width="{s}" height="{s}" fill="none" stroke="{c}" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round">{I[nome]}</svg></div>')


def card(icone, cor, titulo, texto, extra=""):
    c = COR[cor][0]
    return (f'<div class="card {extra}">{ico(icone, cor)}<div class="ct">'
            f'<div class="h" style="color:{c}">{titulo}</div><div class="p">{texto}</div></div></div>')


def check(texto):
    return f'<div class="chk"><div class="ok">{I_CHECK}</div><div>{texto}</div></div>'


I_CHECK = '<svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;font-family:Inter,sans-serif;color:#1f2937;overflow:hidden;
 background:radial-gradient(120% 70% at 100% 0%,#dfe8fb 0%,rgba(223,232,251,0) 60%),
 radial-gradient(90% 60% at 0% 100%,#e4ebf9 0%,rgba(228,235,249,0) 60%),#f5f7fc}
.pg{position:absolute;inset:0;padding:0 80px}
.top{height:150px;display:flex;align-items:center;justify-content:center}
.top img{height:62px}
.tag{display:inline-block;background:#0b2a6f;color:#fff;font:700 21px Inter;letter-spacing:.06em;
 padding:10px 22px;border-radius:999px;text-transform:uppercase;margin-bottom:26px}
.tt{position:relative;padding-left:46px}
.tt:before{content:"";position:absolute;left:0;top:8px;bottom:8px;width:12px;border-radius:6px;
 background:linear-gradient(#0b2a6f,#1d4ed8)}
h1{font:800 76px/1.04 Poppins;color:#0b2a6f;letter-spacing:-.02em}
h1 em{font-style:normal;color:#1d4ed8}
h2{font:800 62px/1.07 Poppins;color:#0b2a6f;letter-spacing:-.02em}
h2 em{font-style:normal;color:#1d4ed8}
.lead{font:400 31px/1.42 Inter;color:#374151;margin:22px 0 0 46px}
.lead b{color:#0b2a6f}
.cards{display:flex;flex-direction:column;gap:20px;margin-top:38px}
.card{display:flex;align-items:center;gap:30px;background:rgba(255,255,255,.92);border:1.5px solid #dfe6f3;
 border-radius:28px;padding:30px 34px;box-shadow:0 10px 30px rgba(11,42,111,.07)}
.card.hl{background:#0b2a6f;border-color:#0b2a6f}
.card.hl .h,.card.hl .p{color:#fff!important}
.ico{flex:none;border-radius:24px;display:flex;align-items:center;justify-content:center}
.ct{flex:1}
.h{font:700 38px/1.15 Poppins;margin-bottom:6px;letter-spacing:-.01em}
.p{font:400 28px/1.38 Inter;color:#374151}
.p b{color:#111827;font-weight:700}
.note{margin-top:20px;display:flex;align-items:center;gap:18px;background:#e8efff;border-radius:22px;
 padding:20px 28px;font:600 25px/1.35 Inter;color:#0b2a6f}
.chk{display:flex;align-items:center;gap:24px;background:rgba(255,255,255,.92);border:1.5px solid #dfe6f3;
 border-radius:24px;padding:22px 28px;font:500 27px/1.35 Inter;color:#1f2937}
.chk b{color:#0b2a6f}
.ok{flex:none;width:52px;height:52px;border-radius:50%;background:#15803d;display:flex;align-items:center;justify-content:center}
.foot{position:absolute;left:80px;right:80px;bottom:44px;display:flex;align-items:center;gap:24px;
 font:400 24px Inter;color:#4b5563}
.foot img{height:40px}
.foot .sep{width:2px;height:36px;background:#c7d0e0}
.foot b{color:#1d4ed8;font-weight:700}
.foot .n{margin-left:auto;font:600 22px Inter;color:#6b7280}
.foot .arr{width:52px;height:52px;border-radius:50%;border:2.5px solid #0b2a6f;display:flex;align-items:center;justify-content:center}
.src{position:absolute;left:80px;right:80px;bottom:118px;font:400 19px Inter;color:#6b7280}
"""
ARR = '<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="#0b2a6f" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5l7 7-7 7"/></svg>'


def foot(n, seta=True):
    return (f'<div class="foot"><img src="logo.png"><div class="sep"></div>'
            f'<div>Feito para a <b>rotina real</b> da advocacia.</div><div class="n">{n}/{TOTAL}</div>'
            + (f'<div class="arr">{ARR}</div>' if seta else '') + '</div>')


def slide(n, corpo, seta=True, src=""):
    s = f'<div class="src">{src}</div>' if src else ""
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="pg">'
            f'<div class="top"><img src="logo.png"></div>{corpo}</div>{s}{foot(n, seta)}</body></html>')


# ---------- ilustração da capa: calendário 6x1 -> 5x2 ----------
CAPA_ILU = """
<div style="position:relative;height:430px;margin-top:40px">
 <div style="position:absolute;left:150px;top:30px;width:640px;height:370px;border-radius:40px;background:linear-gradient(160deg,#ffffff,#e9f0ff);
   border:2px solid #d5def0;box-shadow:0 30px 60px rgba(11,42,111,.16)">
   <div style="height:92px;border-radius:38px 38px 0 0;background:linear-gradient(90deg,#1d4ed8,#0b2a6f)"></div>
   <div style="position:absolute;top:-34px;left:0;right:0;display:flex;justify-content:space-around;padding:0 90px">
     <div style="width:26px;height:74px;border-radius:13px;background:#0b2a6f;border:5px solid #fff"></div>
     <div style="width:26px;height:74px;border-radius:13px;background:#0b2a6f;border:5px solid #fff"></div>
     <div style="width:26px;height:74px;border-radius:13px;background:#0b2a6f;border:5px solid #fff"></div>
   </div>
 </div>
 <div style="position:absolute;left:40px;top:150px;width:330px;height:200px;border-radius:30px;background:#e2e9f8;border:2px solid #c9d5ee;
   display:flex;align-items:center;justify-content:center;font:800 120px Poppins;color:#7b8db5;box-shadow:0 18px 40px rgba(11,42,111,.12)">
   6x1
   <svg style="position:absolute" width="230" height="160" viewBox="0 0 230 160"><path d="M20 20L210 140M210 20L20 140" stroke="#dc2626" stroke-width="14" stroke-linecap="round"/></svg>
 </div>
 <svg style="position:absolute;left:360px;top:205px" width="180" height="110" viewBox="0 0 180 110"><path d="M10 80 C60 95 110 80 150 40" fill="none" stroke="#15803d" stroke-width="14" stroke-linecap="round"/><path d="M118 34 L156 34 L152 72" fill="none" stroke="#15803d" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/></svg>
 <div style="position:absolute;left:530px;top:130px;width:380px;height:230px;border-radius:32px;background:linear-gradient(160deg,#ffffff,#eafaf0);border:3px solid #86d3a4;
   display:flex;align-items:center;justify-content:center;font:800 140px Poppins;color:#15803d;box-shadow:0 24px 50px rgba(21,128,61,.18)">5x2</div>
 <svg style="position:absolute;left:880px;top:60px" width="90" height="90" viewBox="0 0 90 90"><path d="M20 70L36 40M48 78L78 50M52 30L64 8" stroke="#15803d" stroke-width="9" stroke-linecap="round"/></svg>
</div>"""

S = {}
S[1] = slide(1, f"""
<div style="margin-top:20px"><span class="tag">STF · Liminar de 12/11/2026</span></div>
<div class="tt"><h1>Escala 6x1:<br>o que Flávio Dino<br><em>decidiu?</em></h1></div>
<div class="lead">O STF <b>manteve o início da nova jornada em 16/12/2026</b> e definiu as regras da transição para a escala 5x2.</div>
{CAPA_ILU}
""", src="ADIs 8.041 e 8.042 (CNC e CNI) · decisão monocrática, ainda será analisada pelo Plenário")

S[2] = slide(2, f"""
<div class="tt" style="margin-top:20px"><h2>O prazo <em>não</em><br>foi adiado.</h2></div>
<div class="lead">CNC e CNI pediram mais tempo. O ministro negou e manteve o cronograma da EC 141/2026.</div>
<div class="cards">
{card("cal","azul","16 de dezembro de 2026","Jornada máxima cai de <b>44h para 42h</b> semanais.")}
{card("calok","verde","2 repousos semanais remunerados","Garantidos desde o início da nova jornada (escala 5x2).")}
{card("clock","roxo","Até 15/12/2027","Fase intermediária, com as regras de transição.")}
{card("chart","verm","16/12/2027: 40h semanais","Próxima etapa da redução. Falta de acordo <b>não antecipa</b> essa fase.")}
</div>
""")

S[3] = slide(3, f"""
<div class="tt" style="margin-top:20px"><h2>E se não houver<br><em>acordo coletivo?</em></h2></div>
<div class="lead">Sem acordo ou convenção coletiva até <b>15/12/2026</b>, vale a regra de transição:</div>
<div class="cards">
{card("users","azul","5 dias de trabalho","As 42 horas podem ser distribuídas em cinco dias na semana.")}
{card("clock","verde","Até 8h24 por dia","Limite diário, sempre respeitando o teto de 42h semanais.")}
{card("coins","verm","Sem hora extra nos 24 minutos","Os 24 minutos além da 8ª hora <b>não</b> recebem adicional de hora extra.")}
</div>
<div class="note">{ico("calok","azul",60,36)}Regra válida só na fase intermediária: até 15/12/2027.</div>
""")

S[4] = slide(4, f"""
<div class="tt" style="margin-top:20px"><h2>Acordos coletivos:<br><em>90 dias</em> para ajustar.</h2></div>
<div class="cards">
{card("hand","azul","Prazo de 90 dias","A partir de 16/12/2026, sindicatos e empresas podem renegociar as contrapartidas de acordos e convenções.")}
{card("doc","verm","Cláusulas incompatíveis","Deixam de produzir efeitos em 16/12/2026. As demais seguem válidas até o fim da vigência.")}
{card("alert","roxo","Sem renegociação?","Nenhuma das partes pode cancelar ou alterar sozinha o que foi pactuado.")}
{card("gavel","marinho","Conflitos","Divergências podem ser levadas à <b>Justiça do Trabalho</b>.")}
</div>
""")

S[5] = slide(5, f"""
<div class="tt" style="margin-top:20px"><h2>Folgas e<br><em>compensação.</em></h2></div>
<div class="cards" style="gap:16px;margin-top:30px">
{card("repeat","azul","Regimes de compensação","Acordos e convenções podem definir quando as folgas acontecem, sem os limites semanais e mensais originais.")}
{card("calok","verde","2 repousos preservados","As duas folgas semanais remuneradas não podem ser suprimidas.")}
{card("star","verm","Setores citados","Comércio no fim de ano, agro na safra, turismo na alta temporada, embarcações e plataformas.")}
{card("landmark","roxo","Primeiros 90 dias","Se a negociação fracassar, 3 ministérios podem editar portaria conjunta com regras provisórias.")}
</div>
""")

S[6] = slide(6, f"""
<div class="tt" style="margin-top:20px"><h2>Salários e<br><em>remuneração.</em></h2></div>
<div class="lead">Menos horas de trabalho <b>não</b> autorizam corte de salário.</div>
<div class="cards">
{card("coins","azul","Sem redução salarial","O salário deve ser mantido mesmo com a jornada menor.")}
{card("chart","verde","Pisos preservados","Os pisos salariais das categorias também precisam ser mantidos.")}
{card("users","verm","Equiparação salarial","Manter o salário de quem teve a jornada reduzida, por si só, não justifica equiparação com contratados em outras condições.")}
</div>
""")

S[7] = slide(7, f"""
<div class="tt" style="margin-top:20px"><h2>Congresso, empresas<br>e <em>setor público.</em></h2></div>
<div class="cards">
{card("landmark","azul","180 dias para o Congresso","Regulamentar regimes diferenciados (comércio, turismo, operação contínua), sem retirar a redução nem as 2 folgas.")}
{card("build","verde","Micro e pequenas empresas","Pedido de suspensão negado. Congresso tem 180 dias para criar regras de adaptação.")}
{card("doc","verm","Contratos com o poder público","Prazo de adaptação caiu de 1 ano para 180 dias da EC, inclusive licitações em curso.")}
{card("star","roxo","Hipersuficientes","Exceção (diploma + salário de 2,5x o teto do INSS) estendida a estatais em regime concorrencial.")}
</div>
""")

S[8] = slide(8, f"""
<div class="tt" style="margin-top:20px"><h2>O que o advogado<br>trabalhista precisa<br><em>fazer agora?</em></h2></div>
<div class="cards" style="gap:16px;margin-top:34px">
{check("<b>Revisar acordos e convenções</b> e mapear cláusulas incompatíveis com a nova jornada.")}
{check("<b>Preparar a renegociação</b> dentro dos 90 dias a partir de 16/12/2026.")}
{check("<b>Reestruturar escalas e banco de horas</b> para 42h em 5 dias.")}
{check("<b>Orientar clientes</b> sobre a regra de 8h24 sem acordo coletivo.")}
{check("<b>Controlar os prazos</b> de 15/12/2026, 90 dias e 180 dias.")}
</div>
<div class="note" style="margin-top:18px">{ico("gavel","azul",60,36)}A liminar ainda será analisada pelo Plenário do STF.</div>
""")

S[9] = slide(9, f"""
<div class="tt" style="margin-top:30px"><h1 style="font-size:84px">Decisão do STF<br>sobre o fim da<br><em>escala 6x1.</em></h1></div>
<div class="cards" style="margin-top:44px">
{card("cal","azul","42h a partir de 16/12","Com 2 repousos semanais remunerados.")}
{card("hand","verde","90 dias para renegociar","Acordos e convenções coletivas.")}
{card("gavel","roxo","Plenário vai analisar","A liminar tem efeito imediato.")}
</div>
<div style="margin-top:34px;background:linear-gradient(90deg,#1d4ed8,#0b2a6f);border-radius:32px;padding:34px 44px;display:flex;align-items:center;gap:30px;color:#fff">
 <div style="flex:1;font:700 36px/1.25 Poppins">Organize prazos, clientes e tarefas do escritório no LawNova.<div style="font:500 26px Inter;margin-top:8px;opacity:.9">Teste por 7 dias · link na bio</div></div>
 <div style="width:84px;height:84px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center"><svg viewBox="0 0 24 24" width="40" height="40" fill="none" stroke="#1d4ed8" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5l7 7-7 7"/></svg></div>
</div>
""", seta=False)

if __name__ == "__main__":
    so = [int(x) for x in sys.argv[1:]] or list(S)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for n in so:
            f = D / f"s{n}.html"; f.write_text(S[n], encoding="utf-8")
            pg.goto(f.as_uri()); pg.wait_for_timeout(250)
            pg.screenshot(path=str(D / f"s{n}.png"))
            # checagem de transbordo
            h = pg.evaluate("Math.max(...[...document.querySelectorAll('.cards,.note,.lead')].map(e=>e.getBoundingClientRect().bottom))")
            print(n, "conteúdo até y=", round(h))
        b.close()
