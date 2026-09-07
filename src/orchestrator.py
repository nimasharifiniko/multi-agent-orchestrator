"""
Orchestrator - The central engine that manages the entire multi-agent workflow.
Handles state, agent execution, feedback loops, and error recovery.
"""

from src.models import WorkflowState, WorkflowStatus
from src.researcher import research
from src.writer import write_draft, revise_draft
from src.reviewer import review_draft


MAX_ITERATIONS = 3


class Orchestrator:
    """Coordinates the Researcher, Writer, and Reviewer agents with feedback loops."""

    def __init__(self, max_iterations: int = MAX_ITERATIONS):
        self.max_iterations = max_iterations

    def run(self, topic: str) -> WorkflowState:
        """
        Execute the full multi-agent workflow for a given topic.

        Args:
            topic: The subject to research, write, and review.

        Returns:
            Final WorkflowState with all agent outputs and status.
        """
        state = WorkflowState(topic=topic, max_iterations=self.max_iterations)

        print("\n" + "=" * 60)
        print(f"🚀 ORCHESTRATOR: Starting workflow for topic:")
        print(f"   '{topic}'")
        print("=" * 60 + "\n")

        # === STEP 1: RESEARCH ===
        try:
            state.status = WorkflowStatus.RESEARCHING
            state.research = research(topic)

            if not state.research.key_findings or "failed" in state.research.summary.lower():
                state.status = WorkflowStatus.FAILED
                state.error = "Research phase produced no valid findings."
                print(f"\n❌ ORCHESTRATOR: {state.error}")
                return state

        except Exception as e:
            state.status = WorkflowStatus.FAILED
            state.error = f"Research phase crashed: {str(e)}"
            print(f"\n❌ ORCHESTRATOR: {state.error}")
            return state

        # === STEP 2: INITIAL DRAFT ===
        try:
            state.status = WorkflowStatus.WRITING
            state.draft = write_draft(state.research)

        except Exception as e:
            state.status = WorkflowStatus.FAILED
            state.error = f"Writing phase crashed: {str(e)}"
            print(f"\n❌ ORCHESTRATOR: {state.error}")
            return state

        # === STEP 3: REVIEW + FEEDBACK LOOP ===
        for iteration in range(1, self.max_iterations + 1):
            state.iteration = iteration
            print(f"\n--- 🔁 ITERATION {iteration}/{self.max_iterations} ---")

            try:
                state.status = WorkflowStatus.REVIEWING
                state.review = review_draft(state.draft)

            except Exception as e:
                state.status = WorkflowStatus.FAILED
                state.error = f"Review phase crashed at iteration {iteration}: {str(e)}"
                print(f"\n❌ ORCHESTRATOR: {state.error}")
                return state

            # If approved, we are done
            if state.review.approved:
                state.status = WorkflowStatus.COMPLETED
                state.final_output = state.draft.full_text
                print(f"\n✅ ORCHESTRATOR: Draft APPROVED at iteration {iteration}.")
                print(f"   Final Quality Score: {state.review.quality_score}/10")
                return state

            # If not approved AND we still have iterations left, revise
            if iteration < self.max_iterations:
                print(f"⚠️ ORCHESTRATOR: Draft NOT approved. Sending back to Writer for revision...")
                try:
                    state.status = WorkflowStatus.REVISING
                    state.draft = revise_draft(state.draft, state.review)

                except Exception as e:
                    state.status = WorkflowStatus.FAILED
                    state.error = f"Revision phase crashed at iteration {iteration}: {str(e)}"
                    print(f"\n❌ ORCHESTRATOR: {state.error}")
                    return state

        # === STEP 4: MAX ITERATIONS REACHED WITHOUT APPROVAL ===
        state.status = WorkflowStatus.COMPLETED
        state.final_output = state.draft.full_text
        state.error = f"Max iterations ({self.max_iterations}) reached without full approval. Returning best draft."
        print(f"\n⚠️ ORCHESTRATOR: {state.error}")
        print(f"   Final Quality Score: {state.review.quality_score}/10")
        return state