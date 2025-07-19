#guardrails.py
from typing import List
from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    RunContextWrapper,
    TResponseInputItem,
    input_guardrail,
    output_guardrail,
    Runner,
)
from setup_config import google_gemini_config


# ------------ Structures ------------
class HealthInputOutput(BaseModel):
    is_safe: bool
    reason: str


# ------------ Guard Agents with model ------------
model = google_gemini_config.model

input_guard_agent = Agent(
    name="InputGuard",
    instructions="Check if the user input is health-related and safe. Avoid topics like suicide, self-harm, illegal drugs, etc.",
    output_type=HealthInputOutput,
    model=model,
)

output_guard_agent = Agent(
    name="OutputGuard",
    instructions="Check if the assistant response is health-related and whether it should include a medical disclaimer.",
    output_type=HealthInputOutput,
    model=model,
)


# ------------ Input Guardrail ------------
@input_guardrail
async def health_input_guardrail(
    ctx: RunContextWrapper,
    agent: Agent,
    input: str | List[TResponseInputItem],
) -> GuardrailFunctionOutput:
    result = await Runner.run(
        starting_agent=input_guard_agent, 
        input=input,
        context=ctx.context,
        run_config=google_gemini_config,
    )

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_safe,
    )


# ------------ Output Guardrail ------------
@output_guardrail
async def health_output_guardrail(
    ctx: RunContextWrapper,
    agent: Agent,
    output: str,
) -> GuardrailFunctionOutput:
    result = await Runner.run(
        starting_agent=output_guard_agent,
        input=output,
        context=ctx.context,
        run_config=google_gemini_config,
    )

    modified_response = output

    if not result.final_output.is_safe:
        modified_response += "\n\n⚠️ *This output may require professional review.*"
        tripwire = False  # ✅ DON'T BLOCK. Just warn.
    elif any(word in output.lower() for word in ["treatment", "doctor", "medical", "symptom", "health"]):
        modified_response += "\n\n⚠️ *Medical Disclaimer: This is AI-generated and not a substitute for professional advice.*"
        tripwire = False
    else:
        tripwire = False

    return GuardrailFunctionOutput(
        output_info=modified_response,
        tripwire_triggered=tripwire
    )