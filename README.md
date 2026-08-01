# Clip Generator — MVP

Protótipo do núcleo comum ao StreamLadder e ao PlaySquad: transforma um VOD
(Twitch/YouTube/Kick) em clipes verticais com corte automático por IA,
reframe e legenda embutida. Ver `docs/mvp-architecture.md` para a proposta
de arquitetura completa e o roadmap de fases.

## Rodando localmente

Pré-requisitos: Docker e Docker Compose.

```bash
cp .env.example .env
# opcional: preencha ANTHROPIC_API_KEY para usar selecao de highlights por LLM.
# sem a chave, o pipeline usa um fallback heuristico (trechos distribuidos
# uniformemente pelo video), entao o fluxo roda de ponta a ponta sem custo de API.

docker compose up --build
```

- API: http://localhost:8000 (docs interativos em `/docs`)
- Frontend: http://localhost:3000

## Fluxo

1. Cole a URL de um VOD na tela inicial do frontend
2. O backend enfileira um job assíncrono (Celery) que:
   - baixa o vídeo (`yt-dlp`)
   - transcreve com timestamps (`faster-whisper`)
   - escolhe os melhores trechos (Claude API ou fallback heurístico)
   - corta e reenquadra cada trecho em 9:16 (`ffmpeg`, crop central)
   - queima a legenda no vídeo
3. Acompanhe o status de cada etapa na página do projeto e baixe os clipes
   prontos

## Estrutura

```
backend/    API (FastAPI) + workers (Celery) + pipeline de vídeo
frontend/   Next.js — formulário de novo projeto e acompanhamento de status
docs/       Proposta de arquitetura e decisões
```

## Limitações desta primeira versão

- Sem autenticação/usuários e sem billing — isso é a Fase 2 do roadmap
- Sem upload direto de arquivo (só URL por enquanto)
- Reframe usa crop central fixo, sem tracking de rosto/pessoa por cena
- Sem publicação automática em redes sociais (Fase 2)
- Sem migrations (Alembic) — o schema é criado via
  `Base.metadata.create_all` no startup, suficiente para o MVP
