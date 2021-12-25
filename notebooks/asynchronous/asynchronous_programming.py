import asyncio


async def main():
    print('abc')
    await foo("text")


async def foo(text):
    print(text)
    await asyncio.sleep(1)

asyncio.run(main())
