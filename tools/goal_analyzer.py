# tools/goal_analyzer.py
import re
from typing_extensions import TypedDict  # ✅ Correct for Python 3.11
from pydantic import BaseModel
from agents import function_tool, RunContextWrapper

class GoalInput(TypedDict):
    input_text: str

class StructuredGoal(BaseModel):
    goal_type: str
    amount: int
    unit: str
    duration: int
    duration_unit: str

@function_tool
async def analyze_goal(wrapper: RunContextWrapper, input: GoalInput) -> StructuredGoal:
    match = re.search(r"(lose|gain)\s+(\d+)\s*(kg|pounds)\s+(in|within)\s+(\d+)\s*(days|weeks|months)", input["input_text"].lower())
    if not match:
        raise ValueError("Invalid format. Try: 'Lose 5kg in 2 months'.")

    return StructuredGoal(
        goal_type=match.group(1),
        amount=int(match.group(2)),
        unit=match.group(3),
        duration=int(match.group(5)),
        duration_unit=match.group(6)
    )