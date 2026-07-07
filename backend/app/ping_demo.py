"""Demo script to ping example URLs and print results.

Run as a module from the `backend` directory:
    python -m app.ping_demo
"""
import asyncio
from app.checker import ping_url


async def main():
    urls = [
        "https://example.com",
        "https://thisdoesnotexist123456.com",
    ]
    tasks = [ping_url(u, timeout=8.0) for u in urls]
    results = await asyncio.gather(*tasks)
    for r in results:
        print(r)


if __name__ == "__main__":
    asyncio.run(main())
