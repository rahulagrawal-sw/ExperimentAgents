import asyncio
from agents import Agent, trace, Runner, gen_trace_id

from summarygeneratoragent import summary_generator_agent
from websearchagent import web_search_agent

from dotenv import load_dotenv
load_dotenv(override=True)

multi_agent = Agent(
    name= "MultiAgent",
    model="gpt-5.4-nano-2026-03-17",
    instructions="You delegate the user request to other agents for websearch and summary generation",
    tools=[
        web_search_agent.as_tool(tool_name="WebSearchToolUsingAgent", tool_description="You perform web search"),
        summary_generator_agent.as_tool(tool_name="SummaryGeneratorToolUsingAgent", tool_description="You generate summary")
    ]
)


async def run_multi_agent():
    try:
        trace_id = gen_trace_id()
        print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")

        with trace("MultiAgent", trace_id=trace_id):
            result = await Runner.run(multi_agent, "What are trending NSE stocks in March 2026")
            print(result.final_output)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    asyncio.run(run_multi_agent())