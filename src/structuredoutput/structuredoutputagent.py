import asyncio
from agents import Agent, WebSearchTool, trace, Runner, gen_trace_id

from dotenv import load_dotenv
load_dotenv(override=True)

from pydantic import BaseModel
from typing import Optional


class company_detail(BaseModel):
    """
        This pydantic model will store company details, fundementals and stock price
    """
    company_name: str
    company_market_segment: Optional[str]
    stock_last_close_price: Optional[float]
    stock_last_close_date: Optional[float]
    fundamentals: Optional[str]


class companylist(BaseModel):
    company_list: list[company_detail]


structured_output_agent = Agent(
    name= "StructuredOutputAgent",
    model="gpt-5.4-nano-2026-03-17",
    instructions="You are a financial research agent. You use web search tool",
    tools=[WebSearchTool()],
    output_type=companylist
)


async def run_structured_output_agent():
    try:
        trace_id = gen_trace_id()
        print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")

        with trace("StructuredOutputAgent", trace_id=trace_id):
            # What are most active Nifty50 stocks in during 15 March 2026 till 28 March 2026
            result = await Runner.run(structured_output_agent, "Research for oil companies in Indian market")
            # print company details from company_list returned in result
            out = result.final_output
            print(out)
            print()
            for company in out.company_list:
                print(company.company_name, company.company_market_segment, company.stock_last_close_price)
                # or print one object per line as dict/JSON:
                print(company.model_dump())

            print('=' * 20)
            print(result.final_output.model_dump_json(indent=2))

            print('=' * 20)
            for c in result.final_output.company_list:
                print(f"{c.company_name}: {c.company_market_segment} -- {c.stock_last_close_price} @ {c.stock_last_close_date}")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    asyncio.run(run_structured_output_agent())