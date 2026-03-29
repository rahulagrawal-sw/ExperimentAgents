import asyncio
from os import name

async def calculate(a: int, b: int):
    return a+b

async def main():
    # Single asyncio run
    result = await calculate(10,20)
    print(result)

    # Multiple asyncio runs
    results = await asyncio.gather(
        calculate(10,20),
        calculate(20,30),
        calculate(30,40),
        calculate(40,50)
    )

    for output in results:
        print(f"Inside for : {output}")


if __name__ == "__main__":
    asyncio.run(main())