# Fila de publicação do Instagram — @lawnova.oficial

Publicação automática no Instagram usando a **API oficial do Instagram**, sem Metricool.
Tudo roda de graça no GitHub Actions.

## Como funciona

1. **Criar o post:** o Claude coloca uma pasta em `fila/` com a imagem (JPG) e o `post.json`.
2. **Revisão:** o robô abre uma *issue* com a prévia, a data, o horário e a legenda. Você recebe aviso por e-mail ou no app do GitHub.
3. **Aprovar:** comente `aprovado` na issue (ou adicione a etiqueta **aprovado**).
   Para cancelar, comente `cancelar` ou feche a issue. Só o dono do repositório consegue aprovar.
4. **Publicar:** a cada 15 minutos o robô publica o que estiver aprovado e com o horário já vencido.
   O post vai para `publicados/AAAA-MM/`, e a issue recebe o link e é fechada.

Nada é publicado sem aprovação.

## Formato de um post

```
fila/2026-11-16_0900_story_calendario/
├── 1.jpg          # JPG obrigatório (o Instagram não aceita PNG pela API)
└── post.json
```

```json
{
  "quando": "2026-11-16T09:00:00-03:00",
  "tipo": "STORY",
  "titulo": "Calendário",
  "legenda": "",
  "midia": ["1.jpg"],
  "aprovado": false
}
```

Em vez de colocar a imagem na pasta, dá para mandar o link de exportação (ex.: Canva) em `"baixar": ["https://..."]`.
O robô baixa, converte para JPG e preenche `midia` sozinho. O link precisa estar válido na hora do envio.

**Tipos:**
- `FEED`: 1 imagem, 1080×1350
- `CARROSSEL`: 2 a 20 imagens
- `STORY`: 1 imagem ou vídeo, 1080×1920
- `REELS`: 1 vídeo mp4

## Segredos (Settings → Secrets and variables → Actions)

| Segredo | O que é |
|---|---|
| `IG_TOKEN` | Token de acesso **da Página do Facebook da LawNova** (ligada ao @lawnova.oficial), gerado no app "LawNova Publicador" do Meta for Developers. Token de Página gerado a partir de um token de usuário de longa duração **não expira**. |
| `GH_PAT` | (opcional) Token do GitHub com permissão de escrever *Secrets* neste repositório. É usado para gravar o token renovado. |

Se no futuro usarmos o login do Instagram (token de 60 dias), defina a variável `IG_API_HOST=https://graph.instagram.com`: o robô `renovar-token` passa a renovar toda segunda-feira.

## Limites

- 100 publicações por dia pela API do Instagram.
- O GitHub pode atrasar o agendamento em alguns minutos.
