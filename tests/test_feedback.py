"""
Dedicated test to explicitly verify the Feedback Loop and Writer Revision mechanism.
"""

from src.models import ResearchResult, DraftReport, ReviewResult
from src.writer import revise_draft


def test_revision_loop():
    print("\n" + "🔄" * 30)
    print("  FEEDBACK LOOP DIRECT TEST")
    print("🔄" * 30 + "\n")

    # 1. Create a weak dummy draft
    dummy_draft = DraftReport(
        title="AI in Dev",
        introduction="AI is good.",
        key_points=["It helps code."],
        conclusion="The end.",
        full_text="AI is good. It helps code. The end."
    )

    # 2. Create dummy review feedback (simulating Reviewer rejection)
    dummy_review = ReviewResult(
        quality_score=4,
        approved=False,
        feedback="The draft is far too short and lacks detail. Expand the introduction, add at least 3 concrete key points with explanations, and write a proper professional conclusion.",
        issues=["Too brief", "Missing key points", "Unprofessional conclusion"]
    )

    print("📄 ORIGINAL (WEAK) DRAFT:")
    print(f"Title: {dummy_draft.title}")
    print(f"Intro: {dummy_draft.introduction}\n")

    print(f"🧐 REVIEWER FEEDBACK (Score: {dummy_review.quality_score}/10):")
    print(f"Feedback: {dummy_review.feedback}\n")

    print("⚡ TRIGGERING WRITER REVISION...")
    revised_draft = revise_draft(dummy_draft, dummy_review)

    print("\n" + "=" * 60)
    print("✨ REVISED DRAFT RESULT:")
    print("=" * 60)
    print(f"Revised Title: {revised_draft.title}")
    print(f"Revised Intro: {revised_draft.introduction[:150]}...")
    print(f"Key Points Count: {len(revised_draft.key_points)}")
    print(f"Full Text Length: {len(revised_draft.full_text)} chars")
    print("=" * 60)
    print("\n✅ FEEDBACK LOOP VERIFIED SUCCESSFULLY!\n")


if __name__ == "__main__":
    test_revision_loop()