"""
Writer Agent - Takes research findings and drafts a structured report.
"""

import json
from src.llm_client import llm
from src.models import DraftReport, ResearchResult


SYSTEM_PROMPT = """You are a professional technical writer.
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


def write_draft(research_result: ResearchResult) -> DraftReport:
    """
    Run the Writer Agent to draft a report based on research findings.

    Args:
        research_result: The structured findings from the Researcher.

    Returns:
        DraftReport containing the structured article/report.
    """
    print(f"✍️ Writer Agent: Generating draft for '{research_result.topic}'...")

    user_payload = {
        "topic": research_result.topic,
        "key_findings": research_result.key_findings,
        "summary": research_result.summary
    }

    raw_response = llm.chat(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=f"Create a professional report based on this research data:\n{json.dumps(user_payload, indent=2)}"
    )

    if raw_response.startswith("LLM_ERROR"):
        print(f"❌ Writer Agent: {raw_response}")
        return DraftReport(
            title="Draft Generation Failed",
            introduction="",
            key_points=[],
            conclusion="",
            full_text=raw_response
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
        result = DraftReport(**data)
        print(f"✅ Writer Agent: Draft successfully generated. Title: '{result.title}'")
        return result

    except (json.JSONDecodeError, Exception) as e:
        print(f"⚠️ Writer Agent: Could not parse response. Error: {e}")
        return DraftReport(
            title=f"Draft - {research_result.topic}",
            introduction="Parsing failed",
            key_points=research_result.key_findings,
            conclusion="Parsing failed",
            full_text=raw_response
        )