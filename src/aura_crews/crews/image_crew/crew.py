"""Image Crew — Visual prompt engineering."""
import os
import time
from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, crew, task
from fastapi import APIRouter
from src.aura_crews.schemas.models import CrewRequest, CrewResponse
from src.aura_crews.guardrails.hallucination import hallucination_guardrail

router = APIRouter()


@CrewBase
class ImageCrew:
    """Image crew — visual designer for prompt engineering."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self):
        self.llm = LLM(
            model=os.getenv("DEFAULT_MODEL", "openrouter/google/gemini-2.0-flash-001"),
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )

    @agent
    def visual_designer(self) -> Agent:
        return Agent(config=self.agents_config["visual_designer"], llm=self.llm)

    @task
    def prompt_task(self) -> Task:
        return Task(
            config=self.tasks_config["prompt_task"],
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


@router.post("/crew/image", response_model=CrewResponse)
async def run_image(request: CrewRequest):
    """Execute image crew."""
    t0 = time.time()
    try:
        result = ImageCrew().crew().kickoff(
            inputs={
                "topic": request.task,
                "user_name": request.context.get("userName", "Boss"),
            }
        )
        return CrewResponse(
            success=True,
            response=result.raw,
            crew="image",
            duration=round(time.time() - t0, 2),
            metadata={"token_usage": str(getattr(result, "token_usage", ""))},
        )
    except Exception as e:
        return CrewResponse(
            success=False,
            response=f"Image error: {e}",
            crew="image",
            duration=round(time.time() - t0, 2),
        )
