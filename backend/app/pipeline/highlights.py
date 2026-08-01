import json

from app.config import settings

try:
    import anthropic
except ImportError:
    anthropic = None


def select_highlights(segments: list[dict]) -> list[dict]:
    """Returns a list of {start, end, reason} highlight windows.

    Uses the Claude API when ANTHROPIC_API_KEY is configured; otherwise
    falls back to evenly-distributed segments so the pipeline still runs
    end-to-end without any paid API key.
    """
    if settings.anthropic_api_key and anthropic is not None:
        try:
            return _select_with_llm(segments)
        except Exception:
            return _select_with_heuristic(segments)
    return _select_with_heuristic(segments)


def _select_with_llm(segments: list[dict]) -> list[dict]:
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    transcript = "\n".join(f"[{s['start']:.1f}-{s['end']:.1f}] {s['text']}" for s in segments)
    prompt = (
        "Aqui esta a transcricao de um video com timestamps em segundos. "
        f"Escolha os {settings.highlight_clip_count} melhores trechos para "
        f"virarem clipes verticais virais de ate {settings.highlight_clip_seconds} "
        "segundos cada. Responda APENAS com um JSON valido: uma lista de "
        'objetos com as chaves "start", "end" e "reason".\n\n'
        f"{transcript}"
    )
    response = client.messages.create(
        model=settings.anthropic_model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text
    return json.loads(text)


def _select_with_heuristic(segments: list[dict]) -> list[dict]:
    if not segments:
        return []
    total_duration = segments[-1]["end"]
    count = settings.highlight_clip_count
    clip_len = min(settings.highlight_clip_seconds, total_duration)
    step = max(total_duration / count, clip_len)

    highlights = []
    for i in range(count):
        start = min(i * step, max(total_duration - clip_len, 0))
        end = min(start + clip_len, total_duration)
        highlights.append(
            {
                "start": start,
                "end": end,
                "reason": "Trecho selecionado por distribuicao uniforme (fallback sem LLM configurado)",
            }
        )
    return highlights
