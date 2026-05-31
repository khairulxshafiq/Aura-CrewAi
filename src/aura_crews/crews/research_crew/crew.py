"""Research Crew — Analyst + Report Writer."""
import os
import time
from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, crew, task
from fastapi import APIRouter
from src.aura_crews.schemas.models import CrewRequest, CrewResponse
from src.aura_crews.guardrails.hallucination import hallucination_guardrail

router = APIRouter()


@CrewBase
class ResearchCrew:
    """Research crew — analyst + report writer."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self):
        self.llm = LLM(
            model=os.getenv("DEFAULT_MODEL", "openrouter/google/gemini-2.0-flash-001"),
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )

    @agent
    def research_analyst(self) -> Agent:
        return Agent(config=self.agents_config["research_analyst"], llm=self.llm)

    @agent
    def report_writer(self) -> Agent:
        return Agent(config=self.agents_config["report_writer"], llm=self.llm)

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config["research_task"])

    @task
    def report_task(self) -> Task:
        return Task(
            config=self.tasks_config["report_task"],
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


@router.post("/crew/research", response_model=CrewResponse)
async def run_research(request: CrewRequest):
    """Execute research crew."""
    t0 = time.time()
    try:
        result = ResearchCrew().crew().kickoff(
            inputs={
                "topic": request.task,
                "user_name": request.context.get("userName", "Boss"),
            }
        )
        return CrewResponse(
            success=True,
            response=result.raw,
            crew="research",
            duration=round(time.time() - t0, 2),
            metadata={"token_usage": str(getattr(result, "token_usage", ""))},
        )
    except Exception as e:
        return CrewResponse(
            success=False,
            response=f"Research error: {e}",
            crew="research",
            duration=round(time.time() - t0, 2),
        )
