"""
Writer Agent - Takes research findings and drafts a structured report.
Supports initial drafting and revision based on reviewer feedback.
"""

import json
from src.llm_client import llm
from src.models import DraftReport, ResearchResult, ReviewResult


SYSTEM_PROMPT_DRAFT = """You are a professional technical writer.
Your job is to take raw research findings and write a comprehensive, high-quality, and well-structured report.

You MUST respond ONLY with a valid JSON object in this exact format:
{
    "title": "Professional Title of the Report",
    "introduction": "An engaging introduction based on the research findings (1-2 paragraphs)",
    "key_points": [
        "Core point 1 elaborated with details from findings",
        "Core point 2 elaborated with details from findings",
        "Core point 3 elaborated with details from findings"
    ],
    "conclusion": "A strong concluding paragraph summarizing future outlook",
    "full_text": "The complete, formatted report ready for publication. Use markdown formatting like bold text or lists where appropriate."
}

Do NOT include any text outside the JSON. Do NOT use markdown code blocks inside your response.
Respond with raw JSON only."""


SYSTEM_PROMPT_REVISE = """You are a professional technical writer revising a draft report.
You will receive the original draft AND the reviewer's feedback.
Your job is to improve the draft by addressing ALL the reviewer's concerns.

Rules:
- Fix every issue mentioned in the feedback.
- Improve weak sections.
- Keep the same JSON structure.
- Do NOT ignore any feedback point.

You MUST respond ONLY with a valid JSON object in this exact format:
{
    "title": "Revised Title if needed",
    "introduction": "Improved introduction",
    "key_points": [
        "Improved point 1",
        "Improved point 2",
        "Improved point 3"
    ],
    "conclusion": "Improved conclusion",
    "full_text": "The complete revised report."
}

Do NOT include any text outside the JSON. Do NOT use markdown code blocks.
Respond with raw JSON only."""


def _parse_response(raw_response: str, fallback_title: str) -> DraftReport:
    """Helper to parse LLM JSON response into DraftReport."""
    if raw_response.startswith("LLM_ERROR"):
        return DraftReport(
            title=fallback_title,
            introduction="",
            key_points=[],
            conclusion="",
            full_text=raw_response
        )

    try:
        cleaned = raw_response.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1]
        if cleaned.endswith("```"):
            cleaned = cleaned.rsplit("```", 1)[0]
        cleaned = cleaned.strip()

        data = json.loads(cleaned)
        return DraftReport(**data)

    except (json.JSONDecodeError, Exception) as e:
        return DraftReport(
            title=fallback_title,
            introduction="Parsing failed",
            key_points=[],
            conclusion="Parsing failed",
            full_text=raw_response
        )


def write_draft(research_result: ResearchResult) -> DraftReport:
    """Create an initial draft report from research findings."""
    print(f"✍️ Writer Agent: Generating draft for '{research_result.topic}'...")

    user_payload = {
        "topic": research_result.topic,
        "key_findings": research_result.key_findings,
        "summary": research_result.summary
    }

    raw_response = llm.chat(
        system_prompt=SYSTEM_PROMPT_DRAFT,
        user_prompt=f"Create a professional report based on this research data:\n{json.dumps(user_payload, indent=2)}"
    )

    result = _parse_response(raw_response, f"Draft - {research_result.topic}")
    print(f"✅ Writer Agent: Draft generated. Title: '{result.title}'")
    return result


def revise_draft(draft: DraftReport, review: ReviewResult) -> DraftReport:
    """Revise a draft report based on reviewer feedback."""
    print(f"🔄 Writer Agent: Revising draft based on reviewer feedback (Score: {review.quality_score}/10)...")

    user_payload = {
        "original_draft": {
            "title": draft.title,
            "introduction": draft.introduction,
            "key_points": draft.key_points,
            "conclusion": draft.conclusion,
            "full_text": draft.full_text
        },
        "reviewer_feedback": review.feedback,
        "reviewer_issues": review.issues,
        "quality_score": review.quality_score
    }

    raw_response = llm.chat(
        system_prompt=SYSTEM_PROMPT_REVISE,
        user_prompt=f"Revise this draft report based on the reviewer's feedback:\n{json.dumps(user_payload, indent=2)}"
    )

    result = _parse_response(raw_response, draft.title)
    print(f"✅ Writer Agent: Revision completed. Title: '{result.title}'")
    return result