# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents_utils import planner_agent, config
from my_agents.nutrition_expert_agent import nutrition_expert_agent
from my_agents.injury_support_agent import injury_support_agent
from my_agents.escalation import escalation_agent
from agents import Runner

app = FastAPI()

# ✅ Allow requests from frontend (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "FastAPI backend is running ✅"}

agent_map = {
    "planner": planner_agent,
    "nutrition": nutrition_expert_agent,
    "injury": injury_support_agent,
    "escalation": escalation_agent,
}

class ChatRequest(BaseModel):
    user_input: str
    expert: str
    context: dict = {}

@app.post("/chat")
async def chat_endpoint(data: ChatRequest):
    selected_agent = agent_map.get(data.expert, planner_agent)
    try:
        result = await Runner.run(
            starting_agent=selected_agent,
            input=data.user_input,
            context=data.context,
            run_config=config
        )
        return {"response": result.final_output or "⚠️ No valid response returned."}
    except Exception as e:
        return {"response": f"❌ Error from backend: {str(e)}"}
