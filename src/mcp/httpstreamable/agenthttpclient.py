import asyncio
from agents import Agent, Runner, trace, gen_trace_id
from agents.model_settings import ModelSettings
from agents.mcp import MCPServer, MCPServerStreamableHttp

from dotenv import load_dotenv
load_dotenv(override=True)

http_host = "127.0.0.1"
http_port = "8080"
STREAMABLE_HTTP_URL = f"http://{http_host}:{http_port}/mcp"


async def run(my_mcp_server: MCPServer):

    agent = Agent(
        name = "Streamable MCP Agent",
        instructions= "You are a helpful assistant to answer maths and words problem",
        mcp_servers=[my_mcp_server],
        model="gpt-4o-mini",
        model_settings=ModelSettings(tool_choice="required")
    )

    # Use the `add` tool to add two numbers
    message = "Add these numbers: 7 and 22."
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

    # Run the `get_secret_word` tool
    message = "What's the secret word?"
    print(f"\n\nRunning: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

async def main():
    async with MCPServerStreamableHttp(
        name="Streamable HTTP Python Server",
        params={
            "url": STREAMABLE_HTTP_URL
        }
    ) as server:
        trace_id = gen_trace_id()
        with trace("MCPServerStreamableHttp Example", trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
            await run(server)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(e)
