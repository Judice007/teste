# Checklist de Teste — MVP Clip Generator

Roteiro para validar o pipeline completo rodando via Docker Compose. Marque
cada item ao validar. Itens com **[já validado]** foram testados nesta sessão
fora do Docker (venv local + Redis local) e não precisam ser repetidos, só
confirmados dentro do ambiente real.

## 0. Pré-requisitos

- [ ] Docker e Docker Compose instalados
- [ ] `cp .env.example .env`
- [ ] (opcional) preencher `ANTHROPIC_API_KEY` no `.env` para testar seleção de
      highlights via LLM — sem isso, o fallback heurístico entra em ação
      automaticamente
- [ ] Ter à mão a URL de um VOD curto (2–5 min) do YouTube para o teste
      inicial — evita esperar transcrição/processamento de um vídeo longo

## 1. Subir o ambiente

- [ ] `docker compose up --build`
- [ ] Os 5 serviços sobem sem erro: `postgres`, `redis`, `api`, `worker`,
      `frontend`
- [ ] `worker` loga a inicialização do Celery sem erro de conexão com o
      Redis

## 2. Infraestrutura básica

- [ ] `curl http://localhost:8000/health` → `{"status":"ok"}`
- [ ] `http://localhost:8000/docs` abre o Swagger UI com as rotas
      `/projects` e `/clips/{id}/download`
- [ ] `http://localhost:3000` abre o frontend sem erro no console
- [ ] **[já validado]** `POST /projects` cria o registro e chama
      `process_project.delay(...)` sem erro de conexão com o broker

## 3. Fluxo completo (o que ainda não foi possível testar sem Docker)

Este é o teste que mais importa: exercita `yt-dlp` + `ffmpeg`, que não
puderam ser validados no ambiente de desenvolvimento (sandbox sem esses
binários).

- [ ] Colar a URL do VOD curto no frontend e enviar
- [ ] Etapa `fetch_source` conclui — arquivo aparece em
      `storage/<project_id>/source.mp4` (volume `storage_data`)
- [ ] Etapa `transcribe` conclui — não trava/estoura memória com o modelo
      `base` do faster-whisper
- [ ] Etapa `score_highlights` conclui — confirmar no log do worker se caiu
      no fallback heurístico ou usou a LLM (dependendo se
      `ANTHROPIC_API_KEY` foi preenchida)
- [ ] Etapa `render_clips` conclui — nenhum erro de `ffmpeg` no log do
      worker (checar `subprocess.CalledProcessError`, indica filtro de vídeo
      ou parâmetro inválido)
- [ ] Etapa `burn_captions` conclui
- [ ] Status do projeto na página `/projects/{id}` chega a `completed`
- [ ] Clipe(s) aparecem na lista com o motivo (`reason`) preenchido
- [ ] Botão "Baixar clipe" baixa um `.mp4` que abre e reproduz normalmente
- [ ] O vídeo baixado está em 9:16 (1080x1920) e com legenda visível
      queimada na imagem

## 4. Casos de borda

- [ ] URL inválida/vídeo privado → projeto vai para `status: failed` e o
      `error` da etapa `fetch_source` aparece na página do projeto (não
      trava o worker nem quebra o container)
- [ ] VOD sem fala/silêncio total → `score_highlights` não quebra com lista
      de segmentos vazia (o fallback heurístico já trata `segments == []`
      retornando lista vazia — confirmar que o resto do pipeline não
      quebra com zero highlights)
- [ ] Dois projetos enviados em sequência rápida → ambos processam sem os
      workers pisarem no mesmo diretório (cada um usa
      `storage/<project_id>/`, então não deveria colidir)
- [ ] Reiniciar o `worker` (`docker compose restart worker`) no meio de um
      job → o job fica órfão em `running`; não há retomada automática nesta
      versão (limitação conhecida, ver `docs/mvp-architecture.md`)

## 5. Registro de resultados

Depois de rodar, anote aqui (ou em um comentário/PR) o que quebrou:

```
Data do teste:
VOD usado:
Etapa que falhou (se houver):
Mensagem de erro:
Ajuste necessário:
```
