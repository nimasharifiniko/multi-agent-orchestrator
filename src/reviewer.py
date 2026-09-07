"""
Reviewer Agent - Evaluates draft reports for quality, completeness, and structure.
"""

import json
from src.llm_client import llm
from src.models import DraftReport, ReviewResult


SYSTEM_PROMPT = """You are a senior technical editor and quality assurance specialist.
Your job is to strictly evaluate draft reports.

Evaluation Criteria:
1. Does the title match the topic?
2. Is the introduction engaging and clear?
3. Are there at least 3 concrete key points with sufficient detail?
4. Is there a strong conclusion?
5. Is the tone professional and informative?

Rules:
- Score from 1 to 10.
- If score >= 7, set approved to true. Otherwise, set approved to false.
- Provide actionable feedback for the writer if improvements are needed.
- List specific issues if any.

You MUST respond ONLY with a valid JSON object in this exact format:
{
    "quality_score": 8,
    "approved": true,
    "feedback": "Actionable feedback detailing strengths and areas for improvement.",
    "issues": ["Specific issue 1 if any", "Specific issue 2 if any"]
}

Do NOT include any text outside the JSON. Do NOT use markdown code blocks.
Respond with raw JSON only."""


def review_draft(draft: DraftReport) -> ReviewResult:
    """
    Run the Reviewer Agent to evaluate a draft report.

    Args:
        draft: The DraftReport created by the Writer.

    Returns:
        ReviewResult with quality score, approval status, and feedback.
    """
    print(f"🧐 Reviewer Agent: Evaluating draft '{draft.title}'...")

    user_payload = {
        "title": draft.title,
        "introduction": draft.introduction,
        "key_points": draft.key_points,
        "conclusion": draft.conclusion,
        "full_text": draft.full_text
    }

    raw_response = llm.chat(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=f"Strictly review and evaluate this draft report:\n{json.dumps(user_payload, indent=2)}"
    )

    if raw_response.startswith("LLM_ERROR"):
        print(f"❌ Reviewer Agent: {raw_response}")
        return ReviewResult(
            quality_score=1,
            approved=False,
            feedback=raw_response,
            issues=["LLM evaluation failed"]
        )

    try:
        # Clean response - remove markdown code blocks if present
        cleaned = raw_response.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1]
        if cleaned.endswith("```"):
            cleaned = cleaned.rsplit("```", 1)[0]
        cleaned = cleaned.strip()

        data = json.loads(cleaned)
        result = ReviewResult(**data)
        status = "APPROVED ✅" if result.approved else "NEEDS REVISION ⚠️"
        print(f"📊 Reviewer Agent: Finished evaluation. Score: {result.quality_score}/10 -> Status: {status}")
        return result

    except (json.JSONDecodeError, Exception) as e:
        print(f"⚠️ Reviewer Agent: Could not parse response. Error: {e}")
        return ReviewResult(
            quality_score=5,
            approved=False,
            feedback="Automatic review parsing failed. Manual review required.",
            issues=[f"Parser error: {str(e)}"]
        )