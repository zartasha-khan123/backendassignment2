#agents_utils.py
import os
from dotenv import load_dotenv
import chainlit as cl
from agents import Agent, handoff, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig, RunContextWrapper
from my_agents.nutrition_expert_agent import nutrition_expert_agent
from my_agents.injury_support_agent import injury_support_agent
from my_agents.escalation import escalation_agent
from tools.goal_analyzer import analyze_goal
from tools.meal_planner import meal_planner
from tools.workout_recommender import workout_recommender
from tools.scheduler import generate_schedule
from tools.tracker import summarize_user_progress
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from utils.handoffs import make_on_handoff_message
from quardrails import health_input_guardrail, health_output_guardrail
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in your .env file!")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
   
)



planner_agent = Agent(
    name="Wellness Planner",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are a helpful and proactive wellness planning assistant.

Your primary focus is to support users with:
- General fitness goals
- Wellness routines
- Daily/weekly workout planning
- Basic lifestyle improvements (e.g., sleep habits, stress relief)

You have access to tools that help users:
- Set wellness goals
- Plan meals and workouts
- Build schedules
- Track progress

✅ You are responsible for creating **meal plans** using your tool. If a user asks for a meal plan or help with planning meals, DO NOT hand off — instead, use your `meal_planner` tool to respond.

🚨 DO NOT respond to queries outside your scope. You MUST hand off immediately in the following cases:

➡️ **Nutrition & Diet (except meal planning)**: If the user's question is about medical nutrition issues (e.g., diabetes management, allergies, supplement advice, nutritional deficiencies) — hand off to the `Nutrition Expert Agent`.

➡️ **Injury or Medical Support**: If the user mentions any pain, physical injury, joint issues, post-surgery recovery, or requires rehab advice — hand off to the `Injury Support Agent`.

➡️ **Frustrated or Dissatisfied User**: If the user is clearly frustrated, confused, or not satisfied with the assistance so far — hand off to the `Escalation Agent`.

You must never guess answers related to medical or emotionally sensitive topics. Always hand off to the proper expert agent with empathy and clarity.

Keep your tone:
- Friendly, supportive, and motivational
- Clear and to the point
- Do not tell the user you are handing off to another agent — just do it silently

Use your tools when the query is within your domain. Never attempt to answer outside your scope.
"""
,
    tools=[
        analyze_goal,
        meal_planner,
        workout_recommender,
        generate_schedule,
        summarize_user_progress
    ],
    model=model,
    handoffs=[
        handoff(agent=nutrition_expert_agent, on_handoff=make_on_handoff_message(nutrition_expert_agent)),
        handoff(agent=injury_support_agent, on_handoff=make_on_handoff_message(injury_support_agent)),
        handoff(agent=escalation_agent, on_handoff=make_on_handoff_message(escalation_agent)),
    ],
    input_guardrails = [health_input_guardrail],
    output_guardrails = [health_output_guardrail]

 
)