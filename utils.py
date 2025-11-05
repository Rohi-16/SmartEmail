# utils.py
import json

SAMPLE = [
    {
        "from": "ceo@startup.com",
        "subject": "Quick: please review Q4 budget by Oct 10",
        "body": "Hi — can you please review the attached budget and send me feedback by Oct 10? It's urgent as we need to finalize.",
        "is_important_sender": True
    },
    {
        "from": "friend@example.com",
        "subject": "Dinner this weekend?",
        "body": "Hey! Want to grab dinner tomorrow?",
        "is_important_sender": False
    },
    {
        "from": "alerts@service.com",
        "subject": "Your weekly report is ready",
        "body": "Hello, your weekly summary is ready. No action needed unless otherwise.",
        "is_important_sender": False
    }
]


def load_sample_emails():
    return SAMPLE


def save_json(path, data):
    with open(path,'w',encoding='utf-8') as f:
        json.dump(data,f,indent=2)