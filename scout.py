import asyncio

from rich import print
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

client = AsyncOpenAI()


async def main():
    response = await client.responses.create(
        model="gpt-4.1-mini",
        input="Tell me a three sentence bedtime story about a unicorn.",
    )
    print(response.output_text)


if __name__ == "__main__":
    print("Running Scout")
    asyncio.run(main())
