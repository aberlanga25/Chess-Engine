import asyncio

import random


async def my_coroutine(term):
    print("start", term)
    n = random.uniform(0.2, 1.5)
    await asyncio.sleep(n)
    print("end", term)
    return "Term {} slept for {:.2f} seconds".format(term, n)


async def stop_all():
    """Cancels all still running tasks after one second"""
    await asyncio.sleep(1)
    print("stopping")
    fut.cancel()
    return ":-)"


loop = asyncio.get_event_loop()
terms = ["pie", "chicken", "things", "stuff"]
tasks = (my_coroutine(term) for term in terms)
fut = asyncio.gather(stop_all(), *tasks, return_exceptions=True)

print("Here we go!")
loop.run_until_complete(fut)

for task_result in fut.result():
    if not isinstance(task_result, Exception):
        print("OK", task_result)
    else:
        print("Failed", task_result)

loop.close()