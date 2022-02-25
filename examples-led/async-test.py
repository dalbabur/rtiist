import asyncio
import time

class AsyncTest:
    def __init__(self) -> None:
        self.value = 0
        self.done = 0

    async def stim_wrap(self):

        print(str(self.value) + ' Async Stim Start '+time.asctime())
        r = await self.stim(6, True)
        print(str(self.value) + ' Async Stim Done '+time.asctime())
        self.done = 1
        return r

    async def stim(self, timer, v):

        if v: print(str(self.value) + ' Stim Start '+time.asctime())
        self.value = 5
        await asyncio.sleep(timer)
        if v: print(str(self.value) + ' Stim Done '+ time.asctime())

        return 3

    async def measure(self):
        print(str(self.value) + ' Measure Start '+time.asctime())
        self.value = 1
        await asyncio.sleep(2)
        print(str(self.value) + ' Measure Done '+time.asctime())
        if self.done == 0: await self.stim(0, False)

        return True

async def main():
    a = AsyncTest()
    t1 = asyncio.create_task(a.stim_wrap())
    
    for i in range(9):
        await a.measure()
        time.sleep(1)

    await t1

if __name__ == "__main__":
    asyncio.run(main())