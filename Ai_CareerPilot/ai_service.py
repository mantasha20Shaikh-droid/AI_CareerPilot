"""Honest local fallback. External LLM integration is optional and never faked."""
import os, requests

def recommendations(role, missing_skills, category='Mixed', count=8):
    provider = os.getenv('AI_PROVIDER','none').lower()
    key = os.getenv('AI_API_KEY','').strip()
    base = os.getenv('AI_BASE_URL','').strip()
    model = os.getenv('AI_MODEL','').strip()
    if provider == 'openai-compatible' and key and base and model:
        try:
            response = requests.post(base.rstrip('/') + '/chat/completions', headers={'Authorization':f'Bearer {key}'}, json={'model':model,'messages':[{'role':'system','content':'Generate concise career interview questions. Return a JSON array of strings only.'},{'role':'user','content':f'Role: {role}; category: {category}; generate {count} questions.'}]}, timeout=20)
            response.raise_for_status()
            import json
            content=response.json()['choices'][0]['message']['content']
            parsed=json.loads(content)
            if isinstance(parsed,list) and parsed: return {'source':'AI provider','questions':[str(x) for x in parsed[:count]]}
        except Exception:
            pass
    bank = [f'Explain a project where you used {s}.' for s in (missing_skills or [])]
    bank += [f'What are the core responsibilities of a {role}?', 'Describe a challenging problem you solved and how you measured success.', 'How do you validate the quality of your data or results?', 'Tell me about a time you received critical feedback.', 'How would you explain a technical concept to a non-technical stakeholder?', 'What would you do in your first 30 days in this role?', 'Describe a trade-off you made in a project and why.']
    if category.lower() not in ('mixed','hr'):
        bank = [q for q in bank if category.lower() in ('technical','problem-solving') or any(k in q.lower() for k in ('tell me','time','feedback','first 30'))] or bank
    return {'source':'Local fallback question bank','questions':bank[:max(1,min(count,20))]}
