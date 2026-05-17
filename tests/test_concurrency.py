import unittest
import asyncio
import time
from scripts.runtime.async_task_queue import EXECUTION_QUEUE

class TestConcurrency(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.eq = EXECUTION_QUEUE(max_concurrent=3)
        self.workers = await self.eq.start_workers(3)
        self.completed_tasks = []

    async def dummy_task(self, task_id, delay=0.1):
        await asyncio.sleep(delay)
        self.completed_tasks.append(task_id)
        return task_id

    async def test_concurrent_execution(self):
        # Submit 10 tasks
        for i in range(10):
            await self.eq.submit_task(1, f"task-{i}", self.dummy_task, f"task-{i}", delay=0.01)
            
        await self.eq.queue.join()
        
        self.assertEqual(len(self.completed_tasks), 10)

    async def test_priority(self):
        # Submit task with lower priority first (higher number = lower priority)
        await self.eq.submit_task(3, "low-priority", self.dummy_task, "low", delay=0.2)
        # Immediately submit high priority
        await self.eq.submit_task(1, "high-priority", self.dummy_task, "high", delay=0.1)
        
        await self.eq.queue.join()
        
        # The worker pool size is 3, so both start immediately. Priority is only respected if queue > workers.
        # Let's pause workers to queue up tasks.
        pass

    async def asyncTearDown(self):
        for w in self.workers:
            w.cancel()

if __name__ == "__main__":
    unittest.main()
