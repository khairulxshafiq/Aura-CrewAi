"""
AURA Flow — Main orchestration flow.
Routes user input to correct crew using Flow-first architecture.
"""
from crewai.flow.flow import Flow, start, listen, router
from pydantic import BaseModel
import time


class AuraState(BaseModel):
    """State passed between flow steps."""
    user_input: str = ""
    intent: str = "chat"
    user_name: str = "Boss"
    chat_id: str = ""
    crew_result: str = ""
    success: bool = False
    duration: float = 0.0


class AuraFlow(Flow[AuraState]):
    """
    Main AURA Flow — Route user input to correct crew.
    Pattern: receive → detect intent → route → execute → return
    """

    @start()
    def receive_input(self):
        """Step 1: Receive and validate user input."""
        print(f"[FLOW] Input: {self.state.user_input[:80]}...")
        return self.state.user_input

    @router(receive_input)
    def route_to_crew(self):
        """Step 2: Detect intent and route to correct crew."""
        text = self.state.user_input.lower()

        if any(k in text for k in ["content", "post", "caption", "hashtag", "tulis", "write"]):
            self.state.intent = "content"
            return "content"
        elif any(k in text for k in ["research", "cari", "search", "find", "analisis", "analyze"]):
            self.state.intent = "research"
            return "research"
        elif any(k in text for k in ["image", "gambar", "photo", "design", "logo", "visual"]):
            self.state.intent = "image"
            return "image"
        elif any(k in text for k in ["finance", "kira", "calculate", "duit", "money", "revenue", "cost", "budget"]):
            self.state.intent = "finance"
            return "finance"
        else:
            self.state.intent = "chat"
            return "chat"

    @listen("chat")
    def run_chat(self):
        from src.aura_crews.crews.chat_crew.crew import ChatCrew
        t0 = time.time()
        try:
            result = ChatCrew().crew().kickoff(
                inputs={"topic": self.state.user_input, "user_name": self.state.user_name}
            )
            self.state.crew_result = result.raw
            self.state.success = True
        except Exception as e:
            self.state.crew_result = f"Chat error: {e}"
            self.state.success = False
        self.state.duration = round(time.time() - t0, 2)

    @listen("content")
    def run_content(self):
        from src.aura_crews.crews.content_crew.crew import ContentCrew
        t0 = time.time()
        try:
            result = ContentCrew().crew().kickoff(
                inputs={"topic": self.state.user_input, "user_name": self.state.user_name}
            )
            self.state.crew_result = result.raw
            self.state.success = True
        except Exception as e:
            self.state.crew_result = f"Content error: {e}"
            self.state.success = False
        self.state.duration = round(time.time() - t0, 2)

    @listen("research")
    def run_research(self):
        from src.aura_crews.crews.research_crew.crew import ResearchCrew
        t0 = time.time()
        try:
            result = ResearchCrew().crew().kickoff(
                inputs={"topic": self.state.user_input, "user_name": self.state.user_name}
            )
            self.state.crew_result = result.raw
            self.state.success = True
        except Exception as e:
            self.state.crew_result = f"Research error: {e}"
            self.state.success = False
        self.state.duration = round(time.time() - t0, 2)

    @listen("image")
    def run_image(self):
        from src.aura_crews.crews.image_crew.crew import ImageCrew
        t0 = time.time()
        try:
            result = ImageCrew().crew().kickoff(
                inputs={"topic": self.state.user_input, "user_name": self.state.user_name}
            )
            self.state.crew_result = result.raw
            self.state.success = True
        except Exception as e:
            self.state.crew_result = f"Image error: {e}"
            self.state.success = False
        self.state.duration = round(time.time() - t0, 2)

    @listen("finance")
    def run_finance(self):
        from src.aura_crews.crews.finance_crew.crew import FinanceCrew
        t0 = time.time()
        try:
            result = FinanceCrew().crew().kickoff(
                inputs={"topic": self.state.user_input, "user_name": self.state.user_name}
            )
            self.state.crew_result = result.raw
            self.state.success = True
        except Exception as e:
            self.state.crew_result = f"Finance error: {e}"
            self.state.success = False
        self.state.duration = round(time.time() - t0, 2)
