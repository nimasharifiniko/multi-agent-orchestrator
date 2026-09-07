"""
Main entry point for the Multi-Agent Orchestration System.
Runs the workflow on a given topic and prints the final report.
"""

from src.orchestrator import Orchestrator


def main():
    topic = "How AI Agents are changing software development"

    orchestrator = Orchestrator()
    state = orchestrator.run(topic)

    print("\n" + "=" * 60)
    print("📄 FINAL WORKFLOW SUMMARY")
    print("=" * 60)
    print(f"Topic:            {state.topic}")
    print(f"Status:           {state.status.value}")
    print(f"Total Iterations: {state.iteration}")

    if state.review:
        print(f"Final Score:      {state.review.quality_score}/10")
        print(f"Approved:         {state.review.approved}")

    if state.error:
        print(f"Note:             {state.error}")

    print("\n" + "-" * 60)
    print("📝 FINAL REPORT")
    print("-" * 60)
    if state.final_output:
        print(state.final_output)
    else:
        print("No final output produced.")
    print("=" * 60)


if __name__ == "__main__":
    main()