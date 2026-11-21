# Fontes das artes (HTML → JPG)

- `build.py`: base visual (cores, ícones, cards, rodapé) + carrossel da escala 6x1.
- `semana3.py`: stories e posts da semana de 23 a 27/11/2026.
- `blackfriday.py`: peças da Black Friday (50% nos 3 primeiros meses, novas contratações).

Para gerar de novo: `pip install playwright pillow && python semana3.py` (as imagens saem em `s3/`).
Para gerar só uma peça: `python semana3.py bf-abertura`.
