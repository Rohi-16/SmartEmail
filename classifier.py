# classifier.py
import re
from dateutil import parser as dateparser

URGENCY_KEYWORDS = [
    'urgent', 'asap', 'immediately', 'important', 'priority', 'deadline', 'due by', 'action required', 'respond', 'please review'
]

def _contains_deadline(text: str):
    try:
        # naive date detection: find patterns like "on Aug 10" or "by 2025-08-10" or "tomorrow"
        # use dateparser to try to parse substrings
        dates = []
        tokens = re.split('[,;:\n]', text)
        for tok in tokens:
            tok = tok.strip()
            if len(tok) < 6:
                continue
            try:
                d = dateparser.parse(tok, fuzzy=False)
                if d:
                    dates.append(d)
            except Exception:
                continue
        return len(dates) > 0
    except Exception:
        return False


def score_priority(email: dict) -> tuple:
    """Return (score:int 0-100, label:str, reasons:list).

    `email` expected keys: 'subject', 'from', 'body', optional 'is_important_sender' boolean.
    This is intentionally interpretable — perfect for a portfolio to show reasoning.
    """
    body = email.get('body','').lower()
    subject = email.get('subject','').lower()
    score = 0
    reasons = []

    # base rules
    if any(k in body for k in URGENCY_KEYWORDS) or any(k in subject for k in URGENCY_KEYWORDS):
        score += 40
        reasons.append('Contains urgency keywords')

    if _contains_deadline(body) or _contains_deadline(subject):
        score += 30
        reasons.append('Mentions a date/deadline')

    # questions often indicate required response
    qcount = body.count('?')
    if qcount:
        add = min(10, qcount*5)
        score += add
        reasons.append(f'Contains {qcount} question mark(s)')

    # short emails that ask for action get more weight
    if len(body.split()) < 30 and len(body) > 5 and any(w in body for w in ['please', 'could you', 'can you', 'kindly']):
        score += 15
        reasons.append('Short action-oriented email')

    # sender importance override
    if email.get('is_important_sender'):
        score += 20
        reasons.append('Sender flagged important')

    # clamp
    score = max(0, min(100, score))
    if score >= 70:
        label = 'High'
    elif score >= 35:
        label = 'Medium'
    else:
        label = 'Low'

    if not reasons:
        reasons.append('No urgent indicators found — standard priority')

    return score, label, reasons