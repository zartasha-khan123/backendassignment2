# app.py
from asyncio import Runner
from agents import Agent
import chainlit as cl
from agents_utils import planner_agent, config
from my_agents.nutrition_expert_agent import nutrition_expert_agent
from my_agents.injury_support_agent import injury_support_agent
from my_agents.escalation import escalation_agent

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("agent", planner_agent)
    cl.user_session.set("config", config)
    cl.user_session.set("chat_history", [])

    await cl.Message(
        content="👋 Hello! I'm your wellness assistant. Please select an expert to begin:",
        actions=[
            cl.Action(name="expert_select", label="🥗 Talk to Nutrition Expert", payload={"expert": "nutrition"}),
            cl.Action(name="expert_select", label="🦴 Talk to Injury Support", payload={"expert": "injury"}),
            cl.Action(name="expert_select", label="🧑‍🏫 Talk to Human Trainer", payload={"expert": "escalation"}),
            cl.Action(name="expert_select", label="🧠 Talk to Wellness Planner", payload={"expert": "planner"})
        ]
    ).send()

@cl.action_callback("expert_select")
async def handle_expert_selection(action: cl.Action):
    expert = action.payload.get("expert")

    if expert == "nutrition":
        cl.user_session.set("agent", nutrition_expert_agent)
        await cl.Message(content="✅ You're now chatting with the **Nutrition Expert**.").send()
    elif expert == "injury":
        cl.user_session.set("agent", injury_support_agent)
        await cl.Message(content="✅ You're now chatting with the **Injury Support Expert**.").send()
    elif expert == "escalation":
        cl.user_session.set("agent", escalation_agent)
        await cl.Message(content="✅ You're now chatting with the **Human Trainer**.").send()
    elif expert == "planner":
        cl.user_session.set("agent", planner_agent)
        await cl.Message(content="✅ You're now chatting with the **Wellness Planner**.").send()
    else:
        await cl.Message(content="❌ Unknown expert selected. Please try again.").send()

@cl.on_message
async def on_message(message: cl.Message):
    current_agent: Agent = cl.user_session.get("agent")
    config = cl.user_session.get("config")
    history = cl.user_session.get("chat_history") or []
    user_context = cl.user_session.get("context")

    history.append({"role": "user", "content": message.content})
    thinking = cl.Message(content="")
    await thinking.send()

    try:
        result = Runner.run_streamed(
            starting_agent=current_agent,
            input=history,
            context=user_context,
            run_config=config
        )

        new_agent = cl.user_session.get("agent")

        async for event in result.stream_events():
            if event.type == "raw_response_event" and hasattr(event.data, 'delta'):
                token = event.data.delta
                await thinking.stream_token(token)

        if new_agent.name != current_agent.name:
            history.append({"role": "assistant", "content": "✅ Transferred to specialist."})
            cl.user_session.set("agent", new_agent)

            new_history = [{"role": "user", "content": message.content}]
            result = Runner.run_streamed(
                starting_agent=new_agent,
                input=new_history,
                context=user_context,
                run_config=config
            )

            async for event in result.stream_events():
                if event.type == "raw_response_event" and hasattr(event.data, 'delta'):
                    token = event.data.delta
                    await thinking.stream_token(token)

        final_output = result.final_output or "⚠️ Sorry, no valid response was generated."

        agent_label_map = {
            "NutritionExpertAgent": "🥗 This is from the Nutrition Expert.",
            "InjurySupportAgent": "🦴 This is from the Injury Support Expert.",
            "EscalationAgent": "🧑‍🏫 This is from the Human Trainer.",
            "Wellness Planner": "🧠 This is from the Wellness Planner."
        }

        final_output += f"\n\n{agent_label_map.get(new_agent.name, '🤖 This is from an expert agent.')}"
        final_output += "\n\n🤖  Anything else I can help you with?"

        history.append({"role": "assistant", "content": final_output})
        cl.user_session.set("chat_history", history)

        thinking.content = final_output
        await thinking.update()

    except Exception as e:
        thinking.content = f"❌ Error: {e}"
        await thinking.update()
