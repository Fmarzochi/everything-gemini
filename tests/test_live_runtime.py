import unittest
import os
import json
import time
import asyncio
from scripts.orchestration.orchestrator import ORCHESTRATOR
from scripts.runtime.session_manager import SESSION_MANAGER
from scripts.runtime.tracer import TRACER

class TestLiveRuntimeAsync(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.project_root = os.getcwd()
        self.orchestrator = ORCHESTRATOR(self.project_root)
        self.tracer = TRACER(self.project_root)

    async def test_full_cycle(self):
        # 1. Dispatch a task
        task = "Write a security review for the new Python API"
        result = await self.orchestrator.dispatch(task)
        
        # 2. Verify Result
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["agent"], "security-reviewer")
        
        # 3. Verify Logs (Tracer)
        traces = self.tracer.get_traces()
        self.assertTrue(len(traces) > 0)
        
        event_types = [t["type"] for t in traces]
        self.assertIn("start", event_types)
        self.assertIn("routing", event_types)
        self.assertIn("validation", event_types)
        self.assertIn("complete", event_types)

    def test_session_persistence(self):
        sm = SESSION_MANAGER(self.project_root)
        tid = sm.start_task("Persistent Task")
        sm.end_task(tid, {"status": "ok"})
        
        session_file = sm.session_file
        self.assertTrue(os.path.exists(session_file))
        
        with open(session_file, "r") as f:
            data = json.load(f)
            self.assertEqual(data["tasks"][-1]["description"], "Persistent Task")
            self.assertEqual(data["tasks"][-1]["status"], "completed")

if __name__ == "__main__":
    unittest.main()
