"""
Data models for the Multi-Agent Orchestration System.
Defines structured inputs and outputs for each agent.
"""

from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional


class AgentStatus(str, Enum):
    """Status of an agent during workflow execution."""
    WAITING = "waiting"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class WorkflowStatus(str, Enum):
    """Overall status of the orchestration workflow."""
    PENDING = "pending"
    RESEARCHING = "researching"
    WRITING = "writing"
    REVIEWING = "reviewing"
    REVISING = "revising"
    COMPLETED = "completed"
    FAILED = "failed"


class ResearchResult(BaseModel):
    """Output from the Researcher Agent."""
    topic: str
    key_findings: list[str] = Field(description="List of key research findings")
    summary: str = Field(description="Comprehensive summary of research")
    sources_context: str = Field(description="Context and background information")


class DraftReport(BaseModel):
    """Output from the Writer Agent."""
    title: str
    introduction: str
    key_points: list[str] = Field(description="Main points of the report")
    conclusion: str
    full_text: str = Field(description="Complete formatted report")


class ReviewResult(BaseModel):
    """Output from the Reviewer Agent."""
    quality_score: int = Field(ge=1, le=10, description="Quality score from 1 to 10")
    approved: bool = Field(description="Whether the report meets quality standards")
    feedback: str = Field(description="Detailed feedback for improvement")
    issues: list[str] = Field(default_factory=list, description="Specific issues found")


class WorkflowState(BaseModel):
    """Central state that tracks the entire workflow."""
    topic: str
    status: WorkflowStatus = WorkflowStatus.PENDING
    research: Optional[ResearchResult] = None
    draft: Optional[DraftReport] = None
    review: Optional[ReviewResult] = None
    iteration: int = 0
    max_iterations: int = 3
    final_output: Optional[str] = None
    error: Optional[str] = None