import asyncio
from openai import OpenAI
from agents import Agent, Runner, trace, gen_trace_id, ModelSettings
from openai.types.shared import Reasoning

import os
from dotenv import load_dotenv

load_dotenv(override=True)

reasoning_agent = Agent(
    name="reasoning_agent",
    model="gpt-5.2",
    instructions="You are helpful assistant. Only give concise answers",
    model_settings=ModelSettings(
        reasoning=Reasoning(effort="medium", summary="detailed")
    )
)

async def run_reasoning_agent():
    try:
        trace_id = gen_trace_id()
        with trace("reasoning_agent", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            agent_result_stream = Runner.run_streamed(reasoning_agent, "How to build scalable enterprise agentic systems")
            
            print("STARTING AGENT RUN", 20, "*")
            print("\n")

            async for event in agent_result_stream.stream_events():
                if event.type == "raw_response_event":
                    if event.data.type == "response.reasoning_text.delta":
                        print(f"\033[33m{event.data.delta}\033[0m",end="", flush=True)
                        print("\n")
                    elif event.data.type == "response.output_text.delta":
                        print(f"\033[32m{event.data.delta}\033[0m",end="", flush=True)
                        print("\n")

            print("\n\n\n")
            print("ENDED AGENT RUN", 20, "*")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    asyncio.run(run_reasoning_agent())