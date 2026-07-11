import json
from openai import OpenAI
from prompts import INTERVIEW_SYSTEM_PROMPT

class AIInterviewGenerator:
    def __init__(self, model="gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model

    def generate_interview_flow(self, job_title, job_description, resume_text, question_count=5):
        prompt = f"""
Job Title: {job_title}

Job Description:
{job_description}

Candidate Resume:
{resume_text}

Generate exactly {question_count} highly specific interview questions.
Return ONLY valid JSON with this structure:
{{
  "questions": [
    {{
      "question": "string",
      "category": "Technical|Behavioral|Project|Skill Gap",
      "difficulty": "Beginner|Intermediate|Advanced",
      "intent": "string",
      "ideal_answer_blueprint": ["point 1", "point 2", "point 3"]
    }}
  ]
}}
"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": INTERVIEW_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.5,
        )
        return json.loads(response.choices[0].message.content)
