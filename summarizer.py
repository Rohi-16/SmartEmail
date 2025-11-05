# summarizer.py
import os

def summarize_email(text: str, max_length: int = 120) -> str:
    """Return a short summary for an email body.

    Behavior:
      - If OPENAI_API_KEY is set, use OpenAI ChatCompletion (gpt-3.5-turbo or model env var).
      - Otherwise, fall back to a small transformers pipeline (if installed).
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        try:
            import openai
            openai.api_key = api_key
            model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
            prompt = (
                "You are an assistant that writes a concise summary (1-2 sentences) for an email. "
                f"Limit to {max_length} characters. If the email contains action items, list them briefly.\n\nEmail:\n"+text
            )
            resp = openai.ChatCompletion.create(
                model=model,
                messages=[{"role":"user","content":prompt}],
                temperature=0.2,
                max_tokens=200,
            )
            summary = resp['choices'][0]['message']['content'].strip()
            return summary
        except Exception as e:
            # fallback
            print('OpenAI summarization failed:', e)

    # Hugging Face fallback (small & optional)
    try:
        from transformers import pipeline
        summarizer = pipeline('summarization', truncation=True)
        out = summarizer(text, max_length=60, min_length=20)
        return out[0]['summary_text']
    except Exception as e:
        # final fallback: heuristic
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        first = lines[0] if lines else ''
        return (first[:max_length] + '...') if len(first) > max_length else first