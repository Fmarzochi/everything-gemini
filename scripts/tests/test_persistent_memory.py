import asyncio
import os
import sys
import shutil
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from memory.experience_store import ExperienceStore

async def test_memory():
    if os.path.exists(".sessions/memory/egc_memory.db"):
        os.remove(".sessions/memory/egc_memory.db")
        
    store = ExperienceStore(os.getcwd())
    
    print("--- Running Memory Tests ---")
    
    # 1. Record
    await store.record_success("analyze-code", "python-expert", {"result": "ok"})
    
    # 2. Recall
    history = await store.recall("analyze-code")
    assert len(history) == 1
    assert history[0]["result"] == "ok"
    print("Test 1 (Persistence/Recall): PASS")

if __name__ == "__main__":
    asyncio.run(test_memory())
