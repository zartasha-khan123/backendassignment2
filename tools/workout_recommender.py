# tools/workout_recommender.py

from pydantic import BaseModel
from agents import function_tool, AsyncOpenAI  # ❌ No need to use OpenAIChatCompletionsModel
import os
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


class GoalInput(BaseModel):
    goal_type: str
    amount: int
    unit: str
    duration: int
    duration_unit: str


class WorkoutPlan(BaseModel):
    plan: str

@function_tool
async def workout_recommender(input: GoalInput) -> WorkoutPlan:
    """
    Generates a 7-day workout plan based on user's fitness goal.
    """
    try:
        prompt = f"""
        You are a virtual fitness coach. Create a 7-day workout plan for someone who wants to {input.goal_type} 
        {input.amount} {input.unit} in {input.duration} {input.duration_unit}.
        The plan should be well-balanced, safe, and motivating. Provide a daily breakdown in bullet points.
        """

        response = await client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[{"role": "user", "content": prompt}]
        )

        output = response.choices[0].message.content

        return WorkoutPlan(plan=output.strip())

    except Exception as e:
        print("❌ Error in workout_recommender:", e)
        import traceback
        traceback.print_exc()
        return WorkoutPlan(plan="❌ An error occurred while generating your workout plan. Please try again.")