"""Chat Crew — AURA conversational ability."""
import os
import time
from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, crew, task
from fastapi import APIRouter
from src.aura_crews.schemas.models import CrewRequest, CrewResponse
from src.aura_crews.guardrails.hallucination import hallucination_guardrail

router = APIRouter()


@CrewBase
class ChatCrew:
    """Chat crew — single agent for natural conversation."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self):
        self.llm = LLM(
            model=os.getenv("DEFAULT_MODEL", "openrouter/google/gemini-2.0-flash-001"),
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )

    @agent
    def chat_agent(self) -> Agent:
        return Agent(config=self.agents_config["chat_agent"], llm=self.llm)

    @task
    def chat_task(self) -> Task:
        return Task(
            config=self.tasks_config["chat_task"],
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


@router.post("/crew/chat", response_model=CrewResponse)
async def run_chat(request: CrewRequest):
    """Execute chat crew."""
    t0 = time.time()
    try:
        result = ChatCrew().crew().kickoff(
            inputs={
                "topic": request.task,
                "user_name": request.context.get("userName", "Boss"),
            }
        )
        return CrewResponse(
            success=True,
            response=result.raw,
            crew="chat",
            duration=round(time.time() - t0, 2),
            metadata={"token_usage": str(getattr(result, "token_usage", ""))},
        )
    except Exception as e:
        return CrewResponse(
            success=False,
            response=f"Chat error: {e}",
            crew="chat",
            duration=round(time.time() - t0, 2),
        )
