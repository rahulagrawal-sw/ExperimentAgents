from agents import Agent, WebSearchTool


summary_generator_agent = Agent(
    name="SummaryGeneratorAgent",
    model="gpt-5.4-nano-2026-03-17",
    instructions="You generate summary for a given input in 3-4 lines"
)