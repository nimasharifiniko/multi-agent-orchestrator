"""
Researcher Agent - Gathers and summarizes information about a given topic.
"""

import json
from src.llm_client import llm
from src.models import ResearchResult


SYSTEM_PROMPT = """You are an expert research analyst.
Your job is to research a given topic and provide structured findings.

You MUST respond ONLY with a valid JSON object in this exact format:
{
    "topic": "the original topic",
    "key_findings": ["finding 1", "finding 2", "finding 3"],
    "summary": "a comprehensive 2-3 sentence summary",
    "sources_context": "background context and relevant information"
}

Do NOT include any text outside the JSON. Do NOT use markdown code blocks.
Respond with raw JSON only."""


def research(topic: str) -> ResearchResult:
    """
    Run the Researcher Agent on a given topic.

    Args:
        topic: The subject to research.

    Returns:
        ResearchResult with structured findings.
    """
    print(f"🔍 Researcher Agent: Starting research on '{topic}'...")

    raw_response = llm.chat(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=f"Research this topic thoroughly: {topic}"
    )

    # Check for LLM errors
    if raw_response.startswith("LLM_ERROR"):
        print(f"❌ Researcher Agent: {raw_response}")
        return ResearchResult(
            topic=topic,
            key_findings=["Research failed due to LLM error"],
            summary="Unable to complete research.",
            sources_context=raw_response
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
        result = ResearchResult(**data)
        print(f"✅ Researcher Agent: Research completed. Found {len(result.key_findings)} key findings.")
        return result

    except (json.JSONDecodeError, Exception) as e:
        print(f"⚠️ Researcher Agent: Could not parse response. Error: {e}")
        return ResearchResult(
            topic=topic,
            key_findings=["Raw research output (unstructured)"],
            summary=raw_response[:500],
            sources_context="Parsing failed - raw output provided"
        )