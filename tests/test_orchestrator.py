import unittest
import os
import json
import shutil
import asyncio
from scripts.orchestration.orchestrator import ORCHESTRATOR

class TestOrchestratorAsync(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.test_dir = "temp_test_orch"
        os.makedirs(os.path.join(self.test_dir, "registry"), exist_ok=True)
        
        affinity = {"domains": {"test": ["agent-a", "agent-b"]}}
        with open(os.path.join(self.test_dir, "AGENT_AFFINITY_MAP.json"), "w") as f:
            json.dump(affinity, f)
            
        runtime = {"agents": [
            {"name": "agent-a.md", "physicalPath": "agents/agent-a.md", "status": "cold"},
            {"name": "agent-b.md", "physicalPath": "agents/agent-b.md", "status": "cold"},
            {"name": "architect.md", "physicalPath": "agents/architect.md", "status": "cold"}
        ]}
        with open(os.path.join(self.test_dir, "registry", "runtime-map.json"), "w") as f:
            json.dump(runtime, f)
            
        self.orch = ORCHESTRATOR(self.test_dir)

    async def test_dispatch_success(self):
        # Mocking keyword detection for 'test' domain
        self.orch.router.domain_keywords["test"] = ["match"]
        res = await self.orch.dispatch("This is a match task")
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["agent"], "agent-a")
        
        log_path = os.path.join(self.test_dir, ".sessions", "execution_log.jsonl")
        self.assertTrue(os.path.exists(log_path))

    async def asyncTearDown(self):
        shutil.rmtree(self.test_dir)

if __name__ == "__main__":
    unittest.main()
