from typing_extensions import TypedDict 
from agents import function_tool, RunContextWrapper, AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

class SimpleMealPlanInput(TypedDict):
    diet_type: str

@function_tool
async def meal_planner(wrapper: RunContextWrapper, input: SimpleMealPlanInput) -> dict:
    try:
        prompt = (
            f"Create a 7-day meal plan for a {input['diet_type']} diet.\n"
            "Each day should include: breakfast, lunch, dinner, and a healthy snack in bullet points."
        )

        response = await client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[{"role": "user", "content": prompt}]
        )

        output = response.choices[0].message.content

        return {
            "meal_plan": output.strip()
        }

    except Exception as e:
        print("❌ Exception in meal_planner tool:", str(e))
        return {
            "error": f"❌ Exception in meal_planner tool: {str(e)}"
        }