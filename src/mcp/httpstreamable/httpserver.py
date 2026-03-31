import random
from agents import mcp
from mcp.server.fastmcp import FastMCP

http_host = "127.0.0.1"
http_port = "8080"

mcp_server = FastMCP(name="Streamable Http Server", host= http_host, port=http_port)

@mcp_server.tool()
def add(a:int, b:int) -> int:
    print(f"I am adding {a} & {b}")
    return a+b

@mcp_server.tool()
def secret_word() -> str:
    print("Secret Word is being called")
    return random.choice(["Java", "Python", "AgenticAI"])


if __name__ == "__main__":
    mcp_server.run(transport="streamable-http")
