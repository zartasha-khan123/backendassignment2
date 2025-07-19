from agents import function_tool, AsyncOpenAI, RunContextWrapper
from typing_extensions import TypedDict  
import os
from dotenv import load_dotenv


load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

class TrackerInput(TypedDict):
    name: str
    steps_walked: int
    water_intake_liters: float
    sleep_hours: float
    mood: str

@function_tool
async def summarize_user_progress(wrapper: RunContextWrapper, input: TrackerInput) -> str:
    """
    Summarizes the user's daily health progress with a friendly tone in 3–5 lines.
    """
    try:
        prompt = f"""
Summarize the user's health progress based on the following data:

Name: {input['name']}
Steps Walked: {input['steps_walked']}
Water Intake: {input['water_intake_liters']} liters
Sleep Hours: {input['sleep_hours']}
Mood: {input['mood']}

Write a short and encouraging summary in 3–5 lines.
"""

        response = await client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("❌ Error in summarize_user_progress:", e)
        return "An error occurred while summarizing progress. Please try again later."