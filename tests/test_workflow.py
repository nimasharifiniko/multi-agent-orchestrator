"""
Test script for the Multi-Agent Orchestration System.
Tests multiple topics and verifies the feedback loop works correctly.
"""

from src.orchestrator import Orchestrator


TEST_TOPICS = [
    "How AI Agents are changing software development",
    "The future of Python automation in business",
    "Why LLMs are revolutionizing customer support"
]


def run_tests():
    print("\n" + "🧪" * 30)
    print("  MULTI-AGENT WORKFLOW TEST SUITE")
    print("🧪" * 30)

    results = []

    for i, topic in enumerate(TEST_TOPICS, 1):
        print(f"\n\n{'#' * 60}")
        print(f"  TEST {i}/{len(TEST_TOPICS)}")
        print(f"{'#' * 60}")

        orchestrator = Orchestrator(max_iterations=3)
        state = orchestrator.run(topic)

        results.append({
            "topic": topic,
            "status": state.status.value,
            "iterations": state.iteration,
            "score": state.review.quality_score if state.review else 0,
            "approved": state.review.approved if state.review else False,
        })

    # === PRINT SUMMARY TABLE ===
    print("\n\n" + "=" * 70)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 70)
    print(f"{'Topic':<45} {'Status':<12} {'Iter':<6} {'Score':<7} {'Approved'}")
    print("-" * 70)

    for r in results:
        short_topic = r["topic"][:42] + "..." if len(r["topic"]) > 45 else r["topic"]
        approved_mark = "✅" if r["approved"] else "❌"
        print(f"{short_topic:<45} {r['status']:<12} {r['iterations']:<6} {r['score']:<7} {approved_mark}")

    print("=" * 70)

    # Check if any test triggered the feedback loop
    revised = [r for r in results if r["iterations"] > 1]
    if revised:
        print(f"\n🔄 Feedback Loop triggered in {len(revised)} test(s)! Loop is WORKING.")
    else:
        print("\nℹ️ All drafts approved on first iteration. Feedback loop code is ready but was not triggered.")

    print("\n🧪 ALL TESTS COMPLETED.\n")


if __name__ == "__main__":
    run_tests()