from agents import Agent, WebSearchTool


web_search_agent = Agent(
    name="WebSearchAgent",
    model="gpt-5.4-nano-2026-03-17",
    instructions="You are a web search agent to perform a research for a given topic",
    tools=[WebSearchTool()]
)