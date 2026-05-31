"""Content Crew — Strategy + Writing for social media."""
import os
import time
from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, crew, task
from fastapi import APIRouter
from src.aura_crews.schemas.models import CrewRequest, CrewResponse
from src.aura_crews.guardrails.hallucination import hallucination_guardrail

router = APIRouter()


@CrewBase
class ContentCrew:
    """Content crew — strategist + writer for social media posts."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self):
        self.llm = LLM(
            model=os.getenv("DEFAULT_MODEL", "openrouter/google/gemini-2.0-flash-001"),
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )

    @agent
    def content_strategist(self) -> Agent:
        return Agent(config=self.agents_config["content_strategist"], llm=self.llm)

    @agent
    def content_writer(self) -> Agent:
        return Agent(config=self.agents_config["content_writer"], llm=self.llm)

    @task
    def strategy_task(self) -> Task:
        return Task(config=self.tasks_config["strategy_task"])

    @task
    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config["writing_task"],
            guardrail=hallucination_guardrail,
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=False,
        )


@router.post("/crew/content", response_model=CrewResponse)
async def run_content(request: CrewRequest):
    """Execute content crew."""
    t0 = time.time()
    try:
        result = ContentCrew().crew().kickoff(
            inputs={
                "topic": request.task,
                "user_name": request.context.get("userName", "Boss"),
            }
        )
        return CrewResponse(
            success=True,
            response=result.raw,
            crew="content",
            duration=round(time.time() - t0, 2),
            metadata={"token_usage": str(getattr(result, "token_usage", ""))},
        )
    except Exception as e:
        return CrewResponse(
            success=False,
            response=f"Content error: {e}",
            crew="content",
            duration=round(time.time() - t0, 2),
        )
