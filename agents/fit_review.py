from pydantic_ai import Agent

fit_review_agent = Agent(
 model="ollama:llama3.1",
    system_prompt="""
You are an expert technical recruiter.

Evaluate the match between:
1) Candidate CV
2) Cover letter
3) Job description

Return STRICTLY in this format:

CV_MATCH_PERCENT: <number 0-100>
COVER_LETTER_MATCH_PERCENT: <number 0-100>

STRENGTHS:
- bullet
- bullet

GAPS:
- bullet
- bullet

SUGGESTIONS:
- bullet
- bullet
"""
)
