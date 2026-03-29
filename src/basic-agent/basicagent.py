import asyncio
from openai import OpenAI
from agents import Agent, Runner, trace, gen_trace_id

import os
from dotenv import load_dotenv

load_dotenv(override=True)

basic_agent = Agent(
    name="basic_agent",
    model="gpt-4o-mini",
    instructions="You are helpful assistant. Only give concise summary anwers without any details"
)

async def run_basic_agent():
    try:
        trace_id = gen_trace_id()
        with trace("basic_agent", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            agent_result = await Runner.run(basic_agent, "What is asyncio")
            print(agent_result.final_output)
    except Exception as e:
        print(e)

async def main():
    print("I am main")
    await run_basic_agent()

if __name__ == "__main__":
    asyncio.run(main())