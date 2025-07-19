from agents import function_tool, AsyncOpenAI
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


class ScheduleInput(BaseModel):
    wakeup_time: str
    sleep_time: str


class DailySchedule(BaseModel):
    schedule: str

@function_tool
async def generate_schedule(input: ScheduleInput) -> DailySchedule:
    """
    Generates a simple, healthy hour-by-hour daily schedule based on user's wake-up and sleep times.
    Includes meals, hydration, light exercise, and mindfulness.
    """
    try:
        prompt = f"""
Create a healthy hour-by-hour daily routine.

Details:
- Wake-up time: {input.wakeup_time}
- Sleep time: {input.sleep_time}

Include:
- 🥗 Meal times (Breakfast, Lunch, Dinner, and Snacks)
- 💧 Hydration reminders
- 🧘 Meditation or light wellness breaks
- 🏃‍♂️ Light exercise or stretching
- 🛌 Rest and wind-down periods

Format your answer in bullet points by time of day.
"""

        response = await client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[{"role": "user", "content": prompt}]
        )

        output = response.choices[0].message.content

        return DailySchedule(schedule=output.strip())

    except Exception as e:
        print("❌ Error in generate_schedule:", e)
        return DailySchedule(schedule="An error occurred while generating the schedule. Please try again later.")