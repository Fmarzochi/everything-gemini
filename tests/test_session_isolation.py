import unittest
import threading
import time
from scripts.runtime.session_manager import SESSION_MANAGER
import os

class TestSessionIsolation(unittest.TestCase):
    def setUp(self):
        self.project_root = os.getcwd()
        self.sm = SESSION_MANAGER(self.project_root)

    def test_concurrent_task_updates(self):
        task_id = self.sm.start_task("Concurrent Update Task")
        
        def worker(w_id):
            for i in range(50):
                self.sm.update_task(task_id, "running", f"Event from worker {w_id} iter {i}")
                
        threads = [threading.Thread(target=worker, args=(w,)) for w in range(5)]
        
        for t in threads: t.start()
        for t in threads: t.join()
        
        total_events = sum(1 for task in self.sm.state["tasks"] if task["task_id"] == task_id for _ in task["events"])
        self.assertEqual(total_events, 250)

if __name__ == "__main__":
    unittest.main()
