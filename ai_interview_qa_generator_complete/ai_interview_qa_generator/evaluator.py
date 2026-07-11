import json
from openai import OpenAI

def evaluate_answer(model, question, answer, job_title):
    client = OpenAI()
    prompt = f"""
You are evaluating a candidate interviewing for: {job_title}

Question:
{question["question"]}

Evaluation intent:
{question.get("intent", "")}

Ideal answer blueprint:
{question.get("ideal_answer_blueprint", [])}

Candidate answer:
{answer}

Return ONLY valid JSON:
{{
  "score": 0,
  "feedback": "concise but useful feedback",
  "strengths": ["strength"],
  "improvements": ["improvement"]
}}

Score must be an integer from 0 to 10.
"""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a fair, evidence-based technical interview evaluator."},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
    )
    return json.loads(response.choices[0].message.content)

def generate_final_report(model, job_title, evaluations):
    client = OpenAI()
    prompt = f"""
Create a concise final interview report for a {job_title} candidate.

Evaluations:
{json.dumps(evaluations, indent=2)}

Include:
## Overall Assessment
## Key Strengths
## Areas for Improvement
## Hiring Recommendation
## Recommended Next Steps

Do not invent evidence beyond the evaluations.
"""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You create professional interview assessment reports."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content
