"""Finance Crew — Financial analysis + reporting."""
import os
import time
from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, crew, task
from fastapi import APIRouter
from src.aura_crews.schemas.models import CrewRequest, CrewResponse
from src.aura_crews.guardrails.hallucination import hallucination_guardrail

router = APIRouter()


@CrewBase
class FinanceCrew:
    """Finance crew — analyst + reporter for financial tasks."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self):
        self.llm = LLM(
            model=os.getenv("DEFAULT_MODEL", "openrouter/google/gemini-2.0-flash-001"),
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )

    @agent
    def financial_analyst(self) -> Agent:
        return Agent(config=self.agents_config["financial_analyst"], llm=self.llm)

    @agent
    def finance_reporter(self) -> Agent:
        return Agent(config=self.agents_config["finance_reporter"], llm=self.llm)

    @task
    def analysis_task(self) -> Task:
        return Task(config=self.tasks_config["analysis_task"])

    @task
    def finance_report_task(self) -> Task:
        return Task(
            config=self.tasks_config["finance_report_task"],
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


@router.post("/crew/finance", response_model=CrewResponse)
async def run_finance(request: CrewRequest):
    """Execute finance crew."""
    t0 = time.time()
    try:
        result = FinanceCrew().crew().kickoff(
            inputs={
                "topic": request.task,
                "user_name": request.context.get("userName", "Boss"),
            }
        )
        return CrewResponse(
            success=True,
            response=result.raw,
            crew="finance",
            duration=round(time.time() - t0, 2),
            metadata={"token_usage": str(getattr(result, "token_usage", ""))},
        )
    except Exception as e:
        return CrewResponse(
            success=False,
            response=f"Finance error: {e}",
            crew="finance",
            duration=round(time.time() - t0, 2),
        )
