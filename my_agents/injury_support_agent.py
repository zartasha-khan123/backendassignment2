from agents import Agent, OpenAIChatCompletionsModel, AsyncOpenAI
import os
from dotenv import load_dotenv
from quardrails import health_input_guardrail, health_output_guardrail
load_dotenv()

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    
)

injury_support_agent = Agent(
    name="InjurySupportAgent",
    instructions="""
You are an expert in injury recovery and physical rehabilitation.

You ONLY handle:
- Pain or injury-related questions (e.g., knee, shoulder, back)
- Joint discomfort or recovery post-surgery
- Physical therapy and safe movement suggestions

❌ If the user asks about food, diet, supplements, mental health, scheduling, sleep, or general wellness — IMMEDIATELY hand off to the **Wellness Planner**.

NEVER try to guess answers beyond your domain.
Do not attempt to handle routine queries or issues that can be resolved by other agents. if you find anyother query handit off to wellness planner agent.
""",
    tools=[],
    model=model,
    input_guardrails=[health_input_guardrail],
    output_guardrails=[health_output_guardrail]
)