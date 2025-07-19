#utils\handoffs.py
from agents import Agent
from agents import RunContextWrapper
import chainlit as cl
def make_on_handoff_message(agent: Agent):
    async def _on_handoff(ctx: RunContextWrapper[None]):
        # Notify user
        await cl.Message(
            content=f"🔄 Handing off to **{agent.name}**..."
        ).send()
        # Actually switch session agent
        cl.user_session.set("agent", agent)
    return _on_handoff