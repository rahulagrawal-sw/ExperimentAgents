import asyncio
from agents import Agent, Runner, WebSearchTool, function_tool, trace, gen_trace_id, ModelSettings

from dotenv import load_dotenv
from openai.types import Reasoning

load_dotenv(override=True)

@function_tool
async def add_numbers(a : int, b: int) -> int:
    """ Adds 2 numbers
    This function takes 2 integer number as input
    return addition of 2 input numbers
    """

    result = a+b
    print(f"addition --> {result}")
    return result

@function_tool  
async def fetch_weather(location: str) -> str:
    
    """Fetch the weather for a given location string input.

    Args:
        location: The location to fetch the weather for.
    """
    # In real life, we'd fetch the weather from a weather API
    return f"sunny in {location}"


INSTRUCTIONS = """
    You are a helpful assistant which use tools to give concise search summary to users questions. 
    For weather related queries ONLY use fetch_weather tool
    For number calculations ONLY use add_numbers tool.
    e.g. 
    - 4+4 use add_numbers tool
"""

tool_agent = Agent(
    name = "tool_agent",
    model = "gpt-5.2",
    instructions=INSTRUCTIONS,
    tools=[add_numbers, fetch_weather, WebSearchTool()],
    model_settings=ModelSettings(
        reasoning=Reasoning(effort="medium", summary="auto")
    )
)

async def run_agent_with_tools():
    try:
        print("run_agent_with_tools")

        trace_id = gen_trace_id()
        print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")

        with trace("AgentWithTool", trace_id=trace_id):
            result_1 = await Runner.run(tool_agent, "4+4")
            print(f"Result 1 --> {result_1.final_output}")

            result_2 = await Runner.run(tool_agent, "Whats weather in Pune")
            print(f"Result 2 --> {result_2.final_output}")

            result_3 = await Runner.run(tool_agent, "Explain different guardrail types")
            print(f"Result 3 --> {result_3.final_output}")

    except Exception as e:
        print(e)



if __name__ == "__main__":
    asyncio.run(run_agent_with_tools())