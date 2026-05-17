import unittest
import os
import json
from scripts.orchestration.router import AGENT_ROUTER

class TestRouter(unittest.TestCase):
    def setUp(self):
        self.test_dir = "temp_test_router"
        os.makedirs(os.path.join(self.test_dir, "registry"), exist_ok=True)
        
        self.affinity_map = {
            "domains": {
                "backend_python_api": ["python-reviewer", "architect"],
                "frontend_flutter": ["flutter-reviewer"]
            }
        }
        with open(os.path.join(self.test_dir, "AGENT_AFFINITY_MAP.json"), "w") as f:
            json.dump(self.affinity_map, f)
            
        self.runtime_map = {
            "agents": [
                {"name": "python-reviewer.md", "physicalPath": "agents/python-reviewer.md", "status": "cold"},
                {"name": "architect.md", "physicalPath": "agents/architect.md", "status": "cold"},
                {"name": "flutter-reviewer.md", "physicalPath": "agents/flutter-reviewer.md", "status": "cold"}
            ]
        }
        with open(os.path.join(self.test_dir, "registry", "runtime-map.json"), "w") as f:
            json.dump(self.runtime_map, f)
            
        self.router = AGENT_ROUTER(self.test_dir)

    def test_domain_detection(self):
        self.assertEqual(self.router._detect_domain("FastAPI backend"), "backend_python_api")
        self.assertEqual(self.router._detect_domain("Flutter UI"), "frontend_flutter")
        self.assertEqual(self.router._detect_domain("Unknown task"), "general")

    def test_agent_selection(self):
        agent = self.router.get_best_agent("FastAPI backend")
        self.assertEqual(agent["id"], "python-reviewer")
        
        agent_general = self.router.get_best_agent("Repair the leaky faucet")
        self.assertEqual(agent_general["id"], "architect")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir)

if __name__ == "__main__":
    unittest.main()
